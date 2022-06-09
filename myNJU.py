'''
Author: Derry
Date: 2022-06-08 16:51:16
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-06-09 18:19:50
Description: None
'''
from NewsInfo import NewsInfo
from utils import post_data


class NJU(NewsInfo):
    def __init__(self) -> None:
        super().__init__()
        self.univ_name = '南京大学'
        self.base_url = "http://www.news.nju.edu.cn"

        self.infoid_list = ["LCwsLCwsLCwxMDkxNjAsMTA5MTU5LDEwOTE1OCwxMDkxNTcsMTA5MTU2LDEwOTE1NSwxMDkxNDgsMTA5MTQ3",
                            "LCwsLCwsLCwxMDkxNDYsMTA5MTM3LDEwOTEzNSwxMDkxMzMsMTA5MTMxLDEwOTEzMCwxMDkxMjgsMTA5MTI3",
                            "LCwsLCwsLCwxMDkxMjUsMTA5MTIwLDEwOTExOSwxMDkxMDQsMTA5MTAzLDEwOTEwMiwxMDkxMDEsMTA5MTAw",
                            "LCwsLCwsLCwxMDkwOTksMTA5MDk4LDEwOTA4MywxMDkwODIsMTA5MDc0LDEwOTA4MSwxMDkwODAsMTA5MDc5",
                            "LCwsLCwsLCwxMDkwNjksMTA5MDY4LDEwOTA1MSwxMDkwNTAsMTA5MDQ5LDEwOTA0OCwxMDkwNDcsMTA5MDQ2",
                            "LCwsLCwsLCwxMDkwNDQsMTA5MDI4LDEwOTAyNywxMDkwMjYsMTA4OTg1LDEwODk4MCwxMDg5NzgsMTA4OTc3",
                            "LCwsLCwsLCwxMDg5NzUsMTA4OTc0LDEwODk3MSwxMDg5NzAsMTA4OTY5LDEwODk2OCwxMDg5NjcsMTA4ODQ0",
                            "LCwsLCwsLCwxMDg4NDMsMTA4ODQxLDEwODg0MCwxMDg4MzksMTA4ODM3LDEwODgzNSwxMDg4MzQsMTA4ODMz",
                            "LCwsLCwsLCwxMDg4MTMsMTA4ODEyLDEwODgxMSwxMDg4MTAsMTA4ODA5LDEwODgwOCwxMDg4MDcsMTA4ODA2",
                            "LCwsLCwsLCwxMDg4MDUsMTA4ODAzLDEwODgwMSwxMDg3OTksMTA4Nzk3LDEwODc5NSwxMDg3OTMsMTA4Nzkx",
                            "LCwsLCwsLCwxMDg3ODksMTA4Nzg1LDEwODc1NSwxMDg3NTMsMTA4NzUyLDEwODc1MSwxMDg3NDksMTA4NzQ4",
                            "LCwsLCwsLCwxMDg3NDcsMTA4NzQ2LDEwODc0NCwxMDg3NDIsMTA4NzgyLDEwODczOSwxMDg3MzgsMTA4NzM2",
                            "LCwsLCwsLCwxMDg3MzUsMTA4NzM0LDEwODczMywxMDg3MzIsMTA4NzMxLDEwODcyOSwxMDg3MjcsMTA4NzI1",
                            "LCwsLCwsLCwxMDg3MjMsMTA4NzIyLDEwODcyMSwxMDg3MTksMTA4NzE4LDEwODcxNiwxMDg3MTQsMTA4NzEy",
                            "LCwsLCwsLCwxMDg3MTAsMTA4NzA5LDEwODcwNywxMDg3MDUsMTA4NzAzLDEwODcwMSwxMDg2OTksMTA4Njk3",
                            "LCwsLCwsLCwxMDg2MzYsMTA4Njg4LDEwODY4NiwxMDg2ODQsMTA4NjgyLDEwODY4MCwxMDg2NzgsMTA4Njc2",
                            "LCwsLCwsLCwxMDg2NzQsMTA4NjcyLDEwODY3MSwxMDg2NjksMTA4NjY3LDEwODY2NiwxMDg2NjUsMTA4NjY0",
                            "LCwsLCwsLCwxMDg2NjMsMTA4NjYxLDEwODY2MCwxMDg2NTgsMTA4NjU2LDEwODY1MiwxMDg2NTAsMTA4NjQ5",
                            "LCwsLCwsLCwxMDg2MzEsMTA4NjQ4LDEwODY0NiwxMDg3NTYsMTA4NTgyLDEwODYxMSwxMDg1NjcsMTA4NTY1",
                            "LCwsLCwsLCwxMDg1NjMsMTA4NTUzLDEwODU5NiwxMDg1OTUsMTA4NTgxLDEwODU4MCwxMDg1NzksMTA4NTc4",
                            "LCwsLCwsLCwxMDg1NzcsMTA4NTc2LDEwODU3NSwxMDg1NzQsMTA4NTczLDEwODU3MiwxMDg1NzAsMTA4NTY4",
                            "LCwsLCwsLCwxMDg1NTUsMTA4NTUxLDEwODU0OSwxMDg1NDcsMTA4NTI5LDEwODUyOCwxMDg1MjcsMTA4NTI2",
                            "LCwsLCwsLCwxMDg1MTEsMTA4NTI1LDEwODUyMywxMDg1MjIsMTA4NTIxLDEwODUxMCwxMDg1MDYsMTA4NDk5",
                            "LCwsLCwsLCwxMDg0OTcsMTA4NDk2LDEwODQ5NCwxMDg0OTMsMTA4NDkyLDEwODQ5MSwxMDg0OTAsMTA4NDg5",
                            "LCwsLCwsLCwxMDg0ODgsMTA4NDg3LDEwODQ4NiwxMDg0ODUsMTA4NDg0LDEwODQ4MywxMDg0ODIsMTA4NDgx",
                            "LCwsLCwsLCwxMDg0NjYsMTA4NDY0LDEwODQ1MiwxMDg0NTEsMTA4NDUwLDEwODQ0OCwxMDg0NDcsMTA4NDQz",
                            "LCwsLCwsLCwxMDg0NDIsMTA4NDQxLDEwODQ0MCwxMDg0MzksMTA4NDM4LDEwODQ2NSwxMDg0MzMsMTA4NDMw",
                            "LCwsLCwsLCwxMDg0MzIsMTA4NDEzLDEwODQxMiwxMDg0MTEsMTA4NDEwLDEwODQwOSwxMDg0MDIsMTA4NDAx",
                            "LCwsLCwsLCwxMDgzOTQsMTA4MzgzLDEwODM4MiwxMDgzODEsMTA4MzgwLDEwODM3MiwxMDgzNzEsMTA4Mzcw",
                            "LCwsLCwsLCwxMDgzNjIsMTA4MzYxLDEwODM1OSwxMDgzNTgsMTA4MzU3LDEwODM1MywxMDgzNDQsMTA4MzQx",
                            "LCwsLCwsLCwxMDgzMzQsMTA4MzMzLDEwODMzMiwxMDgzMzEsMTA4MzMwLDEwODMyOSwxMDgzMjgsMTA4MzQw",
                            "LCwsLCwsLCwxMDgzMjAsMTA4MzE5LDEwODMxOCwxMDgzMTcsMTA4MzE2LDEwODMwOCwxMDgzMTUsMTA4MzEz",
                            "LCwsLCwsLCwxMDgzMTIsMTA4MzE0LDEwODMwNiwxMDgzMDUsMTA4MzA0LDEwODMwMywxMDgzMDIsMTA4MzAx",
                            "LCwsLCwsLCwxMDgzMDAsMTA4Mjk5LDEwODI5OCwxMDgyODYsMTA4MjgzLDEwODI4MiwxMDgyNzQsMTA4Mjcz",
                            "LCwsLCwsLCwxMDgyNzIsMTA4MjcxLDEwODI3MCwxMDgyNjksMTA4MzA5LDEwODI1NywxMDgyNjEsMTA4MjYw",
                            "LCwsLCwsLCwxMDgyNTUsMTA4MjQ1LDEwODI0MSwxMDgyMzYsMTA4MjUzLDEwODI1MSwxMDgyNDksMTA4MjQ3",
                            "LCwsLCwsLCwxMDgyNjIsMTA4MjM0LDEwODIzMywxMDgyMzIsMTA4MjMxLDEwODIzNSwxMDgyMjIsMTA4MjIx",
                            "LCwsLCwsLCwxMDgyMjAsMTA4MjE5LDEwODIwNiwxMDgyMDUsMTA4MjA0LDEwODIwMywxMDgyMDIsMTA4MjAx",
                            "LCwsLCwsLCwxMDgyMDAsMTA4MTkzLDEwODE5MiwxMDgxOTEsMTA4MTg0LDEwODE4MywxMDgxODIsMTA4MTgx",
                            "LCwsLCwsLCwxMDgxODAsMTA4MTc5LDEwODE4NSwxMDgxNzEsMTA4MTY5LDEwODE2OCwxMDgxNjAsMTA4MTU4",
                            "LCwsLCwsLCwxMDgxNTQsMTA4MTUzLDEwODE1MiwxMDgxNTEsMTA4MTUwLDEwODEzOSwxMDgxMzQsMTA4MTMz",
                            "LCwsLCwsLCwxMDgxMzIsMTA4MTMxLDEwODEyOSwxMDgxMjgsMTA4MTI3LDEwODEyMCwxMDgxMTYsMTA4MTE1",
                            "LCwsLCwsLCwxMDgxMTQsMTA4MTEzLDEwODExMiwxMDgxMDEsMTA4MDk2LDEwODA5NCwxMDgwOTMsMTA4MDky",
                            "LCwsLCwsLCwxMDgwOTEsMTA4MDg0LDEwODA3OCwxMDgwNzcsMTA4MDc2LDEwODA3NSwxMDgwNzQsMTA4MDcz",
                            "LCwsLCwsLCwxMDgwNzIsMTA4MDcwLDEwODA2MiwxMDgwNTEsMTA4MDUwLDEwODA0OSwxMDgwNDgsMTA4MDQ3",
                            "LCwsLCwsLCwxMDgwNDYsMTA4MDQ1LDEwODAzOSwxMDgwMjcsMTA4MDI2LDEwODAyNSwxMDgwMjQsMTA4MDIz",
                            "LCwsLCwsLCwxMDgwMjIsMTA4MTI2LDEwODAwOSwxMDgwMDgsMTA4MDA3LDEwODAwNiwxMDc5OTksMTA3OTk4",
                            "LCwsLCwsLCwxMDc5OTcsMTA3OTk2LDEwNzk5NSwxMDc5ODgsMTA3OTgyLDEwNzk4MSwxMDc5NzksMTA3OTc4",
                            "LCwsLCwsLCwxMDc5NzcsMTA3OTc2LDEwNzk3NSwxMDc5NzQsMTA3OTcyLDEwNzk3MywxMDc5NTksMTA3OTQ4",
                            "LCwsLCwsLCwxMDc5NDcsMTA3OTQ2LDEwNzk0NSwxMDc5NDQsMTA3OTQzLDEwNzk0MiwxMDc5NDEsMTA3OTQw",
                            "LCwsLCwsLCwxMDc5MjUsMTA3OTYyLDEwNzkyNCwxMDc5MjEsMTA3OTIwLDEwNzkxOSwxMDc5MTgsMTA3OTAw"]

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
                    if year not in order_years or month not in order_months:
                        return data

                    print(news_data)
                    data.append(news_data)


if __name__ == "__main__":
    nju = NJU()
    data = nju.get_news(order_years=[2022], order_months=[3, 4, 5, 6])
    nju.classify_data(data)
    nju.save_news(nju.outfile_name)
