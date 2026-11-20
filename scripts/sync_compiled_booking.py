# -*- coding: utf-8 -*-
"""
同步报名链路两页（booking-confirm / booking-success）到 mp-weixin 产物。
复用 sync_compiled_home 的 wxml 转换器 + sass 编译。
特例：textarea 的 value/bindinput、嵌套 paddingTop 表达式、count += 1 复合赋值。
"""
import os
import re
import subprocess

import sync_compiled_home as H

ROOT = H.ROOT
DIST = H.DIST

PAGES = [
    ("booking-confirm", "pages/booking-confirm/booking-confirm.vue", "报名确认", 0),
    ("booking-success", "pages/booking-success/booking-success.vue", "报名成功", 1),
]


def to_native_page(js, data_keys, extra_data=None):
    """Vue Options -> 原生 Page（支持 = / += / -= 三种写数据）"""
    # data() { return {...} }; -> data: {...},
    js = re.sub(
        r"\bdata\(\)\s*\{\s*return (\{.*?\});\s*\},",
        lambda m: "data: " + m.group(1) + ",",
        js, flags=re.S)

    # methods 提升
    m = re.search(r"\t\tmethods:\s*\{(.*?)\n\t\t\}\n", js, re.S)
    if m:
        js = js[:m.start()] + m.group(1) + "\n\t\t" + js[m.end():]

    js = js.replace("export default {", "Page({")
    js = js.replace("uni.", "wx.")

    # 读：this.X -> this.data.X（不排除赋值左值，先统一转，再由下面写转换接住）
    for k in data_keys:
        js = re.sub(r"\bthis\." + k + r"\b", "this.data." + k, js)

    # 写：复合赋值优先
    for k in data_keys:
        js = re.sub(
            r"(?P<pre>^|[^.\w])this\.data\." + k + r"\s*\+=\s*(?P<expr>[^;]+);",
            lambda mm, kk=k: mm.group("pre") + "this.setData({ " + kk + ": this.data." + kk + " + (" + mm.group("expr").strip() + ") });",
            js, flags=re.M)
        js = re.sub(
            r"(?P<pre>^|[^.\w])this\.data\." + k + r"\s*-=\s*(?P<expr>[^;]+);",
            lambda mm, kk=k: mm.group("pre") + "this.setData({ " + kk + ": this.data." + kk + " - (" + mm.group("expr").strip() + ") });",
            js, flags=re.M)
        js = re.sub(
            r"(?P<pre>^|[^.\w])this\.data\." + k + r"\s*=\s*(?P<expr>[^;]+);",
            lambda mm, kk=k: mm.group("pre") + "this.setData({ " + kk + ": " + mm.group("expr").strip() + " });",
            js, flags=re.M)

    # 补插 data 初值
    if extra_data:
        js = re.sub(r"data:\s*\{", "data: {\n\t\t\t\t" + extra_data + ",", js, count=1)

    idx = js.rfind("};")
    if idx != -1:
        js = js[:idx] + "})" + js[idx + 2:]
    else:
        js = js.rstrip()
        if js.endswith("}"):
            js = js[:-1] + "})"
    return js


def main():
    for name, rel, title, _ in PAGES:
        vue = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        out_dir = os.path.join(DIST, "pages", name)
        os.makedirs(out_dir, exist_ok=True)

        # ── wxml
        tpl = vue.split("<template>", 1)[1].rsplit("</template>", 1)[0]
        wxml = H.wxml_from_template(tpl)
        # 嵌套 paddingTop 表达式：(statusBar + 60) + 'px'
        wxml = re.sub(
            r':style="\{\s*paddingTop:\s*\(([^)]+)\)\s*\+\s*\'px\'\s*\}"',
            lambda m: f'style="padding-top:{{{{{m.group(1)}}}}}px"', wxml)
        # 简单 paddingTop（已由转换器处理，这里兜底）
        wxml = re.sub(
            r':style="\{\s*paddingTop:\s*([A-Za-z0-9_\.]+)\s*\+\s*\'px\'\s*\}"',
            lambda m: f'style="padding-top:{{{{{m.group(1)}}}}}px"', wxml)
        # textarea：:value -> value，@input -> bindinput
        wxml = re.sub(r'\s:value="([^"]+)"', lambda m: f' value="{{{{{m.group(1)}}}}}"', wxml)
        wxml = re.sub(r'\s@input="([^"]+)"', lambda m: f' bindinput="{m.group(1)}"', wxml)
        open(os.path.join(out_dir, name + ".wxml"), "w", encoding="utf-8").write(wxml)

        # ── wxss（sass）
        scss = vue.split('<style lang="scss" scoped>')[1].split("</style>")[0]
        scss = scss.replace("@import '@/common/unida-tokens.scss';",
                            "@import '" + os.path.join(ROOT, "common", "unida-tokens.scss").replace("\\", "/") + "';")
        tmp = os.path.join(ROOT, "_sync_" + name.replace("-", "_") + ".scss")
        css = os.path.join(ROOT, "_sync_" + name.replace("-", "_") + ".css")
        open(tmp, "w", encoding="utf-8").write(scss)
        subprocess.run([r"C:\Users\Ryan\.workbuddy\binaries\node\versions\22.22.2-6\npx.cmd",
                        "--yes", "sass@1.77.8", "--no-source-map", tmp, css],
                       check=True, capture_output=True, shell=True)
        open(os.path.join(out_dir, name + ".wxss"), "w", encoding="utf-8").write(
            open(css, encoding="utf-8").read())
        os.remove(tmp); os.remove(css)

        # ── js
        js = vue.split("<script>")[1].split("</script>")[0]
        keys = re.findall(r"^\t\t\t\t([A-Za-z_][A-Za-z0-9_]*)\s*:", js, re.M)
        js = to_native_page(js, keys)
        open(os.path.join(out_dir, name + ".js"), "w", encoding="utf-8").write(js)

        # ── json
        open(os.path.join(out_dir, name + ".json"), "w", encoding="utf-8").write(
            '{\n  "navigationBarTitleText": "%s",\n  "navigationStyle": "custom",\n'
            '  "backgroundColor": "#F5F0FF",\n  "backgroundTextStyle": "dark",\n'
            '  "usingComponents": {}\n}\n' % title)

        print("已同步", name)

    H.sync_static()


if __name__ == "__main__":
    main()
