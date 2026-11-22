# -*- coding: utf-8 -*-
"""校验：用 AppID + AppSecret 换 access_token，判断凭证是否配套。
用法：E:/anaco/envs/sam_gpu/python.exe scripts/verify_wx_secret.py
密钥从本地配置读取，脚本本身不含明文；换 secret 后重跑即可复验。
返回 40125 = invalid appsecret（不配套/已重置），0 正常。"""
import json
import re
import sys
import urllib.parse
import urllib.request

CONF = r"H:\UniDA\unida\uniCloud-alipay\cloudfunctions\common\uni-config-center\index.js"

with open(CONF, encoding="utf-8") as f:
    s = f.read()

appid = re.search(r"appid:\s*'([^']+)'", s).group(1)
secret = re.search(r"appsecret:\s*'([^']+)'", s).group(1)

print("AppID:", appid)
print("Secret:", secret[:4] + "****" + secret[-4:] + "  len=" + str(len(secret)))

url = (
    "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
    + "&appid=" + urllib.parse.quote(appid)
    + "&secret=" + urllib.parse.quote(secret)
)

import ssl

ctx = ssl._create_unverified_context()
try:
    resp = urllib.request.urlopen(url, timeout=10, context=ctx).read().decode("utf-8")
    data = json.loads(resp)
    if "access_token" in data:
        print("RESULT: OK")
        print("  => appid 与 secret 配套，凭证正确")
        print("  expires_in:", data.get("expires_in"), "秒")
    else:
        print("RESULT: FAIL")
        print("  errcode:", data.get("errcode"))
        print("  errmsg:", data.get("errmsg"))
except urllib.error.HTTPError as e:
    print("HTTP_ERROR:", e.code, e.read().decode("utf-8", "ignore"))
except Exception as e:
    print("REQUEST_ERROR:", type(e).__name__, str(e))
