import requests
import json
import hashlib
import time
import os
from dotenv import load_dotenv
from Crypto.Cipher import AES
import base64
# 加载环境变量
load_dotenv()

# 从 .env 读取
key = os.getenv("KEY")
iv = os.getenv("IV")
d = os.getenv("s")
now = int(time.time() * 1000)
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

json_data = {
    'pageNo': 2,
    'pageSize': 20,
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


# 对应 JS 的 l 函数：不区分大小写排序比较
def l(t, e):
    t_str = str(t).upper()
    e_str = str(e).upper()
    if t_str > e_str:
        return 1
    elif t_str == e_str:
        return 0
    else:
        return -1

# 对应 JS 的 u 函数：排序 + 拼接字符串
def u(t):
    # 按 JS 规则排序 key
    keys = sorted(t.keys(), key=lambda x: (str(x).upper(),))
    n = ""
    for key in keys:
        val = t[key]
        if val is None:
            continue
        # 如果是对象/数组 → JSON.stringify
        if isinstance(val, (dict, list)):
            i = json.dumps(val, ensure_ascii=False)
            n += key + i
        else:
            n += key + str(val)
    return n

# 对应 JS 的 encrypt 函数（最终签名）
def encrypt(t):
    # 第一步：过滤空值和 undefined
    filtered = {}
    for k, v in t.items():
        if v != "" and v is not None:
            filtered[k] = v

    # 固定密钥 + 拼接排序后的字符串
    raw_str = d + u(filtered)

    # MD5 小写
    return hashlib.md5(raw_str.encode('utf-8')).hexdigest().lower()
sign = encrypt(json_data)
headers["portal-sign"] = sign

response = requests.post('https://ggzyfw.fujian.gov.cn/FwPortalApi/Trade/TradeInfo', headers=headers, json=json_data)
data_encrypt_bas64 = response.json().get("Data")
key = key.encode()
iv = iv.encode()
aes = AES.new(key, AES.MODE_CBC, iv)
data_encrypt = base64.b64decode(data_encrypt_bas64)
data = aes.decrypt(data_encrypt).decode()
print(data)

