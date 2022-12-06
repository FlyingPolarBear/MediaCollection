'''
Author: Derry
Date: 2022-12-05 20:32:16
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-12-05 20:52:58
Description: None
'''
import hashlib
import http.client
import json
import urllib.parse
import urllib.request

from googletrans import Translator
from retry import retry


class GoogleTranslate:
    def __init__(self):
        self.translator = Translator(service_urls=['translate.google.com.hk'])

    @retry(tries=3, delay=1)
    def translate_zh2en(self, text):
        return self.translator.translate(text, dest='en').text

    @retry(tries=3, delay=1)
    def translate_en2zh(self, text):
        return self.translator.translate(text, dest='zh-cn').text


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


if __name__ == "__main__":
    t = GoogleTranslate()
    print(t.translate_zh2en("你好"))
    print(t.translate_en2zh("hello"))
