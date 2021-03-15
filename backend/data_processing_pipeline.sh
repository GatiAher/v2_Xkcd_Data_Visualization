#!/bin/bash

mkdir -p data/comic_tags
python3 step0_save_comic_links_and_titles.py
python3 step0_tag_comics_with_categories_benchmark.py > data/log_step0_tag.txt

# now check data folder and log file for any errors
# if there were errors, rerun scripts, check if explainxkcd has all info
# or manually fill 000empty000 values in titles.json and image_urls.json

