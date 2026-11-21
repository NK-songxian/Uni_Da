# -*- coding: utf-8 -*-
"""同步收尾批次：用户协议/微信登录/手机登录/旧入口页 四页到 mp-weixin 产物。"""
import os
import re

import sync_compiled_home as H
from sync_compiled_flow import to_native_page, compile_scss

ROOT = H.ROOT
DIST = H.DIST

PAGES = {
    "agreement": {"keys": ("statusBar", "title", "clauses"), "datai": (), "title": "用户协议"},
    "login-wechat": {"keys": ("statusBar", "agreed", "features"), "datai": (), "title": "微信登录"},
    "phone-login": {"keys": ("statusBar", "phone", "code", "codeText", "counting", "agreed"), "datai": (), "title": "手机号登录"},
    "index": {"keys": ("statusBar", "features"), "datai": (), "title": "有你搭"},
}


def main():
    for name, cfg in PAGES.items():
        vue_path = os.path.join(ROOT, "pages", name, name + ".vue")
        vue = open(vue_path, encoding="utf-8").read()
        out_dir = os.path.join(DIST, "pages", name)
        os.makedirs(out_dir, exist_ok=True)

        # wxml
        tpl = vue.split("<template>", 1)[1].rsplit("</template>", 1)[0]
        wxml = H.wxml_from_template(tpl)
        for dn in cfg["datai"]:
            wxml = re.sub(r'((?:bind|catch)tap="%s")' % dn, r'\1 data-i="{{i}}"', wxml)
        # 受控输入 / 微信开放能力
        wxml = re.sub(r':value="([A-Za-z0-9_]+)"', r'value="{{\1}}"', wxml)
        wxml = re.sub(r'\s@input="([A-Za-z0-9_]+)"', r' bindinput="\1"', wxml)
        wxml = re.sub(r'\s@getphonenumber="([A-Za-z0-9_]+)"', r' bindgetphonenumber="\1"', wxml)
        open(os.path.join(out_dir, name + ".wxml"), "w", encoding="utf-8").write(wxml)

        # wxss
        tmp_s = os.path.join(ROOT, "_sync_b4.scss")
        tmp_c = os.path.join(ROOT, "_sync_b4.css")
        compile_scss(vue, os.path.join(out_dir, name + ".wxss"), tmp_s, tmp_c)

        # js
        js = vue.split("<script>")[1].split("</script>")[0]
        open(os.path.join(out_dir, name + ".js"), "w", encoding="utf-8").write(to_native_page(js, cfg["keys"]))

        # json
        open(os.path.join(out_dir, name + ".json"), "w", encoding="utf-8").write(
            '{\n  "navigationBarTitleText": "%s",\n  "navigationStyle": "custom",\n'
            '  "backgroundColor": "#F5F0FF",\n  "backgroundTextStyle": "dark",\n'
            '  "usingComponents": {}\n}\n' % cfg["title"])
        print("已同步", name)

    H.sync_static()
    print("batch4 同步完成")


if __name__ == "__main__":
    main()
