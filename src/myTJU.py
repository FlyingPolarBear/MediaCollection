'''
Author: Derry
Date: 2022-06-08 17:19:54
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-12-01 15:43:15
Description: 天津大学新闻网爬虫
'''
from src.NewsInfo import NewsInfo
from src.utils import request_url


class TJU(NewsInfo):
    def __init__(self) -> None:
        super().__init__()
        self.univ_name = '天津大学'
        self.base_url = "http://news.tju.edu.cn/"
        # self.max_num = 715 #总页数+1

    def _nextpage(self, i):
        if i == 1:
            return "http://news.tju.edu.cn/mtbd.htm"
        else:
            return f"http://news.tju.edu.cn/mtbd/{self.max_num-i}.htm"

    def _get_max_page(self):
        pass

    def _time_parser(self, news_time):
        news_time = news_time.text.strip()
        year = news_time[:4]
        month = news_time[5:7]
        day = news_time[8:10]
        return year+'-'+month+'-'+day

    def _media_parser(self, title):
        return title.split('：')[0]

    def _get_next_pagenum(self, soup):
        a_list = soup.find_all("a")
        for a in a_list:
            if a.text == '下页':
                nextpage_part_url = a.get('href')
                break
        next_num = int(nextpage_part_url.split('.')[0][5:])
        return next_num

    def get_news(self, order_years=[2022], order_months=[3, 4, 5, 6]):
        self.outfile_name = self._get_out_name(
            self.univ_name, order_years[0], order_months)
        data = []
        i = 0
        title_list = []
        while True:
            i += 1
            soup = request_url(self._nextpage(i))
            if i == 1:
                self.max_num = self._get_next_pagenum(soup)+2
            news_list = soup.find_all('h4')
            time_list = soup.find_all('h5')

            for news, time_ in zip(news_list[:-1], time_list[:-1]):
                news_url = self.base_url+news.find('a').get('href')

                news_data = {'url': news_url}

                news_data['time'] = self._time_parser(time_)
                news_data['title'] = news.text
                news_data['media'] = self._media_parser(news_data['title'])
                # news_data['page'] = i

                year = int(news_data['time'][:4])
                month = int(news_data['time'][5:7])
                if year not in order_years or month < min(order_months):
                    return data
                elif month > max(order_months):
                    continue

                if news_data['title'] not in title_list:
                    print(news_data)
                    data.append(news_data)
                    title_list.append(news_data['title'])


if __name__ == "__main__":
    tju = TJU()
    data = tju.get_news(order_years=[2022], order_months=[11])
    tju.classify_data(data)
    tju.save_news(tju.outfile_name)
