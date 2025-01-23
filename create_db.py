import requests
import sqlite3
import urllib.parse
import bs4
from definition import get_content
from definition import category_info

con = sqlite3.connect('news_info.db')
cursor = con.cursor()
cursor.execute("CREATE TABLE url(website TEXT, category TEXT, subcategory TEXT, url TEXT UNIQUE);")

# udn
base_udn_url = "https://udn.com"
soup = get_content("https://udn.com/news/index")
items = soup.find_all("a", "navigation-list")
for i in range(len(category_info)):
    url_sub_list = [(urllib.parse.urljoin(base_udn_url, item.get("href")), item.text) for item in items if item.text in category_info[i]["subcategory"]]
    for (url, sub) in url_sub_list:
        if base_udn_url in url:
            cursor.execute("INSERT INTO url(website, category, subcategory, url) VALUES (?, ?, ?, ?);", ('聯合新聞網', category_info[i]['name'], sub, url))

# yahoo
base_yahoo_url = "https://tw.news.yahoo.com/"
soup = get_content(base_yahoo_url)
items = soup.find_all("a", "rapid-noclick-resp")
for i in range(len(category_info)):
    url_sub_list = [(item.get("href"), item.text.replace(" ", "")) for item in items if item.text.replace(" ", "") in category_info[i]["subcategory"]]
    for (url, sub) in url_sub_list:
        if base_yahoo_url in url:
            cursor.execute("INSERT INTO url(website, category, subcategory, url) VALUES (?, ?, ?, ?);", ('Yahoo新聞', category_info[i]['name'], sub, url))

# cna
base_cna_url = "https://www.cna.com.tw/"
soup = get_content(base_cna_url)
items = soup.find("ul", "main-menu").find_all("a", "first-level")
for i in range(len(category_info)):
    url_sub_list = [(urllib.parse.urljoin(base_cna_url, item.get("href")), item.text) for item in items if item.text in category_info[i]["subcategory"]]
    for (url, sub) in url_sub_list:
        if base_cna_url in url:
            cursor.execute("INSERT INTO url(website, category, subcategory, url) VALUES (?, ?, ?, ?);", ('中央社', category_info[i]['name'], sub, url))

# ltn
base_ltn_url = "https://news.ltn.com.tw/list/breakingnews"
soup = get_content(base_ltn_url)
items = soup.find("div", "useMobi").find_all("a")
for i in range(len(category_info)):
    url_sub_list = [(item.get("href"), item.text) for item in items if item.text in category_info[i]["subcategory"]]
    for (url, sub) in url_sub_list:
        if base_ltn_url in url:
            cursor.execute("INSERT INTO url(website, category, subcategory, url) VALUES (?, ?, ?, ?);", ('自由時報', category_info[i]['name'], sub, url))

print("Complete the creation of table \"url\".")
            
cursor.execute("CREATE TABLE news(title TEXT, url TEXT UNIQUE, website TEXT, category TEXT, date DATETIME, content TEXT);")
print("Complete the creation of table \"news\".")

con.commit()
con.close()