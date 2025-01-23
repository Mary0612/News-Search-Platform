from flask import Flask, render_template, request, redirect, url_for
import datetime
import sqlite3

app = Flask(__name__)
condition = dict()

# result formation
def result_format():
    # result_1
    if condition["search_method"] == "keyword":
        condition["result_1"] = "關鍵字：" + condition["keyword"]
    else:
        category_str = []
        if "social" in condition["method"]:
            category_str.append("社會")
        if "international" in condition["method"]:
            category_str.append("國際與政治")
        if "life" in condition["method"]:
            category_str.append("生活")
        if "sports" in condition["method"]:
            category_str.append("運動")
        if "entertainment" in condition["method"]:
            category_str.append("娛樂")
        if "finance" in condition["method"]:
            category_str.append("產業與金融")
        condition["result_1_str"] = category_str
        condition["result_1"] = "新聞類型：" + "、".join(category_str)
    # result_2
    website_str = []
    if "udn" in condition["search_website"]:
        website_str.append("聯合新聞網")
    if "yahoo" in condition["search_website"]:
        website_str.append("Yahoo新聞")
    if "cna" in condition["search_website"]:
        website_str.append("中央社")
    if "ltn" in condition["search_website"]:
        website_str.append("自由時報")
    condition["result_2_str"] = website_str
    condition["result_2"] = "新聞來源：" + "、".join(website_str)
    # result_3
    if condition["search_date"] == "default-interval":
        condition["date_start"] = str(datetime.date.today() - datetime.timedelta(days = 7))
        condition["date_end"] = str(datetime.date.today() + datetime.timedelta(days = 1))
    if condition["date_start"] == condition["date_end"]:
        condition["result_3"] = "日期：" + condition["date_start"]
    else:
        condition["result_3"] = "日期：" + condition["date_start"] + " 至 " + condition["date_end"]
        
def get_info(condition):
    # 查詢方式
    if condition["search_method"] == "keyword":
        query_method = "%" + condition["keyword"] + "%"
    else:
        query_method_list = [("category = \'" + item + "\'") for item in condition["result_1_str"]]
        query_method = "(" + " OR ".join(query_method_list) + ")"
    # 資料來源
    query_website_list = [("website = \'" + item + "\'") for item in condition["result_2_str"]]
    query_website = "(" + " OR ".join(query_website_list) + ")"
    # 日期區間(d_end有多加一天->包含d_end當天)
    if condition["search_date"] == "default-interval":
        d_start = str(datetime.date.today() - datetime.timedelta(days = 7)).replace("-", "/")
        d_end = str(datetime.date.today() + datetime.timedelta(days = 1)).replace("-", "/") 
    else:
        d_start = condition["date_start"].replace("-", "/")
        d_end_num_list = [int(item) for item in condition["date_end"].split("-")]
        d_end = datetime.date(d_end_num_list[0], d_end_num_list[1], d_end_num_list[2]) + datetime.timedelta(days = 1)
        d_end = str(d_end).replace("-", "/")
    query_date = "(date > \'" + d_start + "\' AND date < \'" + d_end + "\')"
    
    con = sqlite3.connect('news_info.db')
    cursor = con.cursor()
    if condition["search_method"] == "keyword":
        query = "SELECT url, title, date, category, website FROM news WHERE content LIKE ? AND " + query_website + " AND " + query_date + " ORDER BY date DESC;"
        cursor.execute(query, (query_method, ))
    else:
        query = "SELECT url, title, date, category, website FROM news WHERE " + query_method + " AND " + query_website + " AND " + query_date + " ORDER BY date DESC;"
        cursor.execute(query)
    items = cursor.fetchall()
        
    result_data = []
    for item in items:
        temp_dict = {
            "url": item[0],
            "title": item[1],
            "date": item[2],
            "category": item[3],
            "website": item[4]
        }
        result_data.append(temp_dict)
    con.commit()
    con.close()
    
    return result_data

@app.route('/search', methods = ['POST', 'GET'])
def search():
    date_oneweek = datetime.date.today() - datetime.timedelta(days = 7)
    date_today = datetime.date.today()
    return render_template('search.html', date = [date_oneweek, date_today])

@app.route('/submit', methods = ['POST', 'GET'])
def submit():
    condition["search_method"] = request.args.get('search-method')
    condition["keyword"] = request.args.get('keyword')
    condition["method"] = request.args.getlist('method')
    condition["search_website"] = request.args.getlist('search-website')
    condition["search_date"] = request.args.get('search-date')
    condition["date_start"] = request.args.get('date-start')
    condition["date_end"] = request.args.get('date-end')
    return redirect(url_for('result'))

@app.route('/result')
def result():
    result_format()
    result_data = get_info(condition)
    return render_template('result.html', condition = condition, result_data = result_data)

if __name__ == '__main__':
    app.run(debug = True)
