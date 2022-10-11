'''
Author: Derry
Date: 2022-06-08 16:51:16
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-10-11 12:43:07
Description: 南京大学新闻网爬虫
'''
from NewsInfo import NewsInfo
from utils import post_data


class NJU(NewsInfo):
    def __init__(self) -> None:
        super().__init__()
        self.univ_name = '南京大学'
        self.base_url = "http://www.news.nju.edu.cn"

        self.infoid_list = open('nju_infoid_list.txt', 'r').read().split('\n')

    def get_news(self, order_years=[2022], order_months=[3, 4, 5, 6]):
        self.outfile_name = self._get_out_name(
            self.univ_name, order_years[0], order_months)
        data = []
        while True:
            url = "https://news.nju.edu.cn/nju/openapi/t/info/detail.do"
            for i, infoid in enumerate(self.infoid_list):
                news_list = post_data(url, {'infoids': infoid})['detail']

                for news in news_list:
                    news_data = {
                        'url': news['url'], 'time': news['daytime'], 'media': news['source'], 'title': news['title']}

                    year = int(news_data['time'][:4])
                    month = int(news_data['time'][5:7])
                    if year not in order_years or month < min(order_months):
                        return data
                    elif month > max(order_months):
                        continue

                    print(news_data)
                    data.append(news_data)


if __name__ == "__main__":
    nju = NJU()
    data = nju.get_news(order_years=[2022], order_months=[8])
    nju.classify_data(data)
    nju.save_news(nju.outfile_name)
