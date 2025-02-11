'''
Author: Derry
Date: 2022-05-26 21:42:07
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2023-06-02 13:07:18
Description: None
'''

import zipfile
import shutil
import json
import os
import re

import requests
import retry
from bs4 import BeautifulSoup


@retry.retry(tries=3, delay=1)
def request_url(url,encoding = None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding if encoding is None else encoding
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def handle_nju_anomaly(text):
    import re
    text_list = text.split('{"releaseTime"')
    for i in range(len(text_list)):
        regex = '"content"[\s\S]*,"releasetime"'
        pattern = re.compile(regex)
        res = pattern.findall(text_list[i])
        if len(res) > 0:
            text_list[i] = text_list[i].replace(res[0], '"releasetime"')
    return '{"releaseTime"'.join(text_list)


def post_data(url, data):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    response = requests.post(url, data=data, headers=headers)
    response.encoding = response.apparent_encoding
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            res_data = json.loads(soup.text)
        except:
            text = handle_nju_anomaly(soup.text)
            res_data = json.loads(text)
    return res_data


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)
from rich import print as rprint

def zip_dir(dir_path, zip_file_name):
    zip_file = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            zip_file.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file), os.path.join(dir_path, '..')))
    zip_file.close()
    rprint(f"📚 Zipped [italic blue]{dir_path}[/italic blue] to [italic blue]{zip_file_name}[/italic blue]")
