'''
Author: Derry
Date: 2022-06-08 16:06:00
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-06-09 18:19:04
Description: None
'''
import re

from NewsInfo import NewsInfo
from utils import request_url


class USTC(NewsInfo):
    def __init__(self) -> None:
        super().__init__()
        self.univ_name = '中国科大'
        self.base_url = "http://news.ustc.edu.cn/"

    def _nextpage(self, i):
        if i == 1:
            return "http://news.ustc.edu.cn/mtgz.htm"
        else:
            return f"http://news.ustc.edu.cn/mtgz/{448-i}.htm"

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
        media1 = re.findall(pattern1, title)
        pattern2 = re.compile(r'《(.*?)》')
        media2 = re.findall(pattern2, title)
        media1 = media1[0] if len(media1) else ''
        media2 = media2[0] if len(media2) else ''
        return media1 + ' ' + media2

    def get_news(self, order_years=[2022], order_months=[3, 4, 5, 6]):
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
                if year not in order_years or month not in order_months:
                    return data

                print(news_data)
                data.append(news_data)


if __name__ == "__main__":
    ustc = USTC()
    data = ustc.get_news(order_years=[2022], order_months=[3, 4, 5, 6])
    ustc.classify_data(data)
    ustc.save_news(ustc.outfile_name)
