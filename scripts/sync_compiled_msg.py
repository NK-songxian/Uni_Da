# -*- coding: utf-8 -*-
"""同步消息页 V2（设计稿版）到 mp-weixin 产物。"""
import os
import re

import sync_compiled_home as H
from sync_compiled_flow import to_native_page, compile_scss

ROOT = H.ROOT
DIST = H.DIST
NAME = "message"
KEYS = ("statusBar", "active", "tabs", "chats")
DATA_I = ("onTab", "onChat", "onSystem")


def main():
    vue = open(os.path.join(ROOT, "pages", NAME, NAME + ".vue"), encoding="utf-8").read()
    out_dir = os.path.join(DIST, "pages", NAME)
    os.makedirs(out_dir, exist_ok=True)

    # wxml
    tpl = vue.split("<template>", 1)[1].rsplit("</template>", 1)[0]
    wxml = H.wxml_from_template(tpl)
    for dn in DATA_I:
        wxml = re.sub(r'((?:bind|catch)tap="%s")' % dn, r'\1 data-i="{{i}}"', wxml)
    # tabbar：设计稿消息角标 15
    wxml = re.sub(r'<unida-tabbar[^>]*/>', '<unida-tabbar selected="{{3}}" unread-count="{{15}}" />', wxml)
    open(os.path.join(out_dir, NAME + ".wxml"), "w", encoding="utf-8").write(wxml)

    # wxss
    tmp_s = os.path.join(ROOT, "_sync_msg.scss")
    tmp_c = os.path.join(ROOT, "_sync_msg.css")
    compile_scss(vue, os.path.join(out_dir, NAME + ".wxss"), tmp_s, tmp_c)

    # js
    js = vue.split("<script>")[1].split("</script>")[0]
    open(os.path.join(out_dir, NAME + ".js"), "w", encoding="utf-8").write(to_native_page(js, KEYS))

    # json
    open(os.path.join(out_dir, NAME + ".json"), "w", encoding="utf-8").write(
        '{\n  "navigationBarTitleText": "消息",\n  "navigationStyle": "custom",\n'
        '  "backgroundColor": "#F5F0FF",\n  "backgroundTextStyle": "dark",\n'
        '  "usingComponents": {\n    "unida-tabbar": "../../components/unida-tabbar/unida-tabbar"\n  }\n}\n')

    H.sync_static()
    print("消息页 V2 已同步")


if __name__ == "__main__":
    main()
