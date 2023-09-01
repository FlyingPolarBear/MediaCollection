'''
Author: Derry
Date: 2022-05-26 21:38:58
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2023-08-01 11:53:24
Description: 主函数
'''
import datetime
import time

from rich import print as rprint
from rich.console import Console

from university import Fudan, NJU, ZJU, USTC, TJU, zip_dir


def timed_trigger_main():
    now = datetime.datetime.now()
    awake_time = datetime.datetime(
        now.year + 1, 1, 1) if now.month == 12 else datetime.datetime(now.year, now.month + 1, 1)
    rprint(f"awake_time: {awake_time}")
    time.sleep((awake_time - now).total_seconds())
    while True:
        now = datetime.datetime.now()
        for UNIV in [Fudan, NJU, ZJU, USTC, TJU]:
            univ = UNIV()
            rprint(univ.univ_name)
            data = univ.get_news(
                order_years=[2022], order_months=[now.month-1])
            univ.classify_data(data)
            univ.save_news(univ.outfile_name)
        awake_time = datetime.datetime(
            now.year + 1, 1, 1) if now.month == 12 else datetime.datetime(now.year, now.month + 1, 1)
        rprint(f"awake_time: {awake_time}")
        time.sleep((awake_time - now).total_seconds())


def main(order_months=None):
    """
    ! Attention: 南京大学每月需要更新infoids
    ! Attention: 中国科大需要注意max_page的变更
    ? Caution: 天津大学需要注意max_page的变更
    """
    if order_months is None:
        now = datetime.datetime.now()
        order_months = [now.month-1]
    for UNIV in [Fudan, NJU, ZJU, USTC, TJU]:
        univ = UNIV()
        console = Console()
        console.rule(f"\n[bold red]👇👇👇 {' '.join(univ.univ_name)} 👇👇👇[/bold red]\n")
        rprint(f"📕 [bold red]{univ.univ_name}[/bold red] 新闻网：[italic blue]{univ.base_url}[/italic blue]\n")
        data = univ.get_news(order_years=[2023], order_months=order_months)
        univ.classify_data(data)
        univ.save_news(univ.outfile_name)
        rprint(f"📕 [bold red]{univ.univ_name}[/bold red] {','.join([str(m) for m in order_months])} 月媒体数据已保存至：[italic yellow]{univ.outfile_name}[/italic yellow]\n")
    zip_file_dir = f"out/2023{order_months[0]:02d}各刊物情况"
    zip_dir(zip_file_dir, f"{zip_file_dir}.zip")


if __name__ == "__main__":
    main([8])
