import base64
import time
import os

import execjs
import requests

from dotenv import load_dotenv

# 1. 加载 .env 文件到 Python
load_dotenv()
os.environ["s"] = os.getenv("s", "")


now = int(time.time() * 1000)
js_code = open("05加解密函数.js").read()
js_compile = execjs.compile(js_code)
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://ggzyfw.fujian.gov.cn',
    'Referer': 'https://ggzyfw.fujian.gov.cn/business/list',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0',
    'portal-sign': 'ea3391ee5168700add4e5b8891ac5770',
    'sec-ch-ua': '"Microsoft Edge";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
for page in range(1,11):
    json_data = {
        'pageNo': 2,
        'pageSize': 1,
        'total': 2707,
        'AREACODE': '',
        'M_PROJECT_TYPE': '',
        'KIND': 'GCJS',
        'GGTYPE': '1',
        'PROTYPE': '',
        'timeType': '6',
        'BeginTime': '2025-10-23 00:00:00',
        'EndTime': '2026-04-23 23:59:59',
        'createTime': '',
        'ts': now,
    }
    sign = js_compile.call("encrypt",json_data)
    headers["portal-sign"] = sign
    response = requests.post('https://ggzyfw.fujian.gov.cn/FwPortalApi/Trade/TradeInfo', headers=headers, json=json_data)
    # print(response.text)
    data_encrypt_bas64 = response.json().get("Data")

    data = js_compile.call("decrypt", data_encrypt_bas64)
    print(data)
    print("========================================================================")
    time.sleep(1)