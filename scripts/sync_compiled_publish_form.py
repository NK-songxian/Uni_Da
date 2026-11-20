# -*- coding: utf-8 -*-
"""同步发布表单页（publish-form）到 mp-weixin 产物。特例：input/textarea 受控、chip 选择事件。"""
import os
import re
import subprocess

import sync_compiled_home as H

ROOT = H.ROOT
DIST = H.DIST
VUE = os.path.join(ROOT, "pages", "publish-form", "publish-form.vue")
OUT_DIR = os.path.join(DIST, "pages", "publish-form")
DATA_KEYS = ("statusBar", "typeList", "places", "fees", "quicks", "quickIdx",
             "title", "desc", "type", "time", "place", "total", "fee", "feeText")


def to_native_page(js):
    js = re.sub(r"\bdata\(\)\s*\{\s*return (\{.*?\});\s*\},",
                lambda m: "data: " + m.group(1) + ",", js, flags=re.S)
    m = re.search(r"\t\tmethods:\s*\{(.*?)\n\t\t\}\n", js, re.S)
    if m:
        js = js[:m.start()] + m.group(1) + "\n\t\t" + js[m.end():]
    js = js.replace("export default {", "Page({")
    js = js.replace("uni.", "wx.")
    # 先全量转读，再统一转写
    for k in DATA_KEYS:
        js = re.sub(r"\bthis\." + k + r"\b", "this.data." + k, js)
    for k in DATA_KEYS:
        js = re.sub(
            r"(?P<pre>^|[^.\w])this\.data\." + k + r"\s*=\s*(?P<expr>[^;]+);",
            lambda mm, kk=k: mm.group("pre") + "this.setData({ " + kk + ": " + mm.group("expr").strip() + " });",
            js, flags=re.M)
    idx = js.rfind("};")
    js = js[:idx] + "})" + js[idx + 2:]
    return js


def main():
    vue = open(VUE, encoding="utf-8").read()
    os.makedirs(OUT_DIR, exist_ok=True)

    tpl = vue.split("<template>", 1)[1].rsplit("</template>", 1)[0]
    wxml = H.wxml_from_template(tpl)
    # 带下标事件补 data-i
    for name in ("onType", "onPlace", "onFee", "onQuick"):
        wxml = wxml.replace('bindtap="%s"' % name, 'bindtap="%s" data-i="{{i}}"' % name)
    # 受控 input/textarea：:value/@input → value/bindinput
    wxml = re.sub(r':value="([A-Za-z0-9_]+)"', r'value="{{\1}}"', wxml)
    wxml = re.sub(r'\s@input="([A-Za-z0-9_]+)"', r' bindinput="\1"', wxml)
    wxml = wxml.replace("/>", ">").replace("</textarea>", "</textarea>") if False else wxml
    open(os.path.join(OUT_DIR, "publish-form.wxml"), "w", encoding="utf-8").write(wxml)

    scss = vue.split('<style lang="scss" scoped>')[1].split("</style>")[0]
    scss = scss.replace("@import '@/common/unida-tokens.scss';",
                        "@import '" + os.path.join(ROOT, "common", "unida-tokens.scss").replace("\\", "/") + "';")
    tmp = os.path.join(ROOT, "_sync_pf.scss")
    css = os.path.join(ROOT, "_sync_pf.css")
    open(tmp, "w", encoding="utf-8").write(scss)
    subprocess.run([r"C:\Users\Ryan\.workbuddy\binaries\node\versions\22.22.2-6\npx.cmd",
                    "--yes", "sass@1.77.8", "--no-source-map", tmp, css],
                   check=True, capture_output=True, shell=True)
    open(os.path.join(OUT_DIR, "publish-form.wxss"), "w", encoding="utf-8").write(open(css, encoding="utf-8").read())
    os.remove(tmp); os.remove(css)

    js = to_native_page(vue.split("<script>")[1].split("</script>")[0])
    open(os.path.join(OUT_DIR, "publish-form.js"), "w", encoding="utf-8").write(js)

    open(os.path.join(OUT_DIR, "publish-form.json"), "w", encoding="utf-8").write(
        '{\n  "navigationBarTitleText": "发布活动",\n  "navigationStyle": "custom",\n'
        '  "backgroundColor": "#F5F0FF",\n  "backgroundTextStyle": "dark",\n'
        '  "usingComponents": {}\n}\n')

    H.sync_static()
    print("已同步 publish-form")


if __name__ == "__main__":
    main()
