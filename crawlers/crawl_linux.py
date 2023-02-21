#!/usr/bin/python
# -*- coding: UTF-8 -*-
import itchat
import requests
import re
import bs4
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

import os
import sys

sys.path.append(os.path.abspath(__file__).split("crawlers")[0])
from channel import wechat
from common.log import logger

time_match = re.compile("\d{4}-\d{2}-\d{2}")
useless_key_words = ["无查询结果"]
engineering = ["工学"]
expertises = ["网络空间安全", "计算机", "电子", "网络", "计算机科学与技术","电子信息"]
# 爬虫开始的日期
begin_date = datetime.date.today()
# begin_date = datetime.date(2022,2,15)
# file_name = "E:\\msg\\{}.txt".format(begin_date)
file_name = "/root/msg/{}.txt".format(begin_date)


def parse_time(time_str):
    year, month, day = time_str.split('-')
    year, month, day = int(year), int(month), int(day)
    return datetime.date(year, month, day)


def is_msg_exist(msg):
    fp = open(file_name, "r")
    if msg in fp.read():
        # TODO:把消息发出去
        return True
    return False


def is_computer_science(msg):
    for i in expertises:
        if i in msg:
            return True
    return False


def crawl_msg():
    url_dic = {
        "yanzhao": "https://yz.chsi.com.cn/apply/cjcx/cjcx.do",
        "fangban": "http://wyy.gzhu.edu.cn/zsjy/yjszs.htm",
        "guangzhoudaxue": "http://yjsy.gzhu.edu.cn/zsxx/zsdt.htm",
        "fujianshifan": "https://yjsy.fjnu.edu.cn/4227/list1.htm",
        "xiaomuchong": ["http://muchong.com/bbs/kaoyan.php?action=adjust&type=1",
                        "http://muchong.com/bbs/kaoyan.php?action=adjust&type=1&page=1&page=2",
                        "http://muchong.com/bbs/kaoyan.php?action=adjust&type=1&page=1&page=3",
                        "http://muchong.com/bbs/kaoyan.php?action=adjust&type=1&page=3&page=4"]
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
        "Cookie": """SF_cookie_2 = 96816998;JSESSIONID = 6B67978CB3D33B9EA650A22C65F8F2CC"""
    }
    flag = True
    fp = open(file_name, "a")
    msg_to_write = ""
    # # 研招网查成绩
    params = {"xm": "莫登意", "zjhm": "430105199806035615", "ksbh": "100133412881861", "bkdwdm": "10013"}
    req = requests.post(url_dic["yanzhao"], params, headers=headers)
    if "无查询结果" in req.text:
        wchannel.send("【研招网】成绩还查不到\n", get_mo_id())
    else:
        wchannel.send("【研招网】成绩查到了！！\n", get_mo_id())

    # 广州大学方班最新消息
    req = requests.get(url_dic["fangban"], headers=headers)
    req.encoding = "utf-8"
    fangban_b = bs4.BeautifulSoup(req.text, "html.parser")
    for i in fangban_b.select("a > span"):
        mesg_date_str = re.findall(time_match, str(i.find_parent()))
        if mesg_date_str:
            year, month, day = mesg_date_str[0].split('-')
            year, month, day = int(year), int(month), int(day)
            mesg_date = datetime.date(year, month, day)
            if mesg_date > begin_date:
                mesg = "【广州大学方班{}】有新消息{}\n".format(mesg_date,
                                                             re.sub(r"<.*?>|&nbsp;|\n", "", str(i.find_parent())))
                if not is_msg_exist(mesg):
                    flag = False
                    msg_to_write = msg_to_write + mesg

    # 广州大学研究生院
    req = requests.get(url_dic["guangzhoudaxue"], headers=headers)
    req.encoding = "utf-8"
    guangda_b = bs4.BeautifulSoup(req.text, "html.parser")
    for i in guangda_b.find_all('a'):
        mesg_time = re.findall(time_match, str(i))
        if mesg_time:
            if parse_time(mesg_time[0]) > begin_date:

                i = re.findall(r"title=(.+?)\"", str(i))
                mesg = "【广州大学研究生院{}】有新消息：{}\n".format(parse_time(mesg_time[0]), i)
                if not is_msg_exist(mesg):
                    flag = False
                    msg_to_write = msg_to_write + mesg

    # 福建师范大学研究生院
    req = requests.get(url_dic["fujianshifan"], headers=headers)
    req.encoding = "utf-8"
    fushi_b = bs4.BeautifulSoup(req.text, "html.parser")
    for i in fushi_b.find_all("td"):
        mesg_time = re.findall(time_match, str(i))
        if mesg_time and parse_time(mesg_time[0]) > begin_date:
            if not i.find_all("a"):
                continue
            mesg = "【福建师范{}】有新消息：{}\n".format(parse_time(mesg_time[0]),
                                                      re.sub(r"<.*?>|&nbsp;|\n", "", str(i.find_all("a"))))
            if not is_msg_exist(mesg):
                flag = False
                msg_to_write = msg_to_write + mesg

    # 小木虫
    for url in url_dic["xiaomuchong"]:
        req = requests.get(url, headers=headers)
        xiaomu_b = bs4.BeautifulSoup(req.text, "html.parser")
        for i in xiaomu_b.find_all("tr"):
            if not "工学" in str(i):
                continue
            mesg_time = re.findall(time_match, str(i))
            if mesg_time and parse_time(mesg_time[0]) >= begin_date:
                mesg = "【小木虫{}】{}\n".format(parse_time(mesg_time[0]), re.sub(r"<.*?>|&nbsp;|\n", "", str(i)))
                if not is_msg_exist(mesg) and is_computer_science(mesg):
                    flag = False
                    msg_to_write = msg_to_write + mesg
    if not flag:
        fp.write(msg_to_write)

    # TODO:研招网

    # TODO:中国教育在线
    return msg_to_write


def five_m_send():
    msg = crawl_msg()
    if msg:
        wchannel.send(msg, get_mo_id())


def after_login():
    sched.add_job(five_m_send, "interval", minutes=5)
    sched.start()
    logger.info("发送消息")


def get_mo_id():
    mo = itchat.search_friends(name=u'墨')
    mo_id = mo[0]['UserName']
    return mo_id


def test_send():
    msg = "today"
    wchannel.send(msg, get_mo_id())


if __name__ == "__main__":
    sched = BlockingScheduler()
    wchannel = wechat.WechatChannel()
    wchannel.startup(after_login)
