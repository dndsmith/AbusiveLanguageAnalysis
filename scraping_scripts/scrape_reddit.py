from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import pandas as pd
import argparse

REDDIT_URL = 'https://www.reddit.com/r/'

def scrape_html(url):
    browser = webdriver.Firefox()
    browser.get(url)
    html_source = browser.page_source
    browser.quit()

    return html_source

def main():
    # get subreddits from command line
    parser = argparse.ArgumentParser(description='Scrape posts on Reddit.')
    parser.add_argument('subreddits', type=str, nargs='+',
                        help='enter name of subreddit like so: wholesomememes')
    
    args = parser.parse_args()

    # create dataframe to store posts
    df = pd.DataFrame(columns=['Text', 'Subreddit'])

    # get posts from subreddits given on command line
    for sub in args.subreddits:
        html = scrape_html(REDDIT_URL + sub)
        subreddit_soup = BeautifulSoup(html, 'html.parser')
        post_urls = subreddit_soup.find_all("a", {"data-click-id": "body"})

        for post_url in post_urls:
            # fyi the href is being sliced to remove the preceding /r/
            html = scrape_html(REDDIT_URL + post_url['href'][post_url['href'].index('/r/')+len('/r/'):])
            post_soup = BeautifulSoup(html, 'html.parser')
            post_text = post_soup.find_all("div", {"data-click-id": "text"})
            post_msg = ""
            for elem in post_text:
                for s in elem.stripped_strings:
                    post_msg += s + " "
            df = df.append({'Text': post_msg, 'Subreddit': sub}, ignore_index=True)
    
    # write dataframe to csv
    df.to_csv('../data/' + '-'.join(args.subreddits) + '.csv', index=False)

if __name__ == "__main__":
    main()