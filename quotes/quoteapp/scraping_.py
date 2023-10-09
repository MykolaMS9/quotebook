import time

import requests
from bs4 import BeautifulSoup

base_url = 'https://quotes.toscrape.com'  # 1 - 10
quotes_url = f"{base_url}/page/"

quoters = []
authors = []


def get_urls():
    for page_number in range(1, 11):  # 11
        yield f"{quotes_url}{page_number}/"


def spider(url):
    time.sleep(0.1)
    print(f'Scraping... : {url}')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    contents = soup.find_all('div', class_="quote")
    for content in contents:
        quote_dict = {}
        tags = content.find_all('a', class_="tag")
        tags_list = []
        for tag in tags:
            tags_list.append(tag.text)
        quote_dict.update({"tags": tags_list})
        quote_dict.update({"author": content.find('small', class_="author").text.replace('-', ' ')})
        quote_dict.update({"quote": content.find('span', class_="text").text})
        author_url = content.select("span a")[0].get('href')
        quoters.append(quote_dict)

        time.sleep(0.01)
        author_response = requests.get(f"{base_url}{author_url}")
        author_soup = BeautifulSoup(author_response.text, 'html.parser')
        author_dict = {}
        author_dict.update({'fullname': author_soup.find('h3', class_="author-title").text.replace('-', ' ')})
        author_dict.update({'born_date': author_soup.find('span', class_="author-born-date").text})
        author_dict.update({'born_location': author_soup.find('span', class_="author-born-location").text})
        author_dict.update({'description': author_soup.find('div', class_="author-description").text.strip()})
        if author_dict not in authors:
            authors.append(author_dict)
