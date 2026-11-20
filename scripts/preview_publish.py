# -*- coding: utf-8 -*-
"""发布中心页视觉预览：读产物 wxss + 手写等价结构（含 tabbar）"""
import os
import re

ROOT = r"H:\UniDA\unida"
DIST = os.path.join(ROOT, "unpackage", "dist", "dev", "mp-weixin")

wxss = open(os.path.join(DIST, "pages", "publish", "publish.wxss"), encoding="utf-8").read()
tab_css = open(os.path.join(DIST, "components", "unida-tabbar", "unida-tabbar.wxss"), encoding="utf-8").read()
css = wxss + tab_css
css = re.sub(r"(-?\d+(?:\.\d+)?)rpx", lambda m: f"{float(m.group(1))*0.5:g}px", css)
css = re.sub(r"\bimage\b", "img", css)

TONES = {
    "purple": "pb__ico--purple", "orange": "pb__ico--orange", "pink": "pb__ico--pink",
    "green": "pb__ico--green", "sky": "pb__ico--sky", "sun": "pb__ico--sun",
}
TYPES = [
    ("buddy.png", "找搭子", "自习·吃饭·运动，找同频伙伴", "purple"),
    ("calendar.png", "发起活动", "组一场多人校园活动", "orange"),
    ("bulb.png", "技能教学", "分享你的特长与课程", "pink"),
    ("box.png", "跑腿需求", "发布互助跑腿任务", "green"),
    ("book.png", "校园动态", "分享此刻的校园生活", "sky"),
    ("flame.png", "活动招募", "为你的活动招募队友", "sun"),
]
CARDS = "".join(
    f'<div class="pb__card"><div class="pb__cardhead"><div class="pb__ico {TONES[t]}"><img class="pb__ico-img" src="static/icons-dark/{ico}"></div>'
    f'<img class="pb__chev" src="static/icons-dark/chevron.png"></div>'
    f'<span class="pb__name">{name}</span><span class="pb__desc">{desc}</span></div>'
    for ico, name, desc, t in TYPES)

LABELS = ["label-hot", "label-new", "label-study", "label-sport", "label-fun", "label-help",
          "label-campus", "label-rec", "label-sync", "label-limit"]
LABS = "".join(f'<img class="pb__lab" src="static/unida/bubbles/{l}.webp">' for l in LABELS)

TABS = """
<div class="unida-tabbar data-v-d86c95b2">
  <img class="tabbar-sheet data-v-d86c95b2" src="static/unida/tabbar/tabbar-sheet.png">
  <div class="tabbar-content data-v-d86c95b2">
    <div class="tab-item data-v-d86c95b2"><div class="icon-wrap data-v-d86c95b2"><img class="tab-ico data-v-d86c95b2" src="static/unida/tabbar/tab-home.png"></div><span class="tab-text data-v-d86c95b2">首页</span></div>
    <div class="tab-item data-v-d86c95b2"><div class="icon-wrap data-v-d86c95b2"><img class="tab-ico data-v-d86c95b2" src="static/unida/tabbar/tab-discover.png"></div><span class="tab-text data-v-d86c95b2">发现</span></div>
    <div class="tab-item publish-space data-v-d86c95b2"></div>
    <div class="tab-item data-v-d86c95b2"><div class="icon-wrap data-v-d86c95b2"><img class="tab-ico data-v-d86c95b2" src="static/unida/tabbar/tab-message.png"></div><span class="tab-text data-v-d86c95b2">消息</span></div>
    <div class="tab-item data-v-d86c95b2"><div class="icon-wrap data-v-d86c95b2"><img class="tab-ico data-v-d86c95b2" src="static/unida/tabbar/tab-mine.png"></div><span class="tab-text data-v-d86c95b2">我的</span></div>
  </div>
  <div class="publish-center data-v-d86c95b2"><img class="publish-logo data-v-d86c95b2" src="static/unida/tabbar/publish-logo.png"><span class="publish-text data-v-d86c95b2">发布</span></div>
</div>
"""

BODY = f"""
<div class="pb">
  <div class="pb__top"><span class="pb__title">发布中心</span><img class="pb__brand" src="static/unida/bubbles/brand-badge-u.webp"></div>
  <div class="pb__hero">
    <img class="pb__hero-frame" src="static/unida/bubbles/frame-unida-cloud.webp">
    <div class="pb__hero-txt"><span class="pb__hero-t">选一种方式，开启你的校园故事</span><span class="pb__hero-s">清晰的标题 · 真实的封面 · 明确的时间地点</span></div>
    <div class="pb__spark pb__spark--a"></div><div class="pb__spark pb__spark--b"></div>
  </div>
  <div class="pb__grid">{CARDS}</div>
  <div class="pb__sect"><div class="pb__spark pb__spark--c"></div><span class="pb__sect-t">大家都在发</span><span class="pb__sect-s">点标签，搭子更快找到你</span></div>
  <div class="pb__lscroll"><div class="pb__lrow">{LABS}</div></div>
  <div class="pb__tip">
    <div class="pb__tip-ico"><img class="pb__tip-img" src="static/icons-dark/bulb.png"></div>
    <div class="pb__tip-body"><span class="pb__tip-t">发布小贴士</span><span class="pb__tip-s">写清楚做什么、什么时候、在哪儿，再选几个同频标签，搭子会主动来找你。</span></div>
  </div>
  <div class="pb__bottom-space"></div>
  {TABS}
</div>
"""

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#ddd; font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }
.phone { width:375px; margin:0 auto; background:#F5F0FF; }
img { display:block; }
span { display:inline; }
__CSS__
</style></head><body><div class="phone">__BODY__</div></body></html>"""
HTML = HTML.replace("__CSS__", css).replace("__BODY__", BODY)

out = os.path.join(ROOT, "preview_publish.html")
open(out, "w", encoding="utf-8").write(HTML)

from playwright.sync_api import sync_playwright
shot = os.path.join(ROOT, "docs", "audit", "publish_preview.png")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    pg = b.new_page(viewport={"width": 375, "height": 900})
    pg.goto("file:///" + out.replace("\\", "/"))
    pg.wait_for_timeout(900)
    pg.evaluate("document.querySelector('.phone').style.height='auto';document.querySelectorAll('.phone *').forEach(e=>{if(getComputedStyle(e).overflow==='hidden')e.style.overflow='visible'})")
    pg.wait_for_timeout(200)
    pg.screenshot(path=shot, full_page=True)
    b.close()
print("已生成", out, "截图", shot)
