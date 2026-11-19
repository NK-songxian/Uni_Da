# -*- coding: utf-8 -*-
"""
临时同步：把 Home 源码直接编译到 mp-weixin 产物目录
===================================================================
场景：HBuilderX 没有重新编译 .vue，但开发者工具只认 unpackage 里的产物。
      此脚本绕过 HBuilderX，直接生成可运行的 home.wxml / wxss / js。

注意：下次在 HBuilderX 里正常「运行到微信开发者工具」后，产物会被覆盖，
      届时这份脚本就不需要了。源码永远是 pages/home/home.vue。
"""
import os
import re
import shutil
import filecmp
import subprocess

ROOT = r"H:\UniDA\unida"
DIST = os.path.join(ROOT, "unpackage", "dist", "dev", "mp-weixin")

VUE = os.path.join(ROOT, "pages", "home", "home.vue")
API = os.path.join(ROOT, "common", "api", "home.js")
STATIC_SRC = os.path.join(ROOT, "static")
STATIC_DST = os.path.join(DIST, "static")


def wxml_from_template(tpl):
    s = tpl

    # template v-else -> block wx:else
    s = s.replace("<template v-else>", "<block wx:else>")
    s = s.replace("</template>", "</block>")

    # v-for
    for_loop = re.compile(r'v-for="\(\s*([A-Za-z0-9_]+)\s*,\s*([A-Za-z0-9_]+)\s*\)\s+in\s+([A-Za-z0-9_\.]+)"')
    s = for_loop.sub(
        lambda m: f'wx:for="{{{{{m.group(3)}}}}}" wx:for-item="{m.group(1)}" '
                  f'wx:for-index="{m.group(2)}" wx:key="{m.group(2)}"',
        s)
    s = re.sub(r'v-for="([A-Za-z0-9_]+) in (\d+)"',
               lambda m: f'wx:for="{{{{skeletonNums}}}}" wx:for-item="{m.group(1)}" wx:key="*this"', s)

    # 条件
    s = re.sub(r'v-else-if="([^"]+)"', r'wx:elif="{{\1}}"', s)
    s = re.sub(r'v-if="([^"]+)"', r'wx:if="{{\1}}"', s)
    s = s.replace(" v-else", " wx:else")

    # 绑定属性
    s = re.sub(r'\s:key="[^"]*"', "", s)
    s = re.sub(r'\s:src="([^"]+)"', lambda m: f' src="{{{{{m.group(1)}}}}}"', s)
    s = re.sub(r'\s:show-scrollbar="([^"]+)"', lambda m: f' show-scrollbar="{{{{{m.group(1)}}}}}"', s)
    s = re.sub(r'\s:selected="([^"]+)"', lambda m: f' selected="{{{{{m.group(1)}}}}}"', s)
    s = re.sub(r'\s:unread-count="([^"]+)"', lambda m: f' unread-count="{{{{{m.group(1)}}}}}"', s)

    # swiper 属性（布尔 / 数字字面量），小程序 swiper 原生支持这些属性名
    s = re.sub(r'\s:(indicator-dots|autoplay|circular)="(true|false)"',
               lambda m: f' {m.group(1)}="{{{{{m.group(2)}}}}}"', s)
    s = re.sub(r'\s:(interval|duration|current)="(\d+)"',
               lambda m: f' {m.group(1)}="{m.group(2)}"', s)

    # :class 对象语法
    s = re.sub(r':class="\{\s*\'([^\']+)\':\s*([A-Za-z0-9_]+)\s*\}"',
               lambda m: f'class="{{{{ {m.group(2)} ? \'{m.group(1)}\' : \'\' }}}}"', s)
    s = re.sub(r':class="\'([^\']+)\'\s*\+\s*([A-Za-z0-9_\.]+)"',
               lambda m: f'class="{m.group(1)}{{{{m.group(2)}}}}"', s)

    # :style 对象语法（本项目只用到下面几种简单形式）
    s = re.sub(r':style="\{\s*paddingTop:\s*([A-Za-z0-9_\.]+)\s*\+\s*\'px\'\s*\}"',
               lambda m: f'style="padding-top:{{{{{m.group(1)}}}}}px"', s)
    s = re.sub(r':style="\{\s*background:\s*([A-Za-z0-9_\.]+)\s*\}"',
               lambda m: f'style="background:{{{{{m.group(1)}}}}}"', s)
    s = re.sub(r':style="\{\s*color:\s*([A-Za-z0-9_\.]+),\s*background:\s*([A-Za-z0-9_\.]+)\s*\}"',
               lambda m: f'style="color:{{{{{m.group(1)}}}}};background:{{{{{m.group(2)}}}}}"', s)
    s = re.sub(r':style="\{\s*background:\s*([A-Za-z0-9_\.]+),\s*marginLeft:[^}]*\}"',
               lambda m: f'style="background:{{{{{m.group(1)}}}}}"', s)

    # 事件
    s = s.replace("@click.stop=", "catchtap=").replace("@click=", "bindtap=")
    # @change -> bindchange（swiper 轮播切换）
    s = re.sub(r'\s@change="([^"]+)"', lambda m: f' bindchange="{m.group(1)}"', s)
    s = re.sub(r'\s@tap="[^"]*"', "", s)

    # Vue 里带参数的事件：bindtap="onCategory(c)" -> 方法名 + data-*
    def event_arg(m):
        attr, name, arg = m.group(1), m.group(2), m.group(3).strip()
        if name == "loadOverview":
            return f'{attr}="onRetryOverview"'
        if name == "loadFeed":
            return f'{attr}="onFeedRetry"'
        if name == "onCategory":
            return f'{attr}="onCategoryTap" data-label="{{{{{arg}.label}}}}"'
        if name == "onPromoTap":
            return f'{attr}="onPromoTap" data-id="{{{{{arg}.id}}}}"'
        # onCardTap / onJoin 只用事件做跳转或提示，参数可忽略
        if "." in arg:
            return f'{attr}="{name}" data-id="{{{{{arg}.id}}}}"'
        return f'{attr}="{name}"'

    s = re.sub(r'\b(bindtap|catchtap)="([A-Za-z0-9_]+)\(([^)]*)\)"', event_arg, s)

    # 内联表达式改事件：feedTab = i -> onFeedTab + data-i
    s = s.replace('bindtap="feedTab = i"', 'bindtap="onFeedTab" data-i="{{i}}"')

    # 对象形式的 :class（表达式版，如 feedTab === i）
    s = re.sub(r'\s:class="\{\s*\'([^\']+)\':\s*([^}]+)\s*\}"',
               lambda m: f' class="{{{{{m.group(2)} ? \'{m.group(1)}\' : \'\'}}}}"', s)

    # 合并重复 class：Vue 的 class + :class 会变成 WXML 两个 class 属性，非法
    def fix_tag(m):
        tag = m.group(0)
        classes = re.findall(r'\sclass="([^"]*)"', tag)
        if len(classes) < 2:
            return tag
        tag = re.sub(r'\sclass="[^"]*"', '', tag)
        merged = " ".join(classes).strip()
        if tag.endswith("/>"):
            return tag[:-2] + f' class="{merged}"/>'
        return tag[:-1] + f' class="{merged}">'

    s = re.sub(r'<[a-zA-Z][^>]*>', fix_tag, s)

    return s.strip() + "\n"


def api_commonjs(src):
    s = src
    s = s.replace("export async function ", "async function ")
    s = s.replace("export function ", "function ")
    s += "\nmodule.exports = { fetchOverview, fetchFeed, setMockFail };\n"
    return s


def to_native_page(js):
    """
    把 Vue Options API 转出来的 Page 代码改成原生小程序响应式写法：
      1. 模板用到的数据只能放在 data 里，读取必须走 this.data.xxx；
      2. 写数据必须走 this.setData({ xxx: ... })，否则视图不会刷新；
      3. feedReqId 只是内部竞态计数，不进模板，保留为普通实例属性。
    """
    m = re.search(r"(\bdata:\s*\{)(.*?)(\n\s*\},)", js, re.S)
    if not m:
        return js

    keys = re.findall(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:", m.group(2), re.M)
    keys = [k for k in keys if k != "feedReqId"]

    head, rest = js[:m.end()], js[m.end():]

    # 读：this.loading -> this.data.loading
    for k in keys:
        rest = re.sub(r"\bthis\." + re.escape(k) + r"\b", "this.data." + k, rest)

    # 写：this.data.loading = false -> this.setData({ loading: false })
    for k in keys:
        pat = re.compile(
            r"(?P<pre>^|[^.\w])this\.data\." + re.escape(k) + r"\s*=\s*(?P<expr>[^;]+);",
            re.M
        )
        def repl(mm):
            pre = mm.group("pre")
            expr = mm.group("expr").strip()
            return pre + "this.setData({ " + k + ": " + expr + " });"
        rest = pat.sub(repl, rest)

    # 带参数的事件在 WXML 里不能传参，用包装方法接住
    wrappers = """
		onRetryOverview() {
			this.loadOverview(true);
		},
		onFeedRetry() {
			this.loadFeed(false);
		},
		onCategoryTap(e) {
			wx.showToast({ title: e.currentTarget.dataset.label || '', icon: 'none' });
		},
"""
    rest = rest.replace(
        "\t\tonLoad() {",
        wrappers + "\t\tonLoad() {\n\t\t\tthis.feedReqId = 0;",
        1
    )

    return head + rest


def sync_static():
    """
    HBuilderX 偶尔只拷了空文件（0 字节）到编译目录，导致 image 标签静默不显示。
    这里按源码 static/ 覆盖缺失、0 字节和内容不一致的资源。
    """
    copied = []
    for root, _, files in os.walk(STATIC_SRC):
        rel = os.path.relpath(root, STATIC_SRC)
        dst_root = STATIC_DST if rel == "." else os.path.join(STATIC_DST, rel)
        os.makedirs(dst_root, exist_ok=True)
        for name in files:
            src = os.path.join(root, name)
            dst = os.path.join(dst_root, name)
            need = (
                not os.path.exists(dst)
                or os.path.getsize(dst) == 0
                or not filecmp.cmp(src, dst, shallow=False)
            )
            if need:
                shutil.copy2(src, dst)
                copied.append(os.path.relpath(dst, DIST).replace("\\", "/"))
    return copied


def main():
    vue = open(VUE, encoding="utf-8").read()

    # ── wxml
    # 注意用 rsplit：内部还有一个 <template v-else>...</template>，
    # 用 split 会在内层就截断，丢掉 tabbar 和根 </view>
    tpl = vue.split("<template>", 1)[1].rsplit("</template>", 1)[0]
    wxml = wxml_from_template(tpl)
    open(os.path.join(DIST, "pages", "home", "home.wxml"), "w", encoding="utf-8").write(wxml)

    # ── wxss（用 sass 编，rpx 保留，WXSS 原生支持）
    scss = vue.split('<style lang="scss" scoped>')[1].split("</style>")[0]
    scss = scss.replace("@import '@/common/unida-tokens.scss';",
                        "@import '" + os.path.join(ROOT, "common", "unida-tokens.scss").replace("\\", "/") + "';")
    tmp = os.path.join(ROOT, "_sync.scss")
    css = os.path.join(ROOT, "_sync.css")
    open(tmp, "w", encoding="utf-8").write(scss)
    subprocess.run([r"C:\Users\Ryan\.workbuddy\binaries\node\versions\22.22.2-6\npx.cmd",
                    "--yes", "sass@1.77.8", "--no-source-map", tmp, css],
                   check=True, capture_output=True, shell=True)
    open(os.path.join(DIST, "pages", "home", "home.wxss"), "w", encoding="utf-8").write(
        open(css, encoding="utf-8").read())
    os.remove(tmp); os.remove(css)

    # ── api 模块（CommonJS）
    os.makedirs(os.path.join(DIST, "common", "api"), exist_ok=True)
    open(os.path.join(DIST, "common", "api", "home.js"), "w", encoding="utf-8").write(
        api_commonjs(open(API, encoding="utf-8").read()))

    # ── js：从源码 script 里取 data / 生命周期 / methods
    js = vue.split("<script>")[1].split("</script>")[0]
    js = js.replace("import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';", "")
    js = js.replace("import { fetchOverview, fetchFeed } from '@/common/api/home.js';",
                    "const { fetchOverview, fetchFeed } = require('../../common/api/home.js');")
    js = re.sub(r"components:\s*\{\s*unidaTabbar\s*\},", "components: {},", js)
    js = js.replace("export default {", "Page({")
    # 去掉最后一个 "};"
    # 把 Vue Options API 变成小程序 Page 配置
    # 1) data() { return {...} } -> data: {...}
    js = re.sub(r"data\(\)\s*\{\s*return (\{.*?\});\s*\},",
                lambda m: "data: " + m.group(1) + ",", js, flags=re.S)
    # 2) watch 在 Page 里不存在，去掉（切 tab 改用 onFeedTab）
    js = re.sub(r"watch:\s*\{.*?\n\t\t\},\n", "", js, flags=re.S)
    # 3) methods: { ... } 拍平到 Page 根
    m = re.search(r"\t\tmethods:\s*\{(.*?)\n\t\t\}\n", js, re.S)
    if m:
        inner = m.group(1)
        # 方法签名保持，去掉末尾多一层缩进影响不大
        js = js[:m.start()] + inner + "\n\t\t" + js[m.end():]

    # 4) 追加切 tab 的处理方法
    onfeed = """
		onFeedTab(e) {
			const i = Number(e.currentTarget.dataset.i);
			if (i === this.feedTab) return;
			this.feedTab = i;
			this.feedPage = 1;
			this.feedHasMore = true;
			this.feedList = [];
			this.loadFeed(true);
		},
"""
    js = js.replace("\t\tonLoad() {", onfeed + "\t\tonLoad() {", 1)

    # 5) 小程序里没有 uni 全局对象，编译后就是 wx
    js = js.replace("uni.", "wx.")

    # 6) 关键：Vue 的 this.xxx 响应式赋值，在原生 Page 里必须改成
    #    this.data.xxx 读取 + this.setData({ xxx }) 写入
    js = to_native_page(js)

    idx = js.rfind("};")
    js = js[:idx] + "})" + js[idx + 2:]
    # 骨架屏 v-for 用的数组
    js = js.replace("statusBar: 0,", "statusBar: 0,\n\t\t\t\tskeletonNums: [1, 2, 3, 4, 5, 6],", 1)
    open(os.path.join(DIST, "pages", "home", "home.js"), "w", encoding="utf-8").write(js)

    # ── json
    open(os.path.join(DIST, "pages", "home", "home.json"), "w", encoding="utf-8").write(
        """{
  "navigationBarTitleText": "有你搭",
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

    # ── static 资源（修复 0 字节 / 缺失文件）
    copied = sync_static()

    print("已同步编译产物：home.wxml / home.wxss / home.js / home.json / common/api/home.js")
    if copied:
        print("已同步 static 资源 %d 个：" % len(copied))
        for p in copied[:30]:
            print("  -", p)
        if len(copied) > 30:
            print("  ... 其余 %d 个" % (len(copied) - 30))


if __name__ == "__main__":
    main()
