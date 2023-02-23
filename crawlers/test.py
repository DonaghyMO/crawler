import itchat

import sys, os

sys.path.append(os.path.abspath(__file__).split("crawlers")[0])
from crawlers.crawl_linux import *
from channel import wechat
from common.log import logger
from crawlers.base import is_msg_exist, time_match, parse_time
import bs4, re
import requests
from crawlers.crawl_linux import delete_html


def parse_xiangtan_time(time_msg):
    months = {"一月": 1, "二月": 2, "三月": 3, "四月": 4, "五月": 5, "六月": 6, "七月": 7, "八月": 8, "九月": 9,
              "十月": 10, "十一月": 11, "十二月": 12}
    rmatch = re.compile(r"['一','二','三','四', '五','六','七','八','九','十']*['月']{1} \d+, \d+")
    if rmatch.search(time_msg) is not None:
        print(time_msg)
        month, day, year = time_msg.split(' ')
        month = months[month]
        day = day.strip(',')
        year, month, day = int(year), int(month), int(day)
        return str(datetime.date(year=year, month=month, day=day))
    return None



if __name__ == '__main__':
    # 研招网
    # url = "https://yz.chsi.com.cn/apply/cjcx/cjcx.do"
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
    #     "Cookie": """SF_cookie_2 = 96816998;JSESSIONID = 6B67978CB3D33B9EA650A22C65F8F2CC"""
    # }
    # params = {"xm": "莫登意", "zjhm": "430105199806035615", "ksbh": "100133412881861", "bkdwdm": "10013"}
    # req = requests.post(url, params, headers=headers)
    # print(req.text)

    # 杭州师范大学
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
    #     "Cookie": """SF_cookie_2 = 96816998;JSESSIONID = 6B67978CB3D33B9EA650A22C65F8F2CC"""
    # }
    # req = requests.get("https://yjs.hznu.edu.cn/yjszs/sszs/", headers=headers)
    # req.encoding = "utf-8"
    # hangshifan = bs4.BeautifulSoup(req.text, "html.parser")
    # for i in hangshifan.find_all("a",attrs={"title":re.compile("^$")}):
    #     mesg_time = re.findall(time_match, str(i))[0]
    #
    #     mesg = "【杭州师范大学{}】有新消息：{}".format(parse_time(mesg_time),
    #                                                  re.sub(r"<.*?>|&nbsp;|\n", "", str(i)))
    #     if not is_msg_exist(mesg):
    #         flag = False
    #         msg_to_write = msg_to_write + mesg

    # print(msg_to_write)
    # 测试登录
    # chan = wechat.WechatChannel()
    # chan.startup()

    # 测试湘潭大学
    # import ssl
    # #
    # proxy = {'http':'http://127.0.0.1:8080','https':'https://127.0.0.1:8080'}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
        "Cookie": """SF_cookie_2 = 96816998;JSESSIONID = 6B67978CB3D33B9EA650A22C65F8F2CC"""
    }
    # req = requests.get("https://jwxy.xtu.edu.cn/tzgg1/tzgg.htm",headers=headers,verify=False)
    # req.encoding = "utf-8"
    # xiangtan_b = bs4.BeautifulSoup(req.text, "html.parser")
    # for i in xiangtan_b.find_all("article",attrs={"class":"elementor-post elementor-grid-item post-2106 post type-post status-publish format-standard hentry category-36"}):
    #     msg_day = parse_xiangtan_time(delete_html(str(i.div.div)))
    #     if msg_day >= begin_date:

        # print("{}\n\n\n".format(delete_html()
        # print(parse_xiangtan_time(str(i.div.div)))

    # 测试湘潭大学时间
    # a = input()
    # parse_xiangtan_time(a)

    # if platform.system().lower() == "linux":
    #     file_name = "/root/msg/{}.txt".format(begin_date)
    # else:
    #     file_name = "D:\\msg\\{}.txt".format(begin_date)
    #
    # fp = open(file_name, "r")
    # today_contain = fp.read()
    # print(today_contain)


    # 测试燕山大学
    # 燕山大学
    # req = requests.get("https://zsjyc.ysu.edu.cn/yjsxwz/sszs/szdong.htm", headers=headers, verify=False)
    # req.encoding = "utf-8"
    # yanshan_b = bs4.BeautifulSoup(req.text, "html.parser")
    # for i in yanshan_b.find_all("a",attrs={"target":"_blank","class":""}):
    #     print(delete_html(str(i)).strip())
    #     year,month,day= delete_html(str(i.parent()[0])).strip().split('-')
    #     year,month,day = int(year),int(month),int(day)
    #     crawl_day = datetime.date(year,month,day)
    #     if crawl_day <= begin_date:
    #         print(111)


    # 测试湖北大学
    # 湖北大学
    # url = "http://yz.hubu.edu.cn/zsxy/sszs.htm"
    # req = requests.get(url, headers=headers)
    # req.encoding = "utf-8"
    # hubeidaxue_b = bs4.BeautifulSoup(req.text, "html.parser")
    # for i in hubeidaxue_b.find_all("a",attrs={'target':"_blank"}):
    #     if 'title' in i.attrs.keys():
    #
    #         date = parse_time(re.findall(r'\d+-\d+-\d+', str(i.parent))[0])
    #         msg = "【湖北大学{}】{}".format(str(date), delete_html(str(i)))
    #         msg_to_write = msg_to_write + str(msg)
    #         print(msg_to_write)
    #

    # 测试linux发微信
    c = wechat.WechatChannel()
    c.startup(test_send)

