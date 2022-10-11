'''
Author: Derry
Date: 2022-06-08 13:07:16
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-10-11 12:47:27
Description: 浙江大学新闻网爬虫
'''
from NewsInfo import NewsInfo
from utils import request_url


class ZJU(NewsInfo):
    def __init__(self) -> None:
        super().__init__()
        self.univ_name = '浙江大学'
        self.base_url = "http://www.news.zju.edu.cn"

    def _nextpage(self, i):
        if i == 1:
            return "http://www.news.zju.edu.cn/775/list.htm"
        else:
            return f"http://www.news.zju.edu.cn/775/list{i}.htm"

    def _time_parser(self, news_time):
        year = news_time[5:9]
        month = news_time[10:12]
        day = news_time[13:15]
        return year+'-'+month+'-'+day

    def get_news(self, order_years=[2022], order_months=[3, 4, 5, 6]):
        self.outfile_name = self._get_out_name(self.univ_name, order_years[0], order_months)
        data = []
        i = 0
        while True:
            i += 1
            soup = request_url(self._nextpage(i))
            news_list = soup.find_all('span', class_='cols_title')

            for news in news_list:
                news_url = self.base_url+news.find('a').get('href')
                if 'page.htm' in news_url:
                    news_data = {'url': news_url}
                    news_soup = request_url(news_url)

                    news_time = news_soup.find_all(
                        'span', class_='arti-update')[0].text
                    news_data['time'] = self._time_parser(news_time)
                    news_data['title'] = news_soup.find_all(
                        'h1', class_='arti-title rol-title')[0].text
                    news_data['media'] = news_soup.find_all(
                        'span', class_='arti-info')[0].text

                    year = int(news_data['time'][:4])
                    month = int(news_data['time'][5:7])
                    if year not in order_years or month < min(order_months):
                        return data
                    elif month > max(order_months):
                        continue

                    print(news_data)
                    data.append(news_data)


if __name__ == "__main__":
    zju = ZJU()
    data = zju.get_news(order_years=[2022], order_months=[8])
    zju.classify_data(data)
    zju.save_news(zju.outfile_name)
