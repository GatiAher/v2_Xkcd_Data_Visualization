"""
shared functions
"""

# parse html
import re
import string
import requests
import bs4


def get_latest_comic_num():
    """
    Load the comic number from 'latest_comic_num.txt'

    Return:
        serial number (positive integer):   latest comic serial number
    """

    text = requests.get("https://xkcd.com")
    if text.status_code != 200:
        return 0
    soup = bs4.BeautifulSoup(text.text, 'lxml')

    title = soup.title.string

    ele = soup.find(id="middleContainer").find_all(class_="comicNav")[
        1].nextSibling.nextSibling.nextSibling
    serial_number = re.search(r'\d+', str(ele)).group()

    return int(serial_number)
