import requests
from bs4 import BeautifulSoup
import json

html = requests.get("https://www.youm7.com/home").text
soup = BeautifulSoup(html, "lxml")
article_list = []
articles = soup.find_all("div", class_="newsInfo")

for article in articles:
    article_list.append(
        {
            "title": article.find("div", class_="label1").text.strip(),
            "link": article.find("div", class_="label1").h3.a["href"].strip(),
            "image": article.find("div", class_="image").a.img["data-src"].strip(),    
        }
    )
    

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(article_list, f, indent=2, ensure_ascii=False)