'''
Author: Derry
Date: 2022-05-26 21:38:58
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-11-02 12:12:29
Description: None
'''
import datetime
import time

from myFudan import Fudan
from myNJU import NJU
from myTJU import TJU
from myUSTC import USTC
from myZJU import ZJU

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
            data = univ.get_news(order_years=[2022], order_months=[now.month-1])
            univ.classify_data(data)
            univ.save_news(univ.outfile_name)
        awake_time = datetime.datetime(
            now.year + 1, 1, 1) if now.month == 12 else datetime.datetime(now.year, now.month + 1, 1)
        print(f"awake_time: {awake_time}")
        time.sleep((awake_time - now).total_seconds())

def main():
    now = datetime.datetime.now()
    for UNIV in (Fudan, NJU, ZJU, USTC, TJU):
            univ = UNIV()
            print(univ.univ_name)
            data = univ.get_news(order_years=[2022], order_months=[now.month-1])
            univ.classify_data(data)
            univ.save_news(univ.outfile_name)

if __name__ == "__main__":
    main()
