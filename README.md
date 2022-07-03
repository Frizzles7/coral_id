# coral_id

## Overview

The goal of this project is to build a coral identification machine learning model. Using pictures of coral frags, can we reliably identify the type of coral? How specific can we get with this identification?

## Obtaining Training Data

The first step in this project is to obtain the training data. I am beginning with pictures posted on [Reef2Reef.com](www.Reef2Reef.com) during live sales, as thousands of corals are posted in each live sale. I am also beginning with the live sales from World Wide Corals (WWC), because the first live sale I ever participated in was put on by WWC, they provide quality corals, and they have tons of images available from their numerous live sales. You can view pictures of coral frags currently for sale by WWC on their website [worldwidecorals.com](worldwidecorals.com).

If you are wondering what a coral frag looks like, here is an example. This coral is named a WWC Candy Corn Chalice. (Did I mention that these corals have some really fun names?)

<img src="https://github.com/Frizzles7/coral_id/blob/master/TSR11-37-575.jpg" width="300"/>

### BTW: What is a Live Sale?

If you are wondering what a Live Sale is, this is similar to an online auction, and it occurs on the forums of the Reef2Reef website. Pictures of coral frags (small pieces of coral cut off from the mother colony) are posted on the forums, and the first person to purchase the listed coral wins. Since these are live pieces of coral, each one is different. Usually, many good deals are provided, and rare corals are sometimes offered. These sales can last hours (or even an entire weekend). It is a fun way for people to buy corals for their reef tanks and to spend time with other reefers and vendors.

### Scraping for Data

To get the training data, I will need to scrape the images along with the names from the [Reef2Reef.com](www.Reef2Reef.com) website.  I wrote the script `scrape_images.py` to do this job.  For a given url, author of the post, and location of the images, I can pull down all of the images from that thread on the forums.  I save each of the images along with a file mapping the name of the saved image file and the name of the coral.

I then searched for the appropriate live sale threads, as listed in `to_scrape.txt` and applied the script to each of the threads, building up a training set of images.

Before scraping the data, ensure that the folder `scraped_images` exists.

To run the scraping on a specific thread, specify the url, poster, and image location at the command line. The verbose tag is also helpful for logging. Below is an example to perform the scraping and log the results:

```
python3 scrape_images.py -v -u 'https://www.reef2reef.com/threads/world-wide-corals-tax-craze-live-sale-2300-frags-discounted-beyond-belief.552524/page-24' -p 'WWC' -i 'worldwidecorals.sirv.com/Tax_Craze_2019' > 20220626_tax_craze_2019.log 2>&1
```

## Data Cleaning and Preparation

...more to come...

