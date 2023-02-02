'''
Author: Derry
Date: 2022-05-26 21:38:58
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2023-02-02 10:42:39
Description: None
'''
import datetime
import os
import time

from src.myFudan import Fudan
from src.myNJU import NJU
from src.myTJU import TJU
from src.myUSTC import USTC
from src.myZJU import ZJU
from src.utils import zip_dir


def timed_trigger_main():
    now = datetime.datetime.now()
    awake_time = datetime.datetime(
        now.year + 1, 1, 1) if now.month == 12 else datetime.datetime(now.year, now.month + 1, 1)
    print(f"awake_time: {awake_time}")
    time.sleep((awake_time - now).total_seconds())
    while True:
        now = datetime.datetime.now()
        for UNIV in (Fudan, NJU, ZJU, USTC, TJU):
            univ = UNIV()
            print(univ.univ_name)
            data = univ.get_news(
                order_years=[2022], order_months=[now.month-1])
            univ.classify_data(data)
            univ.save_news(univ.outfile_name)
        awake_time = datetime.datetime(
            now.year + 1, 1, 1) if now.month == 12 else datetime.datetime(now.year, now.month + 1, 1)
        print(f"awake_time: {awake_time}")
        time.sleep((awake_time - now).total_seconds())


def main(order_months=None):
    if order_months is None:
        now = datetime.datetime.now()
        order_months = [now.month-1]
    for UNIV in (Fudan, NJU, ZJU, USTC, TJU):
        univ = UNIV()
        print(univ.univ_name)
        data = univ.get_news(order_years=[2023], order_months=order_months)
        univ.classify_data(data)
        univ.save_news(univ.outfile_name)
    zip_file_dir = f"out/2023{order_months[0]:02d}各刊物情况"
    zip_dir(zip_file_dir, f"{zip_file_dir}.zip")


if __name__ == "__main__":
    main([1])
