import json

from bs4 import BeautifulSoup
from datetime import datetime
from collections import Counter
from typing import List, Dict
from pprint import pprint
from urllib import request

def get_date(posts):
    def format_date(dt: str):
        original_datetime = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        return original_datetime.strftime("%d-%m-%Y")

    # the date filed containes a datetime string, we only need the date, so might
    # as well format it to the format we need
    dates = [format_date(post['dateModified']) for post in posts]
    counter = Counter(dates)
    return counter.most_common(1)[0][0]

def read_url_list(url_list_path: str):
    with open(url_list_path, "r") as url_list_file:
        return url_list_file.read().splitlines()


def get_html(url: str) -> str:
    with request.urlopen(url) as response:
        return response.read()

def get_posts(html: str):
    soup = BeautifulSoup(html, features="html.parser")

    # Live blog updates + main entity (duplicate story displayed at the start)
    foo = soup.select_one('script[id="liveBlog-schema"]')

    # Some days don't have the data within as script tag with id="liveBlog-schema", so we fall back to
    # type="application/ld+json".
    if foo is None:
        foo = soup.select_one('script[type="application/ld+json"]')

    stories = json.loads(foo.text)

    if type(stories) is list:
        # On the 17th of December 2023, they decided to change the structure for some reason.
        return stories[1]["liveBlogUpdate"]
    else:
        return stories["liveBlogUpdate"]


# Returns the CNN headlines for the given URL in the format:
# [
#   { 'link': ..., 'headline': ... },
# ]
def get_cnn_headlines(url: str) -> List[Dict[str, str]]:
    html = get_html(url)
    posts = get_posts(html)

    # Not all posts have the same publish date, some are published AFTER midnight (the next day)
    # So we take the most common day.
    # date = get_date(posts)
    filtered_posts = [{'link': post['url'], 'headline': post['headline']} for post in posts if 'headline' in post and 'url' in post]

    return filtered_posts


def example():
    pprint(get_cnn_headlines('https://edition.cnn.com/middleeast/live-news/israel-hamas-war-gaza-news-11-24-23/index.html'))
