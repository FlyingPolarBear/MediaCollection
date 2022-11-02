'''
Author: Derry
Date: 2022-05-26 17:24:57
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-05-26 21:49:56
Description: None
'''
import datetime
import time

import xlwt
from selenium import webdriver  # 用来驱动浏览器的
from selenium.webdriver import ActionChains  # 破解滑动验证码的时候用的 可以拖动图片
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import \
    expected_conditions as EC  # 和下面WebDriverWait一起用的
from selenium.webdriver.support.wait import WebDriverWait

workbook = xlwt.Workbook(encoding='utf-8')
main_sheet = workbook.add_sheet("统计")
line = 0
print("start")
arr = ["人民日报", "人民日报海外版", "新华社", "中央人民广播电台", "中央电视台", "求是", "解放军报", "光明日报", "经济日报", "中国日报",
       "科技日报", "人民政协报", "中国纪检监察报", "中国新闻网", "学习时报", "工人日报", "中国青年报", "中国妇女报", "农民日报", "法制日报"]
# arr = ["中国新闻网"]

current_time = datetime.datetime.now()
year = current_time.year
month = current_time.month


def handle_page(news_list, worksheet, name):
    print("now seeking "+name)
    global line
    for k in range(len(news_list)):
        item = news_list[k]
        print("***********"+item.text+"***********")
        publish_time = item.find_element_by_class_name("date").text
        title = item.find_elements_by_tag_name("a")[0].text
        link = item.find_elements_by_tag_name("a")[0].get_attribute("href")
        verified = name
        if str(year) in publish_time and str(month) in publish_time:
            if verified in title and "客户端" not in title:
                print("publish time="+publish_time)
                print("链接："+link + "  "+title)
                worksheet.write(line, 0, title)
                worksheet.write(line, 1, link)
                line = line+1
        else:
            return False
    return True


for i in range(len(arr)):
    main_sheet.write(0, i, arr[i])
    name = arr[i]
    driver = webdriver.Chrome(executable_path="./chromedriver")
    driver.maximize_window()
    driver.get("https://news.ustc.edu.cn/")
    worksheet = workbook.add_sheet(name)
    line = 0
    wait = WebDriverWait(driver, 10)
    input_tag = wait.until(EC.presence_of_element_located(
        (By.ID, "showkeycode249665")))
    input_tag.clear()
    # 3,在搜索框在输入要搜索的内容
    input_tag.send_keys(name)

    # 4,按键盘回车键
    input_tag.send_keys(Keys.ENTER)
    time.sleep(6)
    # windows = driver.window_handles
    # driver.switch_to.window(windows[0])
    news_list = driver.find_element_by_class_name(
        "info-list").find_elements_by_class_name("row")
    while handle_page(news_list, worksheet, name) is not False:
        print("************NEW TURN STARTS**********")
        next = None
        llist = driver.find_elements_by_class_name(
            "listFrame")[0].find_elements_by_tag_name("a")
        for i in range(len(llist)):
            if llist[i].text == "下一页":
                next = llist[i]
        if next != None:
            next.click()
            time.sleep(2)
            news_list = driver.find_element_by_class_name(
                "info-list").find_elements_by_class_name("row")
        else:
            break
    driver.quit()

month_time = current_time.strftime('%Y%m')
filename = f"中科大{month_time}各刊物情况.xls"
workbook.save(filename)
