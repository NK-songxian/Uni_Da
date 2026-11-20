# -*- coding: utf-8 -*-
"""同步次级页批次：签到/积分/积分商城/社区/帖子详情 五页到 mp-weixin 产物。"""
import os
import re

import sync_compiled_home as H
from sync_compiled_flow import to_native_page, compile_scss

ROOT = H.ROOT
DIST = H.DIST

PAGES = {
    "checkin": {"keys": ("statusBar",), "datai": (), "tab": None, "title": "每日签到"},
    "points": {"keys": ("statusBar", "tasks"), "datai": ("onTask",), "tab": None, "title": "积分中心"},
    "points-mall": {"keys": ("statusBar", "cats", "active", "goods"), "datai": ("onCat", "onExchange"), "tab": None, "title": "积分商城"},
    "community": {"keys": ("statusBar", "tabs", "active", "posts"), "datai": ("onTab", "openPost", "onLike", "onComment", "onFav", "onShare"), "tab": 1, "title": "社区"},
    "post-detail": {"keys": ("statusBar", "following", "likes", "favs", "comment", "grads", "comments"), "datai": (), "tab": None, "title": "帖子详情"},
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
            # v-for 下标参数：bindtap / catchtap 两种事件都补 data-i
            wxml = re.sub(r'((?:bind|catch)tap="%s")' % dn, r'\1 data-i="{{i}}"', wxml)
        # 受控输入 / confirm
        wxml = re.sub(r':value="([A-Za-z0-9_]+)"', r'value="{{\1}}"', wxml)
        wxml = re.sub(r'\s@input="([A-Za-z0-9_]+)"', r' bindinput="\1"', wxml)
        wxml = re.sub(r'\s@confirm="([A-Za-z0-9_]+)"', r' bindconfirm="\1"', wxml)
        if cfg["tab"] is not None:
            wxml = re.sub(r'<unida-tabbar[^>]*/>',
                          '<unida-tabbar selected="{{%d}}" />' % cfg["tab"], wxml)
        open(os.path.join(out_dir, name + ".wxml"), "w", encoding="utf-8").write(wxml)

        # wxss
        tmp_s = os.path.join(ROOT, "_sync_b2.scss")
        tmp_c = os.path.join(ROOT, "_sync_b2.css")
        compile_scss(vue, os.path.join(out_dir, name + ".wxss"), tmp_s, tmp_c)

        # js
        js = vue.split("<script>")[1].split("</script>")[0]
        open(os.path.join(out_dir, name + ".js"), "w", encoding="utf-8").write(to_native_page(js, cfg["keys"]))

        # json
        comps = {}
        if "unidaTabbar" in vue:
            comps["unida-tabbar"] = "../../components/unida-tabbar/unida-tabbar"
        comp_json = ",\n".join('    "%s": "%s"' % (k, v) for k, v in comps.items())
        comp_block = ("  \"usingComponents\": {\n" + comp_json + "\n  }\n") if comps else "  \"usingComponents\": {}\n"
        open(os.path.join(out_dir, name + ".json"), "w", encoding="utf-8").write(
            '{\n  "navigationBarTitleText": "%s",\n  "navigationStyle": "custom",\n'
            '  "backgroundColor": "#F5F0FF",\n  "backgroundTextStyle": "dark",\n%s}\n'
            % (cfg["title"], comp_block))
        print("已同步", name)

    H.sync_static()
    print("batch2 同步完成")


if __name__ == "__main__":
    main()
