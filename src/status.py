import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.INFO)

url = "https://www.youm7.com/home"


def main():
    check_memory()

    articles = []
    load(articles)

    while True:
        r = requests.get(url).text
        soup = BeautifulSoup(r, "lxml")
        html = soup.find("div", id="mainNews").prettify()


        with open("memory.html", "r+", encoding="utf-8") as f:

            if f.read() != html:
                logging.warning("Something Changed!")  # Debug

                clear_file(f)
                f.write(html)
                f.flush()

                load(articles)

                print(
                    f"📰 New! \n Title: {articles[0]["title"]}\n Link: https://www.youm7.com{articles[0]["link"]}\n Date: {datetime.now()}\n"
                )

        time.sleep(10)


def clear_file(f):
    f.seek(0)
    f.truncate()
    logging.info("File Cleared!")  # Debug


def load(articles):
    articles.clear()

    with open("memory.html", "r", encoding="utf-8") as f:
        soup_memory = BeautifulSoup(f.read(), "lxml")
        articles_html = soup_memory.find_all("div", class_="label1")

    for article in articles_html:
        title = article.a.text.strip()
        link = article.a["href"].strip()
        articles.append({"title": title, "link": link})

    logging.info("Articles Loaded!")  # Debug


def check_memory():
    if not os.path.exists("memory.html"):
        r = requests.get(url).text
        soup = BeautifulSoup(r, "lxml")
        html = soup.find("div", id="mainNews").prettify()
        with open("memory.html", "w", encoding="utf-8") as f:
            f.write(html)


main()
