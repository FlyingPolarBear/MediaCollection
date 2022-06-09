'''
Author: Derry
Date: 2022-05-26 21:38:58
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-06-08 21:59:15
Description: None
'''
from myFudan import Fudan
from myZJU import ZJU
from myUSTC import USTC
from myTJU import TJU
from myNJU import NJU

for UNIV in (Fudan, ZJU, USTC, TJU, NJU):
    univ = UNIV()
    data = univ.get_news(order_years=[2022], order_months=[3, 4, 5, 6])
    univ.classify_data(data)
    univ.save_news(univ.outfile_name)
