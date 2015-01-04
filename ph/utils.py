#!/usr/bin/env python
import re
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

def striphtml(htmlTxt):
    if htmlTxt is None:
        return None
    else:
        temp = ''.join(BeautifulSoup(htmlTxt).findAll(text=True))
        return " ".join(temp.split())

def strp(word):
    return str(word).lstrip().rstrip()