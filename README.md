# 新聞資訊整合平台

## 專案描述

本專案運用爬蟲技術及資料庫管理，整合聯合新聞網、Yahoo新聞、中央社及自由時報等四家網站的新聞內容並建立一個新聞查詢平台。使用者可透過網頁介面輸入搜尋條件，快速獲取符合需求的新聞資訊，提供多元且便利的瀏覽體驗。

## 程式語言版本

Python 3.10.2

## 安裝指南

本專案使用到以下套件，若尚未安裝可使用`pip install <package_name>`安裝：

* fake_useragent

* requests

* bs4

* lxml

* selenium （另需安裝 chromedirver ，並將`definition.py`中`driver_path`改為 chromedriver 的路徑）

* python-dateutil

* flask

## 功能

* `definition.py`

    負責引入套件、定義變數和函式，詳細功能說明如下：

    | 變數或函式 | 說明 |
    | :--: | :-- |
    | 定義 selenium 相關參數 | 包含 chromedriver 路徑、開啟無頭模式並隱藏多餘 log 資訊等 |
    | 定義 category_info | 本專案將新聞類型分成「社會」、「國際與政治」、「生活」、「運動」、「娛樂」及「產業與金融」等六個類型，並將子類型（各家新聞網站上的類別名稱）與對應到的類型紀錄在`category_info`中 |
    | date_transform | 將Yahoo新聞上的日期轉換成指定格式 |
    | find_news_list | 針對四間來源網站的新聞總覽頁面，利用 selenium 模擬互動並獲取所有新聞在總覽頁面的 HTML 內容 |
    | get_content | 使用 requests.get 搭配隨機生成的 User-Agent，獲取目標網站的 HTML 內容並回傳 lxml 解析後的結果 |
    | get_content_selenium | 使用 selenium 獲取目標網站的 HTML 內容並回傳 lxml 解析後的結果 |
    | get_news_info | 利用 lxml 解析後的結果，提取出新聞標題、日期及內容等資訊並回傳。若無法成功提取資訊則會拋出例外 |
    | update_db | 將新聞資訊新增到資料庫中的`news`，若該新聞網址已存在，就會更新標題、日期及內容 |
    | get_news_one_website | 利用`find_news_list`、`get_content`、`get_content_selenium`、`get_news_info`及`update_db`等函式，從一個新聞總覽頁面取得所有新聞的資訊，並存入或更新資料庫 |
    | check_result | 輸出資料庫中最舊和最新的新聞標題及日期 |

* `create_db.py`

    建立一個資料庫（`news_info.db`）及兩個資料表（`url`和`news`），並在`url`中存入`category_info`中各個子類型在不同新聞來源網站的新聞總覽網址。`url`及`news`的欄位說明如下：
    
    * `url`：儲存各個新聞來源網站上不同類型的新聞總覽頁面資訊
    
        | 欄位名稱 | 說明 |
        | :--: | :--: |
        | website | 來源網站，包含聯合新聞網、Yahoo新聞、中央社及自由時報 |
        | category | 新聞類型，包含社會、國際與政治、生活、運動、娛樂及產業與金融 |
        | subcategory | 子類型名稱，如：全球、兩岸、國際、政治等 |
        | url | 新聞總覽頁面的網址 |
        
    * `news`：儲存每則新聞的資訊
        
        | 欄位名稱 | 說明 |
        | :--: | :--: |
        | title | 新聞標題 |
        | url | 新聞網址連結 |
        | website | 來源網站 |
        | category | 新聞類型 |
        | date | 新聞發布或更新日期 |
        | content | 新聞內容 |

* `update_news.py`

    至`url`資料表中所有新聞總覽頁面爬取各類型的新聞資訊，並更新或新增到`news`資料表中。
    
* `delete_news.py`

    使用者輸入日期並確認後，會刪除資料庫中該日期（不含當天）之前的所有新聞資訊。

* `render.py`

    負責處理網頁的切換與使用者查詢頁面、資料庫操作及結果顯示頁面之間的資料交換。相關的 HTML 及 JavaScript 檔案也放在`template`和`static`的資料夾中。

## 啟動方法

**1. 建立資料庫（只需建立一次）**

```
python create_db.py
```

**2. 資料庫更新（需持續更新）**

執行`create_db.py`只會建立空白的`news`資料表，新增與刪除新聞資訊需另外執行以下程式：

* 新增新聞

```
python update_news.py
```

* 刪除新聞

```
python delete_news.py
```

執行時系統會提醒使用者要輸入日期（格式：西元年/月/日），並輸入「yes」確認，才會開始刪除資料。

**3. 使用網頁介面搜尋新聞（每次開啟網頁時皆需執行）**

```
python render.py
```

執行程式並輸入網址「[http://127.0.0.1:5000/search](http://127.0.0.1:5000/search)」後即可進入查詢介面。輸入關鍵字或新聞類型、來源網站、日期等搜尋條件後，即可獲得符合條件的新聞資訊，並可透過新聞標題的超連結直接開啟該新聞網頁。
 
## 特別說明

本專案針對四間來源網站上最多新聞使用的格式進行爬蟲，因此少數特殊格式或連接到其他網站的新聞不會被放入資料庫或顯示在結果列中。

