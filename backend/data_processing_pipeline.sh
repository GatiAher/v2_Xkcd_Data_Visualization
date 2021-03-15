#!/bin/bash

mkdir -p data/comic_tags
python3 step0_save_comic_links_and_titles.py
# python3 step0_tag_comics_with_categories_benchmark.py