#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

from .constants import BASE_URL, INTERVAL_BETWEEN_REQUESTS

def get_soup(page='1'):
    """
    Returns a bs4 object of the page requested
    """
    content = requests.get('%s/?page=%s' % (BASE_URL, page)).text
    return BeautifulSoup(content)

def comment_soup(product_id):
    """
    Returns a bs4 object of the requested Comment
    """
    url = BASE_URL + '/posts/' + str(product_id)+ "?modal=true"
    return BeautifulSoup(requests.get(url).text)
