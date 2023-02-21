import requests
if __name__ == '__main__':
    url = "https://yz.chsi.com.cn/apply/cjcx/cjcx.do"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
        "Cookie": """SF_cookie_2 = 96816998;JSESSIONID = 6B67978CB3D33B9EA650A22C65F8F2CC"""
    }
    params = {"xm": "莫登意", "zjhm": "430105199806035615", "ksbh": "100133412881861", "bkdwdm": "10013"}
    req = requests.post(url, params, headers=headers)
    print(req.text)