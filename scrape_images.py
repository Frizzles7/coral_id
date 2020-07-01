#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# NAME: scrape_images.py
# ONELINER: Script to scrape images from Reef2Reef.com
# LANGUAGE: Python 3.7
# AUTHOR: Megan McGee
# CREATED: 2020-06-30
#
# DESCRIPTION:
#   This script was designed to get all of the images and names of corals
#   posted for sale during Reef2Reef live sales. These images and names can 
#   then be used in future machine learning and deep learning projects.
#
#   This script scrapes images. To use this, supply a url from Reef2Reef.com
#   from which to scrape, the Reef2Reef author name for the posts to scrape,
#   and the image location from the data-url. This script will go through all
#   of the pages of the forum thread, download the images posted by the
#   specified poster, and append the names to a text file.
#
#   Note that this script may download many image files. Use at your own risk.
#

import argparse
import csv
import os
import re
import time

from bs4 import BeautifulSoup as bs
import requests
from urllib.parse import urlparse
from urllib.request import urlretrieve


def is_url_valid(url):
    """
    Check if the format of the given url is valid.
    Checks for scheme and netloc, then checks for status code.
    
        Parameters:
            url (string): A string containing the url
            
        Returns:
            is_valid (boolean): True if valid, else False
    """
    
    parsed = urlparse(url)
    
    is_valid = False
    if bool(parsed.netloc) and bool(parsed.scheme):
        if requests.get(url).status_code == 200:
            return True

    return is_valid


def get_all_images(url, poster, image_loc):
    """
    Returns all image urls from the given url.
    
        Parameters:
            url (string): A string containing the url
            poster (string): A string containing the Reef2Reef author name of 
                the post, such as 'WWC-BOT'
            image_loc (string): A string containing the location of the images,
                such as 'worldwidecorals.sirv.com/TSLS_20' from the data-url 
                for the image
        
        Returns:
            image_links (list): A list of [names, image urls] from the page
    """
    
    soup = bs(requests.get(url).content, "html.parser")
    soup_div = soup.find_all('div', 
        attrs={'class':'message-userContent lbContainer js-lbContainer',
               'data-lb-caption-desc':re.compile(r'^%s'%poster)})
    
    # extract links to each of the images
    # when find an image, also extract the name for labels in training
    images=[]
    names=[]
    for tt in soup_div:
        try:
            t1 = tt.find_all('img')
            for image in t1:
                if image_loc in image['data-url']:
                    images.append('https://www.reef2reef.com' + image['src'])
            t2 = tt.find_all('b')
            for name in t2:
                names.append(name.text)
        except:
            pass
    names_trimmed = names[0::6]
    
    # if the lengths of the two lists are the same, zip together
    if len(names_trimmed) == len(images):
        image_links = [list(i) for i in zip(names_trimmed, images)]
    else:
        image_links = []
        print('WARNING: images and names are not the same length',
              '\n', 'no image_links this page')
    
    return image_links


def download_images(image_links):
    """
    Downloads all images provided in the list of image names and urls.
    
        Parameters:
            image_links (list): A list of [names, image urls]
    """

    for i in image_links:
        filename = os.path.join('./scraped_images/', 
                                urlparse(i[1]).path.split('/')[-1])
        urlretrieve(i[1], filename)


def output_names_files(image_links):
    """
    Outputs a csv file with the coral name and filename.
    
        Parameters:
            image_links (list): A list of [names, image urls]
        
        Returns:
            coral_names_files.csv (file): 
    """
    
    with open('coral_names_files.csv', 'a', newline='') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerows(image_links)


def get_num_pages(url):
    """
    Returns the number of pages in this thread of the forum.
    
        Parameters:
            url (string): A string containing the url
        
        Returns:
            num_pages (int): The number of pages
    """
    
    soup = bs(requests.get(url).content, "html.parser")
    nums=[]
    soup_ul = soup.find_all('ul', attrs={'class':'pageNav-main'})
    for tt in soup_ul:
        t1 = tt.find_all('a')
        for num in t1:
            try:
                nums.append(int(num.text))
            except:
                pass
    
    num_pages = max(nums)
    return num_pages


def main(url, poster, image_loc):
    """
    Loops through the pages in this thread of the forum to get all images.
    
        Parameters:
            url (string): A string containing the url with the starting page
                for scraping
            poster (string): A string containing the Reef2Reef author name
                of the post, such as 'WWC-BOT'
            image_loc (string): A string containing the location of the
                images, such as 'worldwidecorals.sirv.com/TSLS_20' from the
                data-url for the image
    """
    
    # find first page, last page, and base url
    if is_url_valid(url):
        last_page = get_num_pages(url)
        base_url, first_page  = url.split('/page-')
        first_page = int(first_page)
        
    # loop through pages from first to last, pausing periodically
    print('Beginning scrape at page ', first_page)
    for i in range(first_page, last_page+1):
        # implement periodic pause
        if i % 20 == 0:
            print('pausing for 30 seconds at page ', i)
            time.sleep(30)
        # get url for the current page of the forum and scrape
        current_url = base_url + '/page-' + str(i)
        if is_url_valid(current_url):
            image_links = get_all_images(current_url)
            if image_links == []:
                print('page ', i, ' has no image links')
            download_images(image_links)
            output_names_files(image_links)
        else:
            print('WARNING: page ', i, ' has invalid url')
    print('End of scrape.')


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--url',
        dest='url', action='store', type=str,
        help='Specify url from which to scrape.',
        required=True)
    parser.add_argument(
        '-p', '--poster',
        dest='poster', action='store', type=str,
        help='Specify author name of the post.',
        required=True)
    parser.add_argument(
        '-i', '--image_loc',
        dest='image_loc', action='store', type=str,
        help='Specify the location of the images from the data-url.',
        required=True)
    parser.add_argument(
        '-q', '--quit',
        dest='do_quit', action='store_true',
        help='Display informational messages then quit.',
        default=False)

    args = parser.parse_args()
    do_quit = args.do_quit
    if do_quit:
        print('Input Arguments:')
        print('  do_quit        :', do_quit)        
        print('  url            :', args.url)
        print('  poster         :', args.poster)
        print('  image_loc      :', args.image_loc)

    if do_quit:
        raise SystemExit('\n --- Requested quit --- \n')

    main(args.url, args.poster, args.image_loc)

