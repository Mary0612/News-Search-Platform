import urllib.parse
import time
import re
import datetime
import dateutil
from fake_useragent import UserAgent
import requests
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import sqlite3

driver_path = 'your/path/to/chromedriver.exe'
service = Service(driver_path)
options = Options()
options.add_argument("--headless")
options.add_argument("--log-level=3")
PAGE_NUM = 100

base_udn_url = "https://udn.com"
base_yahoo_url = "https://tw.news.yahoo.com/"
base_cna_url = "https://www.cna.com.tw/"
base_ltn_url = "https://news.ltn.com.tw/list/breakingnews"

category_info = []
category_info.append({"name": "社會", "subcategory": ["社會", "地方", "社會地方"]})
category_info.append({"name": "國際與政治", "subcategory": ["全球", "兩岸", "國際", "政治"]})
category_info.append({"name": "生活", "subcategory": ["生活", "旅遊", "品味", "健康", "玩樂", "遊戲3C"]})
category_info.append({"name": "運動", "subcategory": ["運動"]})
category_info.append({"name": "娛樂", "subcategory": ["娛樂", "娛樂影劇"]})
category_info.append({"name": "產業與金融", "subcategory": ["產經", "股市", "財經", "證券"]})

def date_transform(date_str):
    date_num = re.sub('[^0-9]', ' ', date_str)
    date_num_list = date_num.split(" ")
    if "下午" in date_str:
        date_str = date_num_list[0] + '/' + date_num_list[1] + '/' + date_num_list[2] + " " + str((int(date_num_list[-2]) % 12) + 12) + ":" + date_num_list[-1]
    elif "上午" in date_str:
        date_str = date_num_list[0] + '/' + date_num_list[1] + '/' + date_num_list[2] + " " + str(int(date_num_list[-2]) % 12) + ":" + date_num_list[-1]
    else:
        date_str = date_num_list[0] + '/' + date_num_list[1] + '/' + date_num_list[2]
    return date_str


def find_news_list(page_url, website):
    try:
        driver = webdriver.Chrome(service = service, options = options)
        driver.get(page_url)
        if website == "聯合新聞網":
            for i in range(PAGE_NUM):
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[class="btn btn-ripple btn-more btn-more--news"]')))
                    more_btn = driver.find_element(By.CSS_SELECTOR, 'button[class="btn btn-ripple btn-more btn-more--news"]')
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", more_btn)
                    more_btn.click()
                    time.sleep(1)
                except:
                    break
            html = driver.page_source
            soup = bs4.BeautifulSoup(html, "lxml")
            articles = soup.find('section', "thumb-news more-news thumb-news--big context-box").find_all('div', "story-list__text")
        elif website == "Yahoo新聞":
            for i in range(PAGE_NUM):
                driver.execute_script("window.scrollBy(0, 1500);")
                time.sleep(1)
            html = driver.page_source
            soup = bs4.BeautifulSoup(html, "lxml")
            articles = soup.find_all("h3")
        elif website == "中央社":
            for i in range(PAGE_NUM):
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[id="SiteContent_uiViewMoreBtn_Style3"]')))
                    more_btn = driver.find_element(By.CSS_SELECTOR, 'a[id="SiteContent_uiViewMoreBtn_Style3"]')
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", more_btn)
                    more_btn.click()
                    time.sleep(1)
                except:
                    break
            html = driver.page_source
            soup = bs4.BeautifulSoup(html, "lxml")
            articles = soup.find('div', "statement").find_all('li')
        else:
            for i in range(PAGE_NUM):
                driver.execute_script("window.scrollBy(0, 1500);")
                time.sleep(1)
            html = driver.page_source
            soup = bs4.BeautifulSoup(html, "lxml")
            articles = soup.find('div', {"data-desc": "新聞列表"}).find_all('li')
        return articles
    except:
        raise Exception("Unable to get news list.")
    finally:
        driver.close()
    
    
def get_content(url):
    time.sleep(1.5)
    user_agent = UserAgent()
    response = requests.get(url, headers = {"user-agent": user_agent.random})
    soup = bs4.BeautifulSoup(response.text, "lxml")
    return soup

def get_content_selenium(url):
    try:
        driver = webdriver.Chrome(service = service, options=options)
        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, "lxml")
        return soup
    except:
        pass
    finally:
        driver.close()
        
def get_news_info(website, soup_news):
    if website == "聯合新聞網":
        title = soup_news.find('h1').text
        date = soup_news.find('time', "article-content__time").text
        date = dateutil.parser.parse(date).strftime("%Y/%m/%d %H:%M")
        paragraph = soup_news.find('section', "article-content__editor").find_all('p', recursive = False)
    elif website == "Yahoo新聞":
        title = soup_news.find('h1').text
        date = soup_news.find("time").text
        date = date_transform(date)
        if len(date) > 10:
            date = dateutil.parser.parse(date).strftime("%Y/%m/%d %H:%M")
        else:
            date = dateutil.parser.parse(date).strftime("%Y/%m/%d")
        paragraph = soup_news.find('div', {"class": "caas-body"}).find_all('p')
    elif website == "中央社":
        title = soup_news.find('h1').text
        date = soup_news.find('div', "updatetime").find_all("span")[0].text
        date = dateutil.parser.parse(date).strftime("%Y/%m/%d %H:%M")
        paragraph = soup_news.find('div', "paragraph").find_all('p')
    else:
        title = soup_news.find('h1').text
        date = soup_news.find('span', "time").text.replace("\n    ", "")
        date = dateutil.parser.parse(date).strftime("%Y/%m/%d %H:%M")
        paragraph = soup_news.find_all('div', {"data-desc": "內容頁"})[0].find_all('p', {"class": ""}, recursive = False)
    
    content = ""
    if website == "聯合新聞網" or website == "Yahoo新聞":
        for text in paragraph:
            link = text.find('a')
            if link == None or link.get("href") == None or "tag" in link.get("href"):
                content += text.text
            else:
                new_text = re.sub(r'<a.*</a>', "", str(text))
                soup_new_text = bs4.BeautifulSoup(new_text, "lxml")
                content += soup_new_text.text
    else:
        for text in paragraph:
            content += text.text
        
    if title == "" or date == "":
        raise Exception("Got empty title or date.")
    return (title, date, content)

def update_db(cursor, title, url, website, category, date, content):
    cursor.execute("SELECT * FROM news WHERE url = ?;", (url, ))
    if cursor.fetchall() == []:
        cursor.execute("INSERT INTO news(title, url, website, category, date, content) VALUES (?, ?, ?, ?, ?, ?);", (title, url, website, category, date, content))
    else:
        cursor.execute("UPDATE news SET title = ?, date = ?, content = ? WHERE url = ?;", (title, date, content, url))
        
def get_news_one_website(website, category, page_url, cursor):
    
    # get the html contents of news list
    for i in range(5):
        try:
            articles = find_news_list(page_url, website)
            break
        except Exception as e:
            if i == 4:
                raise Exception(str(e))
            else:
                pass
    print("Got news list.")
    
    # get information of each piece of news
    news_num = 0
    for article in articles:
        try:
            # get url
            if website == "聯合新聞網":
                url = urllib.parse.urljoin(base_udn_url, article.find('a').get("href"))
                if "124300" in url: # 經濟日報
                    continue
            elif website == "Yahoo新聞":
                url = urllib.parse.urljoin(base_yahoo_url, article.find('a').get("href"))
                if "tw.tv.yahoo.com" in url or "tw.sports.yahoo.com" in url or "autos.yahoo.com.tw" in url:
                    continue
            elif website == "中央社":
                url = urllib.parse.urljoin(base_cna_url, article.find('a').get("href"))
                if "netzero" in url:
                    continue
            else:
                url = article.find_all('a')[1].get("href")
            
            # get title, date, content
            try:
                soup_news = get_content(url)
                (title, date, content) = get_news_info(website, soup_news)
            except:
                for i in range(3):
                    try:
                        soup_news = get_content_selenium(url)
                        (title, date, content) = get_news_info(website, soup_news)
                        break
                    except Exception as e:
                        if i == 2:
                            raise Exception(str(e))
                        else:
                            pass
        except:
            # print(url)  # the url which data can't be retrived from
            continue
            
        # update database
        update_db(cursor, title, url, website, category, date, content)
        news_num += 1
        if news_num > 501:
            break
            
    print("Got {} news articles ".format(str(news_num)), end = "")
    
def check_result():
    con = sqlite3.connect('news_info.db')
    cursor = con.cursor()
    
    cursor.execute("SELECT date, title FROM news WHERE date = (SELECT MIN(date) FROM news);")
    first_data = cursor.fetchall()
    cursor.execute("SELECT date, title FROM news WHERE date = (SELECT MAX(date) FROM news);")
    last_data = cursor.fetchall()

    print("The first piece of data in the database is \"{}\".".format(" ".join([first_data[0][0], first_data[0][1]])))
    print("The last piece of data in the database is \"{}\".".format(" ".join([last_data[0][0], last_data[0][1]])))
    
    con.commit()
    con.close()  