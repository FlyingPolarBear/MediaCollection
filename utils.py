'''
Author: Derry
Date: 2022-05-26 21:42:07
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-06-08 22:51:17
Description: None
'''

import re
import requests
from bs4 import BeautifulSoup
import retry
import json

from sympy import content


@retry.retry(tries=3, delay=1)
def request_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup


def post_data(url, data):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    response = requests.post(url, data=data, headers=headers)
    response.encoding = response.apparent_encoding
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            res_data = json.loads(soup.text)
        except:
            try:
                contents = ['5月18日上午，"云深处——高云作品展"在南京大学美术馆开幕，献礼南京大学120周年校庆。展览紧扣南京大学120周年校庆，展出了高云120幅重磅画作，包括国画、连环画、邮票三大类别，以《花非花》《酹江月》《镜中人》《如意令》四大板块衔接串联、层层叠进。进入展区，迎面而来的便是一片蓝灰色，典雅内敛的氛围衬托出"花非花"版块的"理想伊甸园"。花非花版块展出了高云先生创作的女性题材作品。该部分聚焦于女性题材作品，其中包含了《魂系马嵬》《对话安格尔》《梦》等其最受关注的系列。本次展览还展出了多幅重量级力作，其中有被称为"20世纪白描连环画扛鼎之作"的《罗伦赶考》。《罗伦赶考》用13幅图画，把明代学者在赶考途中拾金不昧的故事生动描绘出来，该作品于1984年获得第六届全国美术作品展金奖，现藏于中国美术馆。展览艺术家高云，是中国画学会副会长、江苏省中国画学会会长、江苏省美术馆名誉馆长、南京大学兼职教授。他介绍，"云深处——高云作品展"是他第四次个人展览，也是首次在高校举办的展出。他希望通过本次展览不忘本心、回溯本意，向南大师生传达"迈好第一步"的精神。当天下午，高云于展厅内开展"笔墨当随人——跟着教授看展览"活动，为大家提供作品的导览介绍，线上直播累计超两万人观看。',
                            '百年来，学院及其前身始终秉承"诚朴雄伟、励学敦行"的校训，弘扬"公、忠、信、勤、久"的治学传统，已成为底蕴深厚、传承连贯、领域覆盖完整、学术建制完备、学术力量雄厚、蜚声海内外的大生命科学人才培养和科学研究基地。百年生科恰风华，学院将以百年华诞为契机，砥砺求索、奋斗不止，开启"第一个生科院"的新纪元。△校长吕建全国人大常委会委员、中国科学院院士、南大校长吕建在致辞中指出，100年来，南大生科薪火相传、学脉悠长，科教融合、立德树人，孜孜以求、勇攀高峰，书写了灿烂的历史篇章。新百年的南大生科，要以更加昂扬的姿态，与时代、国家、民族同频共振、同向同行。一是做到肩负历史使命，勇担复兴大任；二是做到发扬优良传统，发挥自身特色；三是做到坚持问题导向，深化改革创新。钟南山、饶子和等院士专家线上送祝福△钟南山院士著名医学家、"共和国勋章"获得者、中国工程院院士钟南山，在疫情防控百忙之中作为86年前在南京出生的老一辈科学家，向南大生物学科百年华诞致以热烈祝贺。']
                text = soup.text
                for content in contents:
                    text = text.replace(content, '')
                res_data = json.loads(text)
            except:
                with open("a.json", "w") as f:
                    f.write(soup.text)
    return res_data
