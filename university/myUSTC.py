'''
Author: Derry
Date: 2022-06-08 16:06:00
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2023-08-01 11:55:52
Description: 中国科大新闻网爬虫
'''
import re

from university.NewsInfo import NewsInfo
from university.utils import request_url


class USTC(NewsInfo):
    def __init__(self,max_num=442) -> None:
        super().__init__()
        self.univ_name = '中国科大'
        self.base_url = "http://news.ustc.edu.cn/"
        self.max_num = max_num  # 总页数+1（第二页+2）

    def _nextpage(self, i):  # ! 注意这里的i的变化
        if i == 1:
            url = "http://news.ustc.edu.cn/mtgz.htm"
        else:
            url = f"http://news.ustc.edu.cn/mtgz/{self.max_num-i}.htm"
        return url

    def _time_parser(self, news_time):
        news_time = news_time.strip()
        year = news_time[:4]
        month = news_time[5:7]
        day = news_time[8:10]
        return year+'-'+month+'-'+day

    def _title_parser(self, title):
        return title.strip().replace('\u200b', '')

    def _media_parser(self, title):
        pattern1 = re.compile(r'【(.*?)】')
        pattern2 = re.compile(r'《(.*?)》')
        pattern3 = re.compile(r'】(.*?)｜')
        pattern4 = re.compile(r'】(.*?)丨')
        media1 = re.findall(pattern1, title)
        media2 = re.findall(pattern2, title)
        media3 = re.findall(pattern3, title)
        media4 = re.findall(pattern4, title)
        if len(media1) and media1[0] != "牢记嘱托建新功":
            return media1[0]
        else:
            for media in [media2, media3, media4]:
                if len(media):
                    return media[0]
            return ''

    def get_news(self, order_years=[2023], order_months=[5]):
        self.outfile_name = self._get_out_name(
            self.univ_name, order_years[0], order_months)
        data = []
        i = 0
        while True:
            i += 1
            soup = request_url(self._nextpage(i))
            news_list = soup.find_all('a', class_='col-sm-9 col-xs-12')

            for news in news_list:
                news_url = self.base_url+news.get('href')
                news_data = {'url': news_url}
                news_soup = request_url(news_url)

                news_time = news_soup.find_all(
                    'div', class_='date')[0].text
                news_data['time'] = self._time_parser(news_time)
                news_title = news_soup.find_all(
                    'div', class_='article-title person-title')[0].text
                news_data['title'] = self._title_parser(news_title)
                news_data['media'] = self._media_parser(news_data['title'])

                year = int(news_data['time'][:4])
                month = int(news_data['time'][5:7])
                if year not in order_years or month < min(order_months):
                    return data
                elif month > max(order_months):
                    continue

                self.print_info(news_data)
                data.append(news_data)


if __name__ == "__main__":
    ustc = USTC()
    data = ustc.get_news(order_years=[2023], order_months=[5])
    ustc.classify_data(data)
    ustc.save_news(ustc.outfile_name)
