# -*- coding: utf-8 -*-
"""消息页 V2（设计稿版）静态预览对照"""
import os
import re

ROOT = r"H:\UniDA\unida"
DIST = os.path.join(ROOT, "unpackage", "dist", "dev", "mp-weixin")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def load_css(page, extra=""):
    wxss = open(os.path.join(DIST, "pages", page, page + ".wxss"), encoding="utf-8").read()
    css = re.sub(r"(-?\d+(?:\.\d+)?)rpx", lambda m: f"{float(m.group(1))*0.5:g}px", wxss)
    css = re.sub(r"\bimage\b", "img", css)
    return css + extra


TAB_CSS = open(os.path.join(DIST, "components", "unida-tabbar", "unida-tabbar.wxss"), encoding="utf-8").read()
TAB_CSS = re.sub(r"(-?\d+(?:\.\d+)?)rpx", lambda m: f"{float(m.group(1))*0.5:g}px", TAB_CSS)
TAB_CSS = re.sub(r"\bimage\b", "img", TAB_CSS)


def tabbar(active_idx, unread=None):
    names = {0: "home", 1: "discover", 3: "message", 4: "mine"}
    labels = {"home": "首页", "discover": "发现", "message": "消息", "mine": "我的"}
    items = []
    for o in [0, 1, "space", 3, 4]:
        if o == "space":
            items.append('<div class="tab-item publish-space"></div>')
            continue
        key = names[o]
        on = " active" if o == active_idx else ""
        dot = (f'<div class="tab-badge data-v-d86c95b2">{unread}</div>' if o == 3 and unread else "")
        items.append(f'<div class="tab-item data-v-d86c95b2{on}"><div class="icon-wrap data-v-d86c95b2"><img class="tab-ico data-v-d86c95b2" src="static/unida/tabbar/tab-{key}.png">{dot}</div><span class="tab-text data-v-d86c95b2">{labels[key]}</span></div>')
    return (f'<div class="unida-tabbar data-v-d86c95b2"><img class="tabbar-sheet data-v-d86c95b2" src="static/unida/tabbar/tabbar-sheet.png">'
            f'<div class="tabbar-content data-v-d86c95b2">{"".join(items)}</div>'
            f'<div class="publish-center data-v-d86c95b2"><img class="publish-logo data-v-d86c95b2" src="static/unida/tabbar/publish-logo.png"><span class="publish-text data-v-d86c95b2">发布</span></div></div>')


CSS = load_css("message", TAB_CSS + "\n.ms__tabs-row { flex-wrap:nowrap; }\n.ms__tab { flex-shrink:0; }\n")

# tabs
tabs_html = '<div class="ms__tab ms__tab--all ms__tab--on"><span class="ms__tab-all-t">全部</span></div>'
for t in ["tag-chat", "tag-book", "tag-event", "tag-order", "tag-system"]:
    tabs_html += f'<div class="ms__tab"><img class="ms__tab-img" src="static/unida/msg/{t}.webp"></div>'

# 会话卡
CHATS = [
    ("static/unida/msg/mascot-star.webp", "", "林小悠", "tag-chat", "10:12", "badge-3", "今天图书馆自习还去吗？要不要一起？", None, None, None),
    ("static/unida/msg/scene-booth.webp", "", "校园活动｜春日校园跑", "tag-event", "昨天 20:30", None, "【报名开启】UNIDA 春日校园跑来啦！一起在阳光下奔跑，结识更多运动搭子！", None, None, None),
    ("static/unida/msg/scene-fitness.webp", "", "学习健身搭子预约", "tag-book", "昨天 18:05", None, "预约已确认！你已成功约到「图书馆自习 · 健身打卡」搭子～", ["3月12日（周三）", "19:00 – 21:00"], None, "static/unida/msg/badge-check.webp"),
    ("static/unida/msg/scene-takeout.webp", "", "校园跑腿订单", "tag-order", "09:36", None, "【进行中】你的跑腿订单已接单！帮取：食堂奶茶（2杯）› 送达：紫荆宿舍楼 3栋", None, [("已接单", True), ("取货中", True), ("配送中", False), ("已完成", False)], "static/unida/msg/badge-doing.webp"),
    ("", [("阿", "purple"), ("星", "orange"), ("林", "green"), ("Leo", "sky")], "校园活动搭子群（128）", "tag-chat", "08:47", "badge-12", "阿晨：周六的飞盘活动还有名额！要一起组队吗？", None, None, None),
]
chats_html = ""
for avatar, group, name, tag, time, unread, preview, meta, progress, status in CHATS:
    if avatar:
        av = f'<img class="ms__avatar" src="{avatar}">'
    else:
        faces = "".join(f'<div class="ms__group-face ms__group-face--{tone}"><span class="ms__group-ch">{ch}</span></div>' for ch, tone in group)
        av = f'<div class="ms__avatar-group">{faces}</div>'
    online = '<div class="ms__online"></div>' if name == "林小悠" else ""
    unread_html = f'<img class="ms__unread" src="static/unida/msg/{unread}.webp">' if unread else ""
    meta_html = ("<div class=\"ms__meta\">" + "".join(f'<span class="ms__meta-t">{m}</span>' for m in meta) + "</div>") if meta else ""
    progress_html = ""
    if progress:
        dots = "".join(
            f'<div class="ms__progress-line"><div class="ms__progress-dot{" ms__progress-dot--on" if on else ""}"></div>'
            f'<span class="ms__progress-t{" ms__progress-t--on" if on else ""}">{t}</span></div>'
            for t, on in progress)
        progress_html = f'<div class="ms__progress">{dots}</div>'
    status_html = f'<img class="ms__status" src="{status}">' if status else ""
    chats_html += (f'<div class="ms__item"><div class="ms__avatar-wrap">{av}{online}</div>'
                   f'<div class="ms__main"><div class="ms__row"><span class="ms__name">{name}</span>'
                   f'<img class="ms__row-tag" src="static/unida/msg/{tag}.webp">'
                   f'<div class="ms__row-right"><span class="ms__time">{time}</span>{unread_html}</div></div>'
                   f'<span class="ms__preview">{preview}</span>{meta_html}{progress_html}{status_html}</div>'
                   f'<img class="ms__chev" src="static/icons-dark/chevron.png"></div>')

BODY = (f'<div class="ms unida-page"><div class="ms__hero"><img class="ms__hero-img" src="static/unida/msg/msg-hero.jpg"></div>'
        f'<div class="ms__search"><img class="ms__search-ico" src="static/unida/msg/ico-search.webp">'
        f'<span class="ms__search-ph">搜索聊天、活动、订单等消息</span></div>'
        f'<div class="ms__tabs"><div class="ms__tabs-row">{tabs_html}</div></div>'
        f'<div class="ms__pin"><img class="ms__pin-mascot" src="static/unida/msg/mascot-wave.webp">'
        f'<div class="ms__pin-body"><div class="ms__pin-row"><span class="ms__pin-name">UNIDA（有你搭）</span>'
        f'<img class="ms__pin-shield" src="static/unida/msg/ico-shield.webp"><span class="ms__pin-sys">系统</span></div>'
        f'<span class="ms__pin-title">欢迎来到 UNIDA!</span>'
        f'<span class="ms__pin-desc">在这里，找到同频的搭子、参与精彩的校园活动、解锁更丰富的大学生活！一起搭出属于你的校园故事吧！</span></div>'
        f'<img class="ms__pin-badge" src="static/unida/msg/pin-yellow.webp"></div>'
        f'{chats_html}<div class="ms__bottom-space"></div>{tabbar(3, 15)}</div>')

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#ddd; font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }
.phone { width:375px; margin:0 auto; background:#F5F0FF; }
img { display:block; }
span { display:inline; }
__CSS__
</style></head><body><div class="phone">__BODY__</div></body></html>"""
out = os.path.join(ROOT, "preview_message_v2.html")
open(out, "w", encoding="utf-8").write(HTML.replace("__CSS__", CSS).replace("__BODY__", BODY))

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_page(viewport={"width": 375, "height": 900})
    pg.goto("file:///" + out.replace("\\", "/"))
    pg.wait_for_timeout(800)
    pg.evaluate("document.querySelector('.phone').style.height='auto';document.querySelectorAll('.phone *').forEach(e=>{if(getComputedStyle(e).overflow==='hidden')e.style.overflow='visible'})")
    pg.wait_for_timeout(200)
    shot = os.path.join(ROOT, "docs", "audit", "message_v2_preview.png")
    pg.screenshot(path=shot, full_page=True)
    print("shot", shot)
    b.close()
