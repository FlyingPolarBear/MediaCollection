'''
Author: Derry
Date: 2022-06-08 16:51:16
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2023-05-31 12:56:37
Description: 南京大学新闻网爬虫
'''
from university.utils import post_data
from university.NewsInfo import NewsInfo
from university.utils import request_url
from rich import print as rprint

class NJU(NewsInfo):
    def __init__(self) -> None:
        super().__init__()
        self.univ_name = '南京大学'
        self.base_url = "https://news.nju.edu.cn"
        self.info_base_url = "https://www.nju.edu.cn"
        self.max_num = 1367

    def _nextpage(self, i):
        if i == 1:
            return "https://www.nju.edu.cn/xww/mtcz.htm"
        else:
            return f"https://www.nju.edu.cn/xww/mtcz/{self.max_num-i}.htm"

    def _get_next_pagenum(self, soup):
        p_no = soup.find('span', attrs={"class": "p_no"})
        nextpage_url = p_no.find('a').get('href')
        return int(nextpage_url.split('.')[-2].split('/')[-1])

    def _time_parser(self, news):
        date_year = news.find('div', attrs={"class": "kxdt-l"})
        year = int(date_year.find('span').get_text())
        month_date = date_year.find('p').get_text()
        month = int(month_date.split('-')[0])
        date = int(month_date.split('-')[1])
        return year, month, date

    def _detail_parser(self, news_url):
        detail_soup = request_url(news_url)

        time_ = detail_soup.find(
            'span', attrs={"class": "ardate"})
        if time_ is not None:
            time_ = time_.get_text().strip()
            if time_.startswith("发布时间："):
                time_ = time_[5:]
        else:
            raise Exception("time_ is None")

        media = detail_soup.find(
            'span', attrs={"class": "arsource"})
        if media is not None:
            media = media.get_text().strip()
            if media.startswith("来源："):
                media = media[3:]
        else:
            raise Exception("media is None")

        title = detail_soup.find_all('h2')[2].get_text()
        # sub_title = detail_soup.find_all('h3')
        return {"url": news_url, "time": time_, "media": media, "title": title}

    def _detail_parser2(self, news_url):
        detail_soup = request_url(news_url)
        info = detail_soup.find('span', attrs={"id": "copyfrom"})
        if info is not None:
            info = info.get_text().strip().replace("&nbsp;", "")
            media = info.split("|")[0]
            time_ = info.split("|")[1].split(" ")[0].strip()
        else:
            return False
        title = detail_soup.find(
            'h1', attrs={"id": "js-title", "class": "js-title"})
        if title is not None:
            title = title.get_text().strip()
        else:
            raise Exception("title is None")
        return {"url": news_url, "time": time_, "media": media, "title": title}

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
                self.max_num = self._get_next_pagenum(soup) + 2
            news_list = soup.find_all('a', attrs={"class": "flex"})
            for news in news_list:
                title = news.find(
                    'h3', attrs={"class": "l2"}).get_text().replace("\xa0", " ")
                news_url = news.get('href').strip('.')
                if news_url.startswith('/..'):
                    news_url = news_url[3:]
                year_coarse, month_coarse, date_coarse = self._time_parser(
                    news)
                if year_coarse not in order_years or month_coarse < min(order_months):
                    # 如果超出了限定范围
                    return data
                elif month_coarse > max(order_months):
                    # 如果未到达限定范围
                    continue
                elif not news_url.startswith('/info'):
                    # 奇怪的链接
                    news_data = self._detail_parser2(news_url)
                else:
                    # 正常链接
                    news_url = self.info_base_url + news_url
                    news_data = self._detail_parser(news_url)
                if news_data is False:
                    rprint(f"abnormal news: {news_url}")
                    continue
                if news_data['title'] not in title_list:
                    self.print_info(news_data)
                    data.append(news_data)
                    title_list.append(title)


class NJUv1(NewsInfo):
    def __init__(self) -> None:
        super().__init__()
        self.univ_name = '南京大学'
        self.base_url = "http://news.nju.edu.cn"

        self.infoid_list = open(
            'nju_infoid_list.txt', 'r').read().split('\n')

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

                    self.print_info(news_data)
                    data.append(news_data)


if __name__ == "__main__":
    nju = NJU()
    data = nju.get_news(order_years=[2023], order_months=[8])
    nju.classify_data(data)
    nju.save_news(nju.outfile_name)
