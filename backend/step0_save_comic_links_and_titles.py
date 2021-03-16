"""
extract and saves the title and image URL from 'xkcd.com' html pages

takes about 15 min to run

@author: Gati Aher
"""

# save
import json
# parse html
import re
import string
import requests
import bs4
# visualize progress bar in terminal
from tqdm import tqdm
# get num comics
from utils import get_latest_comic_num

# define save locations
title_save_location = "./data/comic_tags/titles.json"
image_urls_save_location = "./data/comic_tags/image_urls.json"
error_save_location = "./data/comic_tags/ERROR_"


def get_text(comic_number):
    """
    For each comic number, scrape info from explain xkcd page

    Args:
        comic_number (positive integer): comics are numbered sequentially

    Return:
        title (string):     natural language title of comic
        image url (string): image url of comic (where image is located).

    """

    # get HTML text
    # from explainxkcd because it handles practical joke comics appropriately
    text = requests.get(
        "https://www.explainxkcd.com/wiki/index.php/" + str(comic_number))
    if text.status_code != 200:
        raise Exception(str(text.status_code) +
                        " could not find explainxkcd page")
    soup = bs4.BeautifulSoup(text.text, 'html5lib')

    # get title
    title = soup.title.string[:-15]

    # get image url
    image = soup.find("a", {"class": "image"}).find("img")
    image_url = "https://www.explainxkcd.com" + image['src']

    return title, image_url


if __name__ == "__main__":
    """Record all comics in range 0-num_comics. Record any errors"""

    num_comics = get_latest_comic_num() + 1

    titles = ["000empty000"] * num_comics
    image_urls = ["000empty000"] * num_comics

    for i in tqdm(range(1, num_comics)):
        try:
            title, image_url = get_text(i)
            titles[i] = title
            image_urls[i] = image_url
            print(i, title, image_url)
        except Exception as err:
            # record errors
            f = open(error_save_location + str(i) + ".txt", "w")
            f.write("*** (" + str(i) + ") An exception occurred ***")
            f.write(" ".join(err.args))
            f.close()

    # save as individual json arrays
    with open(title_save_location, 'w') as f:
        json.dump(titles, f)
    with open(image_urls_save_location, 'w') as f:
        json.dump(image_urls, f)

    print("Finished Step0: saving", num_comics, "comics")
