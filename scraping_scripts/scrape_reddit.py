from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv

REDDIT_URL = 'https://www.reddit.com'

def scrape_html(url):
    browser = webdriver.Firefox()
    browser.get(url)
    html_source = browser.page_source
    browser.quit()

    return html_source

# FIXME: get urls from command line args
html = scrape_html(REDDIT_URL + "/r/abuse")
subreddit_soup = BeautifulSoup(html, 'html.parser')
post_urls = subreddit_soup.find_all("a", {"data-click-id": "body"})

for post_url in post_urls:
    html = scrape_html(REDDIT_URL + post_url["href"])
    post_soup = BeautifulSoup(html, 'html.parser')

    post_text = post_soup.find_all("div", {"data-click-id": "text"})
    post_msg = ""
    for elem in post_text:
        for s in elem.stripped_strings:
            post_msg += s
    print(post_msg)