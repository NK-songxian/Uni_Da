# -*- coding: utf-8 -*-
"""
同步发现页源码到 mp-weixin 产物（复用 home 同步脚本的转换器）
===================================================================
HBuilderX 未重新编译时的临时桥接。源码永远是 pages/discover/discover.vue。
"""
import os
import re
import subprocess

import sync_compiled_home as H

ROOT = H.ROOT
DIST = H.DIST
VUE = os.path.join(ROOT, "pages", "discover", "discover.vue")
API = os.path.join(ROOT, "common", "api", "discover.js")

OUT_DIR = os.path.join(DIST, "pages", "discover")


def api_commonjs(src):
    import sync_cloud
    s = sync_cloud.patch_api_imports(src)
    s = s.replace("export async function ", "async function ")
    s = s.replace("export function ", "function ")
    s = s.replace("export const ", "const ")
    s += "\nmodule.exports = { fetchDiscover, DISCOVER_FILTERS, setDiscoverFail };\n"
    return s


def to_native_page(js):
    """与 home 版相同：this.xxx -> this.data.xxx + setData；reqId 作普通属性。"""
    m = re.search(r"(\bdata:\s*\{)(.*?)(\n\s*\},)", js, re.S)
    if not m:
        return js
    keys = re.findall(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:", m.group(2), re.M)
    keys = [k for k in keys if k != "reqId"]
    head, rest = js[:m.end()], js[m.end():]
    for k in keys:
        rest = re.sub(r"\bthis\." + re.escape(k) + r"\b", "this.data." + k, rest)
    for k in keys:
        pat = re.compile(
            r"(?P<pre>^|[^.\w])this\.data\." + re.escape(k) + r"\s*=\s*(?P<expr>[^;]+);", re.M)
        def repl(mm):
            return mm.group("pre") + "this.setData({ " + k + ": " + mm.group("expr").strip() + " });"
        rest = pat.sub(repl, rest)
    # reqId 没被转换，是普通实例属性，在 onLoad 里初始化
    rest = rest.replace("\t\tonLoad() {", "\t\tonLoad() {\n\t\t\tthis.reqId = 0;", 1)
    # 带参事件（onMainTab/onChip/onSort）在 WXML 里改成 data-i 传值，
    # 这里把方法入参从数字 i 改为从 event.dataset 读取，兼容原来的方法体
    for name in ("onMainTab", "onChip", "onSort"):
        rest = re.sub(
            r"(" + name + r"\()(i)(\)\s*\{)",
            lambda m, n=name: n + "(e) {\n\t\t\t\tconst i = Number(e.currentTarget.dataset.i);",
            rest,
            count=1
        )
    return head + rest


def main():
    vue = open(VUE, encoding="utf-8").read()
    os.makedirs(OUT_DIR, exist_ok=True)

    # ── wxml
    tpl = vue.split("<template>", 1)[1].rsplit("</template>", 1)[0]
    # 发现页的 v-for 用 (item, i) in feedList，home 转换器已支持
    # 但 skeletonNums 的 v-for="i in 4" 需要骨架数组
    wxml = H.wxml_from_template(tpl)
    # home 转换器未覆盖本页 3 处 :style（borderColor / 条件价格色），
    # 不补会在真机丢色。补成 WXML 静态插值，避免 :style 原样残留。
    wxml = wxml.replace(':style="{ borderColor: item.bar }"', 'style="border-color:{{item.bar}}"')
    wxml = wxml.replace(':style="{ color: item.bar }"', 'style="color:{{item.bar}}"')
    wxml = wxml.replace(
        ':style="{ color: item.price === \'免费\' ? \'#29CA83\' : item.bar }"',
        'style="color:{{item.price === \'免费\' ? \'#29CA83\' : item.bar}}"')
    # 转换器对无属性链的事件参数（onCardTap(item)）会直接丢弃，
    # 详情页需要 id，这里单独补 data-id；home 页的 onCardTap 不用参数，不受影响。
    wxml = wxml.replace('bindtap="onCardTap"', 'bindtap="onCardTap" data-id="{{item.id}}"')
    open(os.path.join(OUT_DIR, "discover.wxml"), "w", encoding="utf-8").write(wxml)

    # ── wxss
    scss = vue.split('<style lang="scss" scoped>')[1].split("</style>")[0]
    scss = scss.replace("@import '@/common/unida-tokens.scss';",
                        "@import '" + os.path.join(ROOT, "common", "unida-tokens.scss").replace("\\", "/") + "';")
    tmp = os.path.join(ROOT, "_sync_disc.scss")
    css = os.path.join(ROOT, "_sync_disc.css")
    open(tmp, "w", encoding="utf-8").write(scss)
    subprocess.run([r"C:\Users\Ryan\.workbuddy\binaries\node\versions\22.22.2-6\npx.cmd",
                    "--yes", "sass@1.77.8", "--no-source-map", tmp, css],
                   check=True, capture_output=True, shell=True)
    open(os.path.join(OUT_DIR, "discover.wxss"), "w", encoding="utf-8").write(
        open(css, encoding="utf-8").read())
    os.remove(tmp); os.remove(css)

    # ── api
    os.makedirs(os.path.join(DIST, "common", "api"), exist_ok=True)
    open(os.path.join(DIST, "common", "api", "discover.js"), "w", encoding="utf-8").write(
        api_commonjs(open(API, encoding="utf-8").read()))

    # ── js
    js = vue.split("<script>")[1].split("</script>")[0]
    js = js.replace("import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';", "")
    import re as _re
    js = _re.sub(
        r"import \{[^}]+\} from '@/common/api/discover\.js';",
        "const { fetchDiscover, DISCOVER_FILTERS, DISCOVER_SORTS } = require('../../common/api/discover.js');",
        js
    )
    js = re.sub(r"components:\s*\{\s*unidaTabbar\s*\},", "components: {},", js)
    js = js.replace("export default {", "Page({")
    js = re.sub(r"data\(\)\s*\{\s*return (\{.*?\});\s*\},",
                lambda m: "data: " + m.group(1) + ",", js, flags=re.S)
    m = re.search(r"\t\tmethods:\s*\{(.*?)\n\t\t\}\n", js, re.S)
    if m:
        js = js[:m.start()] + m.group(1) + "\n\t\t" + js[m.end():]
    js = js.replace("uni.", "wx.")
    js = to_native_page(js)
    idx = js.rfind("};")
    js = js[:idx] + "})" + js[idx + 2:]
    # 骨架 v-for 用的数组
    js = js.replace("statusBar: 0,", "statusBar: 0,\n\t\t\t\tskeletonNums: [1, 2, 3, 4],", 1)
    open(os.path.join(OUT_DIR, "discover.js"), "w", encoding="utf-8").write(js)

    # ── json
    open(os.path.join(OUT_DIR, "discover.json"), "w", encoding="utf-8").write(
        """{
  "navigationBarTitleText": "发现",
  "navigationStyle": "custom",
  "enablePullDownRefresh": true,
  "backgroundColor": "#F5F0FF",
  "backgroundTextStyle": "dark",
  "onReachBottomDistance": 120,
  "usingComponents": {
    "unida-tabbar": "../../components/unida-tabbar/unida-tabbar"
  }
}
""")

    # ── static
    copied = H.sync_static()

    print("已同步发现页：discover.wxml / wxss / js / json + common/api/discover.js")
    if copied:
        print("已同步 static 资源 %d 个" % len(copied))


if __name__ == "__main__":
    main()
