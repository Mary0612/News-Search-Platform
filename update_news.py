import datetime
import sqlite3
from definition import get_news_one_website

con = sqlite3.connect('news_info.db')
cursor = con.cursor()
    
cursor.execute("SELECT * FROM url WHERE website = '聯合新聞網';")
items_udn = cursor.fetchall()
cursor.execute("SELECT * FROM url WHERE website = 'Yahoo新聞';")
items_yahoo = cursor.fetchall()
cursor.execute("SELECT * FROM url WHERE website = '中央社';")
items_cna = cursor.fetchall()
cursor.execute("SELECT * FROM url WHERE website = '自由時報';")
items_ltn = cursor.fetchall()
    
con.commit()
con.close()    
    
for items in [items_udn, items_yahoo, items_cna, items_ltn]:
    for item in items:
        d1 = datetime.datetime.now()
        print("[{}] Start to get news from {} - {}...".format(d1, item[0], item[2]))
        con = sqlite3.connect('news_info.db')
        cursor = con.cursor()
        try:
            get_news_one_website(item[0], item[1], item[3], cursor)
        except:
            print("Errors occur on " + str(item))
        con.commit()
        con.close()
        d2 = datetime.datetime.now()
        print("in {} on {} - {}.".format(str(d2-d1), item[0], item[2]))    