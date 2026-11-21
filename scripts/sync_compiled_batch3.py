# -*- coding: utf-8 -*-
"""同步次级页批次3：他人主页/活动日历/活动评价/举报/资料设置 五页到 mp-weixin 产物。"""
import os
import re

import sync_compiled_home as H
from sync_compiled_flow import to_native_page, compile_scss

ROOT = H.ROOT
DIST = H.DIST

PAGES = {
    "user-home": {"keys": ("statusBar", "following", "stats", "tags", "feeds"), "datai": ("openFeed",), "title": "个人主页"},
    "calendar": {"keys": ("statusBar", "weeks", "year", "month", "selected", "days", "schedules"), "datai": ("onDay",), "title": "我的日程"},
    "review": {"keys": ("statusBar", "rating", "stars", "ratingTexts", "tags", "content"), "datai": ("onRate", "onTag"), "title": "活动评价"},
    "report": {"keys": ("statusBar", "selected", "detail", "reasons"), "datai": ("onSelect",), "title": "举报"},
    "profile-setup": {"keys": ("statusBar", "step", "school", "nickname", "nickFirst", "interests"), "datai": ("onInterest",), "title": "完善资料"},
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
        # 受控输入 / confirm
        wxml = re.sub(r':value="([A-Za-z0-9_]+)"', r'value="{{\1}}"', wxml)
        wxml = re.sub(r'\s@input="([A-Za-z0-9_]+)"', r' bindinput="\1"', wxml)
        wxml = re.sub(r'\s@confirm="([A-Za-z0-9_]+)"', r' bindconfirm="\1"', wxml)
        open(os.path.join(out_dir, name + ".wxml"), "w", encoding="utf-8").write(wxml)

        # wxss
        tmp_s = os.path.join(ROOT, "_sync_b3.scss")
        tmp_c = os.path.join(ROOT, "_sync_b3.css")
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
    print("batch3 同步完成")


if __name__ == "__main__":
    main()
