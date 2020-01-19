#!/usr/bin/env python
"""Python-Pinboard

Python script for downloading your saved stories and saved comments on Hacker News
and converting them to a JSON format for easy use.

Originally written on Pythonista on iPad
"""

__version__ = "1.1"
__license__ = "BSD"
__copyright__ = "Copyright 2013-2014, Luciano Fiandesio"
__author__ = "Luciano Fiandesio <http://fiandes.io/> & John David Pressman <http://jdpressman.com>"

import argparse
import time
import re
import sys
import urllib
import urllib.parse as urlparse
import json
from bs4 import BeautifulSoup
import requests
from types import *
import xml.etree.ElementTree as xml

HACKERNEWS = 'https://news.ycombinator.com'

parser = argparse.ArgumentParser()

parser.add_argument("username", help="The Hacker News username to grab the stories from.")
parser.add_argument("password", help="The password to login with using the username.")
parser.add_argument("-f", "--file", help="Filepath to store the JSON document at.")
parser.add_argument("-n", "--number", default=1, type=int, help="Number of pages to grab, default 1. 0 grabs all pages.")
parser.add_argument("-s", "--stories",  action="store_true", help="Grab stories only.")
parser.add_argument("-c", "--comments", action="store_true", help="Grab comments only.")

arguments = parser.parse_args()

def getSavedStories(session, hnuser, page_range):
    """Return a list of story IDs representing your saved stories. 

    This function does not return the actual metadata associated, just the IDs. 
    This list is traversed and each item inside is grabbed using the Hacker News 
    API by story ID."""
    story_ids = []
    for page_index in page_range:
        saved = session.get(HACKERNEWS + '/upvoted?id=' + 
                            hnuser + "&p=" + str(page_index))
        soup = BeautifulSoup(saved.content)
        for tag in soup.findAll('td',attrs={'class':'subtext'}):
            if tag.a is not type(None):
                a_tags = tag.find_all('a')
                for a_tag in a_tags:
                    if a_tag['href'][:5] == 'item?':
                        story_id = a_tag['href'].split('id=')[1]
                        story_ids.append(story_id)
                        break
    return story_ids

def getSavedComments(session, hnuser, page_range):
    """Return a list of IDs representing your saved comments.

    This function does not return the actual metadata associated, just the IDs.
    This list is traversed and each item inside is grabbed using the Hacker News
    API by ID."""
    comment_ids = []
    for page_index in page_range:
        saved = session.get(HACKERNEWS + '/upvoted?id=' + 
                            hnuser + "&comments=t" + "&p=" + str(page_index))
        soup = BeautifulSoup(saved.content)
        for tag in soup.findAll('td',attrs={'class':'default'}):
            if tag.a is not type(None):
                a_tags = tag.find_all('a')
                for a_tag in a_tags:
                    if a_tag['href'][:5] == 'item?':
                        comment_id = a_tag['href'].split('id=')[1]
                        comment_ids.append(comment_id)
                        break
    return comment_ids


def loginToHackerNews(username, password):
    s = requests.Session() # init a session (use cookies across requests)

    headers = { # we need to specify an header to get the right cookie
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0',
        'Accept' : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    # Build the login POST data and make the login request.
    payload = {
        'whence': 'news',
        'acct': username,
        'pw': password
    }
    auth = s.post(HACKERNEWS+'/login', data=payload, headers=headers )
    if 'Bad login' in str(auth.content):
        raise Exception("Hacker News authentication failed!")
    if not username in str(auth.content):
        raise Exception("Hacker News didn't succeed, username not displayed.")

    return s # return the http session

def getHackerNewsItem(item_id):
    """Get an 'item' as specified in the HackerNews v0 API."""
    time.sleep(0.2)
    item_json_link = "https://hacker-news.firebaseio.com/v0/item/" + item_id + ".json"
    try:
        with urllib.request.urlopen(item_json_link) as item_json:
            return json.loads(item_json.read().decode('utf-8'))
    except urllib.error.URLError:
        return {"title":"Item " + item_id + " could not be retrieved",
                "id":item_id}

def item2stderr(item_id, item_count, item_total):
    sys.stderr.write("Got item " + item_id + ". ({} of {})\n".format(item_count,
                                                                     item_total))
    
def main():
    json_items = {"saved_stories":list(), "saved_comments":list()}
    if arguments.stories and arguments.comments:
        # Assume that if somebody uses both flags they mean to grab both
        arguments.stories = False
        arguments.comments = False
    item_count = 0
    session = loginToHackerNews(arguments.username, arguments.password)
    page_range = range(1, arguments.number + 1)
    if arguments.stories or (not arguments.stories and not arguments.comments):
        story_ids = getSavedStories(session,
                                    arguments.username,
                                    page_range)
        for story_id in story_ids:
            json_items["saved_stories"].append(getHackerNewsItem(story_id))
            item_count += 1
            item2stderr(story_id, item_count, len(story_ids))
    if arguments.comments or (not arguments.stories and not arguments.comments):
        item_count = 0
        comment_ids = getSavedComments(session,
                                       arguments.username,
                                       page_range)
        for comment_id in comment_ids:
            json_items["saved_comments"].append(getHackerNewsItem(comment_id))
            item_count += 1
            item2stderr(comment_id, item_count, len(comment_ids))
    if arguments.file:
        with open(arguments.file, 'w') as outfile:
            json.dump(json_items, outfile)
    else:
        print(json.dumps(json_items))

if __name__ == "__main__":
    main()
