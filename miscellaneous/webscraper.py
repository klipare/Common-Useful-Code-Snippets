#!/usr/bin/python

# This script is to scan the FAQ webpage and split the information into questions and answers
# This script requires Python version 3.x to be installed in the system

# The arguments for the scripts are: N/A

# We are using Beautifulsoup4 to parse HTML webpage. Documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/.
# Make HTTP get requests using requests. Documentation: http://docs.python-requests.org/en/master/

# usage python <webscraper.py> --path <directory_path> --filename <output_filename_to_store_result> --url <https://type.url.com/faqs/>
# usage python <webscraper.py> -p <directory_path> -f <output_filename_to_store_result> -u 


import os
from os import getcwd
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


# parse web pages
cwd = os.getcwd()
print("current working directory", cwd)
raw_html = simple_get('https://chime.aws/faq/')
html = BeautifulSoup(raw_html, 'html.parser')
for i, p in enumerate(html.select('p')):
    with open('aws_faq.csv', 'a', encoding='utf-8') as r:
        if "Q:" in p.text:
            r.write('\n')
            r.write("'")
            r.write(str(i))
            r.write("'")
            r.write(',')
            r.write("'")
            r.write(p.text)
            r.write("'")
            r.write(',')
        else:
            r.write("'")
            r.write(p.text)
            r.write("'")
