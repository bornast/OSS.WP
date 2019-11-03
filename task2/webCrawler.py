# -*- coding: utf-8 -*-
import re
import time
import urllib2
import sys

domain = sys.argv[1]
starting_url = "https://" + domain
visited_urls = []
links_to_visit = 50

def crawl(url):
    if len(visited_urls) >= links_to_visit:
        return

    if (is_url_visited(url) == True):
        return

    try:
        page_html = get_page_html(url)
    except:
        return

    visited_urls.append(url)

    page_urls = get_urls_from_html(page_html)

    for page_url in page_urls:
        crawl(page_url)

def get_page_html(url):
    hdrs = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
    }

    try:
        request = urllib2.Request(url, headers=hdrs)

        page = urllib2.urlopen(request)

        content = page.read()

        return content
    except:
        raise Exception("error fetching html from page: " + url)

def get_urls_from_html(html):
    result = []

    regex_items = re.findall(
        "href=\"(https?:\/\/)?(" + domain + ")\/(.*?)\"", html)

    for item_group in regex_items:
        full_url = item_group[0] + item_group[1] + "/" + item_group[2]
        result.append(full_url)

    return result

def is_url_visited(url):
    if url in visited_urls:
        return True
    elif (url[-1] == '/' and url[:-1] in visited_urls):
        return True
    elif (url[-1] != '/' and (url + '/') in visited_urls):
        return True
        
    return False

crawl(starting_url)
print visited_urls
