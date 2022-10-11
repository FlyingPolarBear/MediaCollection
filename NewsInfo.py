'''
Author: Derry
Date: 2022-06-08 15:42:40
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-10-11 12:51:05
Description: 新闻网爬虫基类
'''
import xlwt


class NewsInfo:
    def __init__(self):
        self.media_list = ["人民日报海外版", "人民日报客户端", "人民日报", "新华社", "中央人民广播电台", "中央电视台", "求是", "解放军报", "光明日报", "经济日报", "中国日报",
                           "科技日报", "人民政协报", "中国纪检监察报", "中国新闻网", "学习时报", "工人日报", "中国青年报", "中国妇女报", "农民日报", "法制日报", "其它"]

    def _get_out_name(self, univ_name, year, month):
        if len(month) > 1:
            month_start = min(month)
            month_end = max(month)
            month_start = month_start if month_start > 10 else '0'+str(month_start)
            month_end = month_end if month_end > 10 else '0'+str(month_end)
            time_str = f'{year}{month_start}-{year}{month_end}'
        else:
            month = month[0] if month[0] > 10 else '0'+str(month[0])
            time_str = f'{year}{month}'
        return f"data/{univ_name}{time_str}各刊物情况.xls"

    def classify_data(self, data):
        self.media_dict = {media: [] for media in self.media_list}
        for d in data:  # for each news
            flag = False
            if '新闻联播' in d['media']:
                d['media'] = '中央电视台'
                self.media_dict['中央电视台'].append(d)
                continue
            for media in self.media_list[:-1]:
                if media in d['media']:
                    d['media'] = media
                    self.media_dict[media].append(d)
                    flag = True
                    break
            if not flag:
                self.media_dict['其它'].append(d)

    def save_news(self, outfile_name='各刊物情况.xlsx'):
        wb = xlwt.Workbook()
        ws_all = wb.add_sheet('统计')
        ws_all.write(0, 0, '媒体')
        ws_all.write(0, 1, '数量')
        for i, media in enumerate(self.media_list):
            ws_all.write(i+1, 0, media)
            ws_all.write(i+1, 1, len(self.media_dict[media]))
            ws = wb.add_sheet(media)
            ws.write(0, 0, '时间')
            ws.write(0, 1, '标题')
            ws.write(0, 2, '链接')
            for i, d in enumerate(self.media_dict[media]):
                ws.write(i+1, 0, d['time'])
                ws.write(i+1, 1, d['title'])
                ws.write(i+1, 2, d['url'])
        wb.save(outfile_name)
