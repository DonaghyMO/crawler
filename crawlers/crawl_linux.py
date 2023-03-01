#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys

sys.path.append(os.path.abspath(__file__).split("crawlers")[0])
import itchat
import requests
import re
import bs4
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import platform
from channel import wechat
from common.log import logger

time_match = re.compile("\d{4}-\d{2}-\d{2}")
useless_key_words = ["无查询结果"]
engineering = ["工学"]
expertises = ["网络空间安全", "计算机", "电子", "网络", "计算机科学与技术", "电子信息"]
strong_notify_schools = ["燕山大学", "广州大学", "福建师范大学", "湖北大学", "石河子大学", "杭州师范大学", "湘潭大学"]
# 爬虫开始的日期
begin_date = datetime.date.today()
# begin_date = datetime.date(2022,2,15)


# 测试用
start_time = time.time()

work_directory_linux = "/root/msg/"
work_directory_win = "D:\\msg\\"

if platform.system().lower() == "linux":
    file_name = "{}{}.txt".format(work_directory_linux,begin_date)
else:
    file_name = "{}{}.txt".format(work_directory_win,begin_date)
if not os.path.exists(file_name):
    fp = open(file_name, "w")
    fp.close()

def get_work_directory():
    if platform.system().lower() == "linux":
        return work_directory_linux
    return work_directory_win

def parse_xiangtan_time(time_msg):
    months = {"一月": 1, "二月": 2, "三月": 3, "四月": 4, "五月": 5, "六月": 6, "七月": 7, "八月": 8, "九月": 9,
              "十月": 10, "十一月": 11, "十二月": 12}
    rmatch = re.compile(r"['一','二','三','四', '五','六','七','八','九','十']*['月']{1} \d+, \d+")
    if rmatch.search(time_msg) is not None:
        month, day, year = time_msg.split(' ')
        month = months[month]
        day = day.strip(',')
        year, month, day = int(year), int(month), int(day)
        return datetime.date(year=year, month=month, day=day)
    return None


def delete_html(msg):
    return re.sub(r"<.*?>|&nbsp;|\n", "", msg)


def parse_time(time_str):
    year, month, day = time_str.split('-')
    year, month, day = int(year), int(month), int(day)
    return datetime.date(year, month, day)


def is_msg_exist(msg,today_contain):
    return msg in today_contain


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
                        "http://muchong.com/bbs/kaoyan.php?action=adjust&type=1&page=3&page=4"],
        "hangzhoushifan": "https://yjs.hznu.edu.cn/yjszs/sszs/",
        "xiangtandaxue": "https://jwxy.xtu.edu.cn/tzgg1/tzgg.htm",
        "yanshandaxue":"https://zsjyc.ysu.edu.cn/yjsxwz/sszs/szdong.htm",
        "hubeidaxue":"http://yz.hubu.edu.cn/zsxy/sszs.htm"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
        "Cookie": """SF_cookie_2 = 96816998;JSESSIONID = 6B67978CB3D33B9EA650A22C65F8F2CC"""
    }
    fp_r = open(file_name,"r")
    today_contain = fp_r.read()
    flag = True
    fp = open(file_name, "a")
    msg_to_write = ""

    # # 研招网查成绩
    # params = {"xm": "莫登意", "zjhm": "430105199806035615", "ksbh": "100133412881861", "bkdwdm": "10013"}
    # req = requests.post(url_dic["yanzhao"], params, headers=headers)
    # if "无查询结果" in req.text:
    #     wchannel.send("【研招网】成绩还查不到\n", get_mo_id())
    # else:
    #     wchannel.send("【研招网】成绩查到了！！\n", get_mo_id())

    # 广州大学方班最新消息
    req = requests.get(url_dic["fangban"], headers=headers)
    req.encoding = "utf-8"
    fangban_b = bs4.BeautifulSoup(req.text, "html.parser")
    for i in fangban_b.select("a > span"):
        mesg_date_str = re.findall(time_match, str(i.find_parent()))
        if mesg_date_str:
            mesg_date = parse_time(mesg_date_str[0])
            if mesg_date > begin_date:
                mesg = "【广州大学方班{}】有新消息{}\n".format(mesg_date,
                                                             re.sub(r"<.*?>|&nbsp;|\n", "", str(i.find_parent())))
                if not is_msg_exist(mesg,today_contain):
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
                if not is_msg_exist(mesg,today_contain):
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
            if not is_msg_exist(mesg,today_contain):
                flag = False
                msg_to_write = msg_to_write + mesg

    # 杭州师范大学
    # req = requests.get(url_dic["hangzhoushifan"], headers=headers)
    # req.encoding = "utf-8"
    # hangshifan = bs4.BeautifulSoup(req.text, "html.parser")
    # for i in hangshifan.find_all("a", attrs={"title": re.compile("^$")}):
    #     mesg_time = re.findall(time_match, str(i))[0]
    #     mesg = "【杭州师范大学{}】有新消息：{}\n".format(parse_time(mesg_time),
    #                                                   re.sub(r"<.*?>|&nbsp;|\n", "", str(i)))
    #     if not is_msg_exist(mesg,today_contain) and parse_time(mesg_time) >= begin_date:
    #         flag = False
    #         msg_to_write = msg_to_write + mesg

    # 湘潭大学
    requests.packages.urllib3.disable_warnings()
    req = requests.get(url_dic["xiangtandaxue"], headers=headers, verify=False)
    req.encoding = "utf-8"
    xiangtan_b = bs4.BeautifulSoup(req.text, "html.parser")
    for i in xiangtan_b.find_all("article", attrs={
        "class": "elementor-post elementor-grid-item post-2106 post type-post status-publish format-standard hentry category-36"}):
        msg_day = parse_xiangtan_time(delete_html(str(i.div.div)))
        if msg_day >= begin_date:
            msg = "【湘潭大学{}】{}\n".format(str(begin_date), delete_html(str(i)))
            if not is_msg_exist(msg,today_contain):
                flag = False
                msg_to_write = msg_to_write + msg

    # 燕山大学
    req = requests.get(url_dic["yanshandaxue"], headers=headers, verify=False)
    req.encoding = "utf-8"
    yanshan_b = bs4.BeautifulSoup(req.text, "html.parser")
    for i in yanshan_b.find_all("a", attrs={"target": "_blank", "class": ""}):
        year, month, day = delete_html(str(i.parent()[0])).strip().split('-')
        year, month, day = int(year), int(month), int(day)
        crawl_day = datetime.date(year, month, day)
        if crawl_day >= begin_date:
            msg = "【燕山大学{}】{}\n".format(begin_date, delete_html(str(i)).strip())
            if not is_msg_exist(msg, today_contain):
                msg_to_write = msg_to_write+msg

    # 湖北大学
    req = requests.get(url_dic['hubeidaxue'], headers=headers)
    req.encoding = "utf-8"
    hubeidaxue_b = bs4.BeautifulSoup(req.text, "html.parser")
    for i in hubeidaxue_b.find_all("a", attrs={'target': "_blank"}):
        if 'title' in i.attrs.keys():
            date = parse_time(re.findall(r'\d+-\d+-\d+',str(i.parent))[0])
            if date >= begin_date:
                msg = "【湖北大学{}】{}\n".format(str(date),delete_html(str(i)))
                if not is_msg_exist(msg, today_contain):
                    msg_to_write = msg_to_write + msg


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
                if not is_msg_exist(mesg,today_contain) and is_computer_science(mesg):
                    flag = False
                    msg_to_write = msg_to_write + mesg

    if not flag:
        fp.write(msg_to_write)
        msg_fp = open(get_work_directory()+"newmsg",'a')
        msg_fp.write(msg_to_write)
        wchannel.send(msg_to_write,get_mo_id())
    else:
        logger.info("正在爬取")
        wchannel.send("持续时间：{}分钟".format((time.time()-start_time)/60),get_mo_id())

    # TODO:研招网

    # TODO:中国教育在线
    return msg_to_write


def five_m_send():
    msg = crawl_msg()
    if msg:
        itchat.send(msg, toUserName=get_mo_id())
        wchannel.send(msg, get_mo_id())


def after_login():
    sched.add_job(five_m_send, "interval", minutes=3, max_instances=10)
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
