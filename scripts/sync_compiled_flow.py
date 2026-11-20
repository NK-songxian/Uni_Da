# -*- coding: utf-8 -*-
"""同步消息/会话/跑腿大厅/跑腿详情 四页到 mp-weixin 产物。"""
import os
import re
import subprocess

import sync_compiled_home as H

ROOT = H.ROOT
DIST = H.DIST

PAGES = {
    "message": {"keys": ("statusBar", "notices", "chats"), "datai": ("onNotice", "onChat"), "tab": 3},
    "chat": {"keys": ("statusBar", "peerName", "text", "scrollTop", "emojis", "msgs"), "datai": ("onEmoji",), "tab": None},
    "errand-hall": {"keys": ("statusBar", "cats", "orders"), "datai": ("onCat", "onOrder"), "tab": 1},
    "errand-detail": {"keys": ("statusBar", "steps", "activeStep"), "datai": (), "tab": None},
}


def to_native_page(js, keys):
    js = re.sub(r"\bdata\(\)\s*\{\s*return (\{.*?\});\s*\},",
                lambda m: "data: " + m.group(1) + ",", js, flags=re.S)
    m = re.search(r"\t\tmethods:\s*\{(.*?)\n\t\t\}\n", js, re.S)
    if m:
        js = js[:m.start()] + m.group(1) + "\n\t\t" + js[m.end():]
    js = js.replace("export default {", "Page({")
    js = js.replace("uni.", "wx.")
    js = js.replace("import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';", "")
    js = re.sub(r"components:\s*\{[^}]*\},", "components: {},", js)
    for k in keys:
        js = re.sub(r"\bthis\." + k + r"\b", "this.data." + k, js)
    for k in keys:
        js = re.sub(
            r"(?P<pre>^|[^.\w])this\.data\." + k + r"\s*=\s*(?P<expr>[^;]+);",
            lambda mm, kk=k: mm.group("pre") + "this.setData({ " + kk + ": " + mm.group("expr").strip() + " });",
            js, flags=re.M)
    idx = js.rfind("};")
    js = js[:idx] + "})" + js[idx + 2:]
    return js


def compile_scss(vue, out_path, scss_tmp, css_tmp):
    scss = vue.split('<style lang="scss" scoped>')[1].split("</style>")[0]
    scss = scss.replace("@import '@/common/unida-tokens.scss';",
                        "@import '" + os.path.join(ROOT, "common", "unida-tokens.scss").replace("\\", "/") + "';")
    scss = scss.replace("@import '@/common/unida-global.scss';",
                        "@import '" + os.path.join(ROOT, "common", "unida-global.scss").replace("\\", "/") + "';")
    open(scss_tmp, "w", encoding="utf-8").write(scss)
    subprocess.run([r"C:\Users\Ryan\.workbuddy\binaries\node\versions\22.22.2-6\npx.cmd",
                    "--yes", "sass@1.77.8", "--no-source-map", scss_tmp, css_tmp],
                   check=True, capture_output=True, shell=True)
    open(out_path, "w", encoding="utf-8").write(open(css_tmp, encoding="utf-8").read())
    os.remove(scss_tmp)
    os.remove(css_tmp)


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
            wxml = wxml.replace('bindtap="%s"' % dn, 'bindtap="%s" data-i="{{i}}"' % dn)
        # 受控输入 / scroll-top / confirm / focus
        wxml = re.sub(r':value="([A-Za-z0-9_]+)"', r'value="{{\1}}"', wxml)
        wxml = re.sub(r'\s@input="([A-Za-z0-9_]+)"', r' bindinput="\1"', wxml)
        wxml = re.sub(r':scroll-top="([A-Za-z0-9_]+)"', r'scroll-top="{{\1}}"', wxml)
        wxml = re.sub(r'\s@confirm="([A-Za-z0-9_]+)"', r' bindconfirm="\1"', wxml)
        wxml = re.sub(r'\s@focus="([A-Za-z0-9_]+)"', r' bindfocus="\1"', wxml)
        if cfg["tab"] is not None:
            wxml = re.sub(r'<unida-tabbar[^>]*/>',
                          '<unida-tabbar selected="{{%d}}" unread-count="{{3}}" />' % cfg["tab"], wxml)
        open(os.path.join(out_dir, name + ".wxml"), "w", encoding="utf-8").write(wxml)

        # wxss
        tmp_s = os.path.join(ROOT, "_sync_flow.scss")
        tmp_c = os.path.join(ROOT, "_sync_flow.css")
        compile_scss(vue, os.path.join(out_dir, name + ".wxss"), tmp_s, tmp_c)

        # js
        js = vue.split("<script>")[1].split("</script>")[0]
        open(os.path.join(out_dir, name + ".js"), "w", encoding="utf-8").write(to_native_page(js, cfg["keys"]))

        # json
        comps = {}
        if "unidaTabbar" in vue:
            comps["unida-tabbar"] = "../../components/unida-tabbar/unida-tabbar"
        if "unidaSearch" in vue:
            comps["unida-search"] = "../../components/unida-search/unida-search"
        comp_json = ",\n".join('    "%s": "%s"' % (k, v) for k, v in comps.items())
        comp_block = ("  \"usingComponents\": {\n" + comp_json + "\n  }\n") if comps else "  \"usingComponents\": {}\n"
        open(os.path.join(out_dir, name + ".json"), "w", encoding="utf-8").write(
            '{\n  "navigationBarTitleText": "%s",\n  "navigationStyle": "custom",\n'
            '  "backgroundColor": "#F5F0FF",\n  "backgroundTextStyle": "dark",\n%s}\n'
            % ({"message": "消息", "chat": "搭子会话", "errand-hall": "跑腿大厅", "errand-detail": "跑腿详情"}[name], comp_block))
        print("已同步", name)

    H.sync_static()


if __name__ == "__main__":
    main()
