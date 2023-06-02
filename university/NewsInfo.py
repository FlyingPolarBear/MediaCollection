'''
Author: Derry
Date: 2022-06-08 15:42:40
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2023-06-01 11:06:23
Description: 新闻网爬虫基类
'''
import json

import xlwt
from rich import print as rprint

from university.utils import mkdir

# 新华社：包含新华社客户端和新华社报纸的新闻，不包含新华网的新闻
# 中央广播电视总台：包括中央电视台和中央人民广播电台，主要是包括各类CCTV频道报道，一般以“央视新闻”、“新闻联播”等作为标签
# 中国青年报：只统计报纸的，不包括客户端

class NewsInfo:
    def __init__(self):
        self.univ_name = 'xx大学'
        self.base_url = "https://www.xxx.edu.cn"
        with open("media_list.json", "r", encoding="utf-8") as f:
            self.outmedia_to_media = json.load(f)
        self.media_list = list(self.outmedia_to_media.values())
        self.media_list = sorted(set(self.media_list), key=self.media_list.index)

    def _get_out_name(self, univ_name, year, month):
        if len(month) > 1:
            month_start = min(month)
            month_end = max(month)
            month_start = month_start if month_start > 10 else '0'+str(month_start)
            month_end = month_end if month_end > 10 else '0'+str(month_end)
            time_str = f'{year}{month_start}-{year}{month_end}'
        else:
            month = month[0] if month[0] >= 10 else '0'+str(month[0])
            time_str = f'{year}{month}'
        out_dir = f"out/{time_str}各刊物情况"
        mkdir(out_dir)
        out_name = f"{out_dir}/{univ_name}{time_str}各刊物情况.xls"
        return out_name

    def print_info(self,info:dict):
        rprint(f"[bold]{info['title']}[/bold]")
        rprint(f"[cyan]{info['time']}[/cyan] [yellow]{info['media']}[/yellow] [italic]{info['url']}[/italic]\n")

    def classify_data(self, data):
        self.media_dict = {media: [] for media in self.media_list}
        for d in data:  # for each news
            flag = False
            for media in self.outmedia_to_media.keys():
                if media in d['media']:
                    d['media'] = self.outmedia_to_media[media]
                    self.media_dict[self.outmedia_to_media[media]].append(d)
                    flag = True
                    break
            if not flag:
                self.media_dict['其它'].append(d)

    def save_news(self, outfile_name='各刊物情况.xlsx'):
        num = 0
        wb = xlwt.Workbook()
        ws_all = wb.add_sheet('统计')
        ws_all.write(0, 0, '媒体')
        ws_all.write(0, 1, '数量')
        for i, media in enumerate(self.media_list):
            ws_all.write(i+1, 0, media)
            ws_all.write(i+1, 1, len(self.media_dict[media]))
            num+=len(self.media_dict[media])
            ws = wb.add_sheet(media)
            ws.write(0, 0, '时间')
            ws.write(0, 1, '标题')
            ws.write(0, 2, '链接')
            for i, d in enumerate(self.media_dict[media]):
                ws.write(i+1, 0, d['time'])
                ws.write(i+1, 1, d['title'])
                ws.write(i+1, 2, d['url'])
        wb.save(outfile_name)
        if len(self.media_dict) == 0:
            rprint(f"❌ [bold yellow]警告：[/bold red] {self.univ_name}未找到任何新闻！\n")
        else:
            rprint(f"✅ [bold red]{self.univ_name}[/bold red] [bold green]成功[/bold green] 找到 {num} 条新闻！\n")
        

if __name__ == "__main__":
    NewsInfo()
