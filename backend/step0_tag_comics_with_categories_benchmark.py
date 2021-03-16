"""
extract and save user tags from 'explain xkcd' html pages

takes 2-5 minutes to run

@author: Gati Aher
"""

# save
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
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
comic_tags_save_location = "./data/comic_tags/comic_tags.json"


def get_comic_serial_numbers(soup):
    """
    get list of comic numbers on soup's page

    Args:
        soup: beautiful soup object

    Return:
        ret_list (list of positive integers):   list of comic numbers on page
    """
    ret_list = []

    mw_pages = soup.find("div", {"id": "mw-pages"})
    if mw_pages:
        anchors = mw_pages.find_all("a")

        for doc in anchors:
            title = doc["title"]
            try:
                serial_number = re.search(r'\d+', title).group()
                if len(serial_number) > 1:
                    ret_list.append(int(serial_number))
            except:
                print("!! ERROR when extracting serial number from title: ", title)

    return ret_list


def get_subcategory_hrefs(soup):
    """
    get list of subcategory hrefs on soup's page

    Arg:
        soup: beautiful soup object

    Return:
        ret_list (list of strings):     list of links to subcategory pages
    """
    ret_list = []

    mw_subcategories = soup.find("div", {"id": "mw-subcategories"})
    if mw_subcategories:
        anchors = mw_subcategories.find_all("a")

        for doc in anchors:
            href = doc["href"]
            ret_list.append(href)

    return ret_list


def go_into_subcategory(link, comic_tags, visited_subcategories):
    """
    Recursively traverse explain xkcd subcategory pages
    Not all tags are accessible from main subcategory page

    Args:
        link (string):                              link to sub-category page 
        comic_tags (list of lists of strings):      list of sub-categories for each comic, in overall list ordered by comic serial number
        visited_subcategories (list of strings):    list of visited sub-categories
    """
    text = requests.get("https://www.explainxkcd.com" + link)
    if text.status_code != 200:
        print("!! ERROR: ", text.status_code, link)
        return
    soup = bs4.BeautifulSoup(text.text, 'lxml')

    tag = soup.title.string.lower()[9:-15]

    if tag not in visited_subcategories:
        visited_subcategories.append(tag)

        serial_numbers = get_comic_serial_numbers(soup)
        for num in serial_numbers:
            if num < len(comic_tags):
                comic_tags[num].append(tag)
            else:
                print("!! Error: unaccounted comic number", num)

        hrefs = get_subcategory_hrefs(soup)
        for href in hrefs:
            go_into_subcategory(href, comic_tags, visited_subcategories)


if __name__ == "__main__":
    "Scrape comics relation to user-defined categories"

    num_comics = get_latest_comic_num() + 1
    # just ignore the first index, indexing works nicely
    comic_tags = [[] for i in range(num_comics)]
    visited_subcategories = []
    go_into_subcategory("/wiki/index.php/Category:Comics_by_topic",
                        comic_tags,
                        visited_subcategories)

    # save categories as one-hot vectors (1-0 indicating presence of category)
    # take out any categories that don't have any comics (pages with only subcategories)
    mlb = MultiLabelBinarizer()
    comic_serial_numbers = [str(i) for i in range(num_comics)]
    df = pd.DataFrame(mlb.fit_transform(comic_tags),
                      columns=mlb.classes_,
                      index=comic_serial_numbers)

    df.to_json(path_or_buf=comic_tags_save_location)
    print("Finished Step0: saving ", len(
        visited_subcategories), " subcategories")
