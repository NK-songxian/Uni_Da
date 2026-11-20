# -*- coding: utf-8 -*-
"""
同步活动详情页源码到 mp-weixin 产物（HBuilderX 未重编时的桥接）
复用 sync_compiled_home 的 wxml 转换器 + sass 编译。
源码永远是 pages/activity-detail/activity-detail.vue。
"""
import os
import re
import subprocess

import sync_compiled_home as H

ROOT = H.ROOT
DIST = H.DIST
VUE = os.path.join(ROOT, "pages", "activity-detail", "activity-detail.vue")
OUT_DIR = os.path.join(DIST, "pages", "activity-detail")


def to_native_page(js):
    """Vue Options -> 原生 Page：data() 提到 data，methods 提升，computed pct 预置。"""
    # data() { return {...} } -> data: {...}
    js = re.sub(
        r"\bdata\(\)\s*\{\s*return (\{.*?\});\s*\},",
        lambda m: "data: " + m.group(1) + ",",
        js, flags=re.S)

    # computed 块整段删除（pct 直接写进 data 初值）
    js = re.sub(r"\n\s*computed:\s*\{.*?\n\s*\},", "", js, flags=re.S)

    # methods: { ... } 提升为 Page 顶层方法
    m = re.search(r"\t\tmethods:\s*\{(.*?)\n\t\t\}\n", js, re.S)
    if m:
        js = js[:m.start()] + m.group(1) + "\n\t\t" + js[m.end():]

    js = js.replace("export default {", "Page({")
    js = js.replace("uni.", "wx.")

    # data key 读取/写入转换（这里只有 statusBar / faved 会被 JS 写入）
    for k in ("statusBar", "faved", "joined", "total", "members"):
        # 读
        js = re.sub(r"\bthis\." + k + r"\b(?!\s*=)", "this.data." + k, js)
    # this.faved = !this.data.faved -> setData
    js = re.sub(
        r"this\.data\.faved\s*=\s*!this\.data\.faved;",
        "this.setData({ faved: !this.data.faved });", js)
    # onLoad 里 this.statusBar = (sys && ...) || 0; 整句赋值 -> setData
    # 用非贪婪匹配到分号，且表达式可能含 || 与括号
    js = re.sub(
        r"this\.statusBar\s*=\s*([^;]+);",
        lambda m: "this.setData({ statusBar: " + m.group(1).strip() + " });",
        js, count=1)

    # data 里插入 pct 初值（36/50 = 72）
    js = re.sub(r"data:\s*\{\s*statusBar:",
                "data: {\n\t\t\t\tpct: 72,\n\t\t\t\tstatusBar:", js, count=1)

    idx = js.rfind("};")
    if idx != -1:
        js = js[:idx] + "})" + js[idx + 2:]
    else:
        js = js.rstrip()
        if js.endswith("}"):
            js = js[:-1] + "})"
    return js


def main():
    vue = open(VUE, encoding="utf-8").read()
    os.makedirs(OUT_DIR, exist_ok=True)

    # ── wxml：先用通用转换器，再补活动详情特有的 :style width
    tpl = vue.split("<template>", 1)[1].rsplit("</template>", 1)[0]
    wxml = H.wxml_from_template(tpl)
    wxml = re.sub(
        r':style="\{\s*width:\s*([A-Za-z0-9_\.]+)\s*\+\s*\'%\'\s*\}"',
        lambda m: f'style="width:{{{{{m.group(1)}}}}}%"', wxml)
    open(os.path.join(OUT_DIR, "activity-detail.wxml"), "w", encoding="utf-8").write(wxml)

    # ── wxss：sass 编译
    scss = vue.split('<style lang="scss" scoped>')[1].split("</style>")[0]
    scss = scss.replace("@import '@/common/unida-tokens.scss';",
                        "@import '" + os.path.join(ROOT, "common", "unida-tokens.scss").replace("\\", "/") + "';")
    tmp = os.path.join(ROOT, "_sync_ad.scss")
    css = os.path.join(ROOT, "_sync_ad.css")
    open(tmp, "w", encoding="utf-8").write(scss)
    subprocess.run([r"C:\Users\Ryan\.workbuddy\binaries\node\versions\22.22.2-6\npx.cmd",
                    "--yes", "sass@1.77.8", "--no-source-map", tmp, css],
                   check=True, capture_output=True, shell=True)
    open(os.path.join(OUT_DIR, "activity-detail.wxss"), "w", encoding="utf-8").write(
        open(css, encoding="utf-8").read())
    os.remove(tmp); os.remove(css)

    # ── js
    js = vue.split("<script>")[1].split("</script>")[0]
    js = to_native_page(js)
    open(os.path.join(OUT_DIR, "activity-detail.js"), "w", encoding="utf-8").write(js)

    # ── json（自定义导航 + 沉浸式封面，无 tabbar）
    open(os.path.join(OUT_DIR, "activity-detail.json"), "w", encoding="utf-8").write(
        """{
  "navigationBarTitleText": "活动详情",
  "navigationStyle": "custom",
  "backgroundColor": "#F5F0FF",
  "backgroundTextStyle": "dark",
  "usingComponents": {}
}
""")

    H.sync_static()
    print("已同步活动详情页：activity-detail.wxml / wxss / js / json")


if __name__ == "__main__":
    main()
