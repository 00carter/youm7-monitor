import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import logging
import os
import json


logging.basicConfig(level=logging.INFO)




def main():
    while True:
        url = f"https://www.youm7.com/home/?t={int(time.time())}"
        time.sleep(10)
        current_articles = []
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            r = response.text #Change to text
        except requests.exceptions.RequestException as e:
            logging.warning(f"Request failed: {e}")
            time.sleep(60)
            continue

        soup = BeautifulSoup(r, "lxml")
        articles = soup.find_all("div", class_="newsInfo")

        for article in articles:
            current_articles.append(
                {
                    "title": article.find("div", class_="label1").text.strip(),
                    "link": article.find("div", class_="label1").h3.a["href"].strip(),
                    "image": article.find("div", class_="image")
                    .a.img["data-src"]
                    .strip(),
                }
            )
        try:
            with open("memory.json", "r+", encoding="utf-8") as f:
                try:
                    saved_articles = json.load(f)
                except json.decoder.JSONDecodeError:
                    clear_file(f)
                    json.dump(current_articles, f, indent=2, ensure_ascii=False) #If file empty for some reason
                    continue

                if saved_articles == current_articles:
                    print("Monitoring..")
                    continue
                else:
                    new_articles = [
                        article
                        for article in current_articles
                        if article not in saved_articles
                    ]
                    clear_file(f)
                    json.dump(current_articles, f, indent=2, ensure_ascii=False)
                    display_new_articles(new_articles)
                    f.flush()

        except FileNotFoundError:
            check_memory(current_articles)
            continue

        


def clear_file(f):
    f.seek(0)
    f.truncate()


def check_memory(current_articles):
    if not os.path.exists("memory.json"):
        with open("memory.json", "w", encoding="utf-8") as f:
            json.dump(current_articles, f, indent=2, ensure_ascii=False)


def display_new_articles(new_articles: list) -> str:  # Removing later
    for article in new_articles:
        print(f"\n📰 Title: {article['title']}")
        print(f"🔗 Link: https://www.youm7.com/{article['link']}")
        print(f"🖼️  Image: {article['image']}\n")


main()