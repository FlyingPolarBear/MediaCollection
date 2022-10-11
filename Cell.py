'''
Author: Derry
Date: 2022-08-07 22:45:57
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-10-07 20:08:22
Description: None
'''
import datetime
import hashlib
import http.client
import json
import os
import smtplib
import time
import urllib.parse
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib import request

import requests
from bs4 import BeautifulSoup
from translate import Translator


class EmailSender:
    """
    邮件发送模块
    """

    def __init__(self, msg_to='derrylv@qq.com', msg_from='derrylv@qq.com', pwd="lcbejwsmaajeheeh"):
        self.smtp = "smtp.qq.com"
        self.msg_to = msg_to
        self.msg_from = msg_from
        self.pwd = pwd

    def send(self, content, subject="程序出错啦 /(ㄒoㄒ)/~~"):
        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"] = self.msg_from
        msg["To"] = self.msg_to
        text = MIMEText(content, "html", "utf-8")
        msg.attach(text)
        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.smtp)
            smtp.login(self.msg_from, self.pwd)
            smtp.sendmail(self.msg_from, self.msg_to, msg.as_string())
            print("Successfully sending email to", self.msg_to)
        except:
            print("Failed to send email to", self.msg_to)
        finally:
            smtp.quit()


class Cell:
    def __init__(self):
        self.base_url = "https://www.sciencedirect.com/journal/molecular-cell/articles-in-press"

    def _nextpage(self, i):
        return f"https://www.sciencedirect.com/journal/molecular-cell/articles-in-press?page={i}"

    def load_main_webpage(self, url, file_path="tmp/articles-in-press"):
        if os.path.exists(file_path):
            os.remove(file_path)
        os.system(f'wget -U "Mozilla/5.0" -O {file_path} "{self.base_url}"')
        with open(file_path, "r") as f:
            for line in f:
                if line.startswith("</style>"):
                    html = line.lstrip("</style>").rstrip("</div>\n")
                    break
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def extract_date_info(self, raw_date):
        raw_date = raw_date.lstrip(
            "In Press, Corrected Proof, Available online ")
        date = datetime.datetime.strptime(raw_date, '%d %B %Y')
        return date

    def get_info(self, time_interval=None):
        if time_interval is None:  # 默认取最近七天的文章
            self.end_date = datetime.datetime.today()
            self.start_date = datetime.datetime.now() - datetime.timedelta(days=7)
        else:  # 指定起止日期
            self.start_date, self.end_date = time_interval
            self.start_date = datetime.datetime.strptime(
                self.start_date, '%Y-%m-%d')
            self.end_date = datetime.datetime.strptime(
                self.end_date, '%Y-%m-%d')

        i = 0
        while True:
            i += 1
            soup = self.load_main_webpage(self._nextpage(i))
            info_list = soup.find_all(
                'dl', class_='js-article article-content')
            paper_list = []
            for paper_soup in info_list:
                paper = {}
                title_element = paper_soup.find(
                    'a', class_='anchor article-content-title u-margin-xs-top u-margin-s-bottom anchor-default')
                relative_url = title_element.get('href')
                paper['title'] = title_element.get_text()
                paper['url'] = f"https://www.sciencedirect.com{relative_url}"
                paper['author'] = paper_soup.find(
                    'dd', class_='js-article-author-list u-clr-grey8 text-s').get_text()
                raw_date = paper_soup.find(
                    'dd', class_='u-clr-grey8 u-text-italic text-s js-article-item-aip-date').get_text()
                paper['date'] = self.extract_date_info(raw_date)
                title_translated = translate(paper['title'])
                paper['title'] += f"++++({title_translated})"
                if paper['date'] > self.start_date and paper['date'] < self.end_date:
                    paper['date'] = paper['date'].strftime('%Y-%m-%d')
                    paper_list.append(paper)
                else:
                    return paper_list

    def send_info(self, paper_list):
        from HTMLTable import HTMLTable
        date_interval = f"{self.start_date.strftime('%Y-%m-%d')} - {self.end_date.strftime('%Y-%m-%d')}"
        table = HTMLTable(
            caption=f"Molecular Cell Weekly Update ({date_interval})++++https://www.sciencedirect.com/journal/molecular-cell/articles-in-press")
        table.append_header_rows([["Title", "Date", "URL"]])
        for paper in paper_list:
            table.append_data_rows(
                [[paper['title'], paper['date'], paper['url']]])
        # 标题样式
        table.caption.set_style({
            'font-size': '20px',
            'font-weight': 'bold',
        })
        # 表格样式，即<table>标签样式
        table.set_style({
            'border-collapse': 'collapse',
            'word-break': 'keep-all',
            'white-space': 'nowrap',
            'font-size': '14px',
        })
        # 统一设置所有单元格样式，<td>或<th>
        table.set_cell_style({
            'border-color': '#000',
            'border-width': '1px',
            'border-style': 'solid',
            'padding': '5px',
        })
        # 表头样式
        table.set_header_row_style({
            'color': '#fff',
            'background-color': '#48a6fb',
            'font-size': '18px',
        })
        # 覆盖表头单元格字体样式
        table.set_header_cell_style({
            'padding': '15px',
        })
        html = table.to_html()
        html = html.replace("++++", "<br>")
        with open("tmp/res.html", "w") as f:
            f.write(html)
        sender = EmailSender(msg_to="411473510@qq.com")
        sender.send(content=html, subject=f"Molecular Cell Weekly Update ({date_interval})")


class BaiduTranslate:
    def __init__(self, query):
        import random
        self.params = {}
        self.q = query
        self.fromLang = 'en'
        self.toLang = 'zh'
        self.appid = '20220808001299064'
        self.salt = str(random.randint(0, 10**10-1)).zfill(10)  # 随机码
        self.key = 'Wubwgr8ieMIZqxwH3hVy'  # 密钥

    def translate_api(self):
        self.sign = self.appid = self.q+self.salt+self.key
        md5 = hashlib.md5()
        md5.update(self.sign.encode('utf-8'))
        self.sign = md5.hexdigest()
        myurl = "/api/trans/vip/translate"
        myurl = f"{myurl}?q={self.q}&from={self.fromLang}&to={self.toLang}&appid={self.appid}&salt={self.salt}&sign={self.sign}"
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            # response是HTTPResponse对象
            response = httpClient.getresponse()
            result_all = response.read().decode("utf-8")
            result = json.loads(result_all)
            trans_result = result['trans_result'][0]['dst']
        except Exception as e:
            print(e)
        finally:
            if httpClient:
                httpClient.close()
        return trans_result


def translate(content):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom=http://fanyi.youdao.com/'
    data = {  # 表单数据
        'i': content,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_CLICKBUTTION',
        'typoResult': 'false'
    }
    data = urllib.parse.urlencode(data).encode('utf-8')  # 对POST数据进行编码
    response = urllib.request.urlopen(url, data)  # 发出POST请求并获取HTTP响应
    html = response.read().decode('utf-8')  # 获取网页内容，并进行解码解码
    target = json.loads(html)  # json解析
    return target['translateResult'][0][0]['tgt']


def CellWeekly(immed=True):
    current_time = datetime.datetime.now()
    print(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')}\t脚本开始运行")
    if immed:
        cell = Cell()
        paper_list = cell.get_info()
        cell.send_info(paper_list)
    next_week_time = current_time + datetime.timedelta(days=(4-current_time.weekday())%7)
    next_week_time = next_week_time.replace(hour=16, minute=0, second=0)
    if next_week_time < current_time:
        next_week_time += datetime.timedelta(days=7)
    sleep_time = (next_week_time - current_time).total_seconds()
    print(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')}\t下次唤醒时间：{next_week_time.strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(sleep_time)
    while True:
        current_time = datetime.datetime.now()
        cell = Cell()
        paper_list = cell.get_info()
        cell.send_info(paper_list)
        next_week_time = current_time + datetime.timedelta(days=7)
        next_week_time = next_week_time.replace(hour=20, minute=0, second=0)
        sleep_time = (next_week_time - current_time).total_seconds()
        print(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')}\t下次唤醒时间：{next_week_time.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(sleep_time)

if __name__ == "__main__":
    CellWeekly(immed=False)
    # cell = Cell()
    # paper_list = cell.get_info()
    # cell.send_info(paper_list)
