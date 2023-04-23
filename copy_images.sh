#!/bin/bash

cd /Users/megan/projects/coral_id/coral_types_filepaths

for txtfile in *.txt; do
    mkdir "/Users/megan/projects/coral_id/sorted_images/${txtfile%.*}"

    while IFS= read -r line; do
        src_path="/Users/megan/projects/coral_id/scraped_images/$line"
        dir_num=$(basename "$(dirname "$src_path")" | awk -F '_' '{print $NF}')
        filename=$(basename "$src_path")
        new_filename="${dir_num}_${filename}"
        cp "$src_path" "/Users/megan/projects/coral_id/sorted_images/${txtfile%.*}/$new_filename"
    done < "$txtfile"
done
