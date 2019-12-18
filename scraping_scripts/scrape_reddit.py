from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
#import requests
import csv
#import time ### check if this is actually needed

# make into command line args
url = "https://www.reddit.com/r/abuse"

browser = webdriver.Firefox()
browser.get(url)
html_source = browser.page_source
browser.quit()

subredditSoup = BeautifulSoup(html_source, 'html.parser')

posts = subredditSoup.find_all("a", {"data-click-id": "body"})

i=0
for post in posts:
    print(i)
    print(post)
    i += 1