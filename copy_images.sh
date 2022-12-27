#!/bin/bash

cd /home/megan/projects/coral_id/coral_types_filepaths

for txtfile in *.txt; do
    mkdir "/home/megan/projects/coral_id/sorted_images/${txtfile%.*}"
    
    while IFS= read -r line; do
        src_path="/home/megan/projects/coral_id/scraped_images/$line"
        cp "$src_path" "/home/megan/projects/coral_id/sorted_images/${txtfile%.*}"
    done < "$txtfile"
done

