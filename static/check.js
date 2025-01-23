const radio_keyword = document.getElementById("keyword");
const text_keyword = document.getElementById("keyword-input");
const radio_category = document.getElementById("category");
const checkbox_category_group = document.getElementById("group-category");
const checkbox_category = checkbox_category_group.querySelectorAll("input[type = 'checkbox']");
const checkbox_website_group = document.getElementById("group-website");
const checkbox_website = checkbox_website_group.querySelectorAll("input[type = 'checkbox']");
const radio_default_time = document.getElementById("default-interval");
const radio_set_time = document.getElementById("set-interval");
const time_start = document.getElementById("interval-start");
const time_end = document.getElementById("interval-end");
const btn_submit = document.getElementById("submit");

function disable_effect(){
    if (radio_keyword.checked){
        text_keyword.disabled = false;
        checkbox_category.forEach(item => (item.disabled = true));
    }
    else if (radio_category.checked){
        text_keyword.disabled = true;
        checkbox_category.forEach(item => (item.disabled = false));
    }
    if (radio_default_time.checked){
        time_start.disabled = true;
        time_end.disabled = true;
    }
    else if (radio_set_time.checked){
        time_start.disabled = false;
        time_end.disabled = false;
    }
}

function check_condition(event){
    let message = ["請完成以下搜尋條件:"];
    
    // 未選擇查詢方式
    if (radio_keyword.checked == false && radio_category.checked == false) message.push("查詢方式:");
    
    // 選擇以關鍵字查詢但沒輸入關鍵字
    else if (radio_keyword.checked == true && text_keyword.value == "") message.push("輸入關鍵字");

    // 選擇以類型查詢但沒勾選類型
    else if (radio_category.checked == true){
        let cnt = 0;
        for (i = 0; i < checkbox_category.length; i++){
            if (checkbox_category[i].checked == true) cnt++;
        }
        if (cnt == 0) message.push("欲查詢的新聞類型");
    }
    
    // 關鍵字有問題
    if (text_keyword.value == ";" || text_keyword.value == " "){
        event.preventDefault();
        alert("請輸入有效關鍵字");
        return
    }
    
    // 未指定新聞網站
    let cnt_website = 0;
    for (i = 0; i < checkbox_website.length; i++){
        if (checkbox_website[i].checked == true) cnt_website++;
    }
    if (cnt_website == 0) message.push("欲指定的新聞網站");
    
    // 未指定日期區間
    if (radio_default_time.checked == false && radio_set_time.checked == false) message.push("指定日期區間");
    
    // 日期區間錯誤(end和start寫反)
    else if (radio_default_time.checked == false && time_start.value > time_end.value) message.push("日期區間請由小到大輸入");
    
    // 顯示alert
    if (message.length > 1){
        event.preventDefault();
        alert(message.join("\n"));
    }
}

radio_keyword.addEventListener('change', disable_effect);
radio_category.addEventListener('change', disable_effect);
radio_default_time.addEventListener('change', disable_effect);
radio_set_time.addEventListener('change', disable_effect);
btn_submit.addEventListener('click', check_condition);