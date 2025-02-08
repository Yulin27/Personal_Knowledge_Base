"""_summary_

This module contains the Scraper class which is used to scrape web pages.
"""

import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, type = "Static Page"):
        self.type = type


    def scrape_static(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1').text
        article_body = ' '.join([p.text for p in soup.find_all('p')])
        return title, article_body

    def scrape_dynamic(self, url):
        pass

    def scrape(self, url):
        if self.type == "Static Page":
            return self.scrape_static(url)
        else:
            return self.scrape_dynamic(url)
