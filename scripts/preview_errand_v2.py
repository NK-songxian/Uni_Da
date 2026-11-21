# -*- coding: utf-8 -*-
"""跑腿大厅 V2（3D 统一元素版）静态预览"""
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


def tabbar(active_idx):
    names = {0: "home", 1: "discover", 3: "message", 4: "mine"}
    labels = {"home": "首页", "discover": "发现", "message": "消息", "mine": "我的"}
    items = []
    for o in [0, 1, "space", 3, 4]:
        if o == "space":
            items.append('<div class="tab-item publish-space"></div>')
            continue
        key = names[o]
        on = " active" if o == active_idx else ""
        items.append(f'<div class="tab-item data-v-d86c95b2{on}"><div class="icon-wrap data-v-d86c95b2"><img class="tab-ico data-v-d86c95b2" src="static/unida/tabbar/tab-{key}.png"></div><span class="tab-text data-v-d86c95b2">{labels[key]}</span></div>')
    return (f'<div class="unida-tabbar data-v-d86c95b2"><img class="tabbar-sheet data-v-d86c95b2" src="static/unida/tabbar/tabbar-sheet.png">'
            f'<div class="tabbar-content data-v-d86c95b2">{"".join(items)}</div>'
            f'<div class="publish-center data-v-d86c95b2"><img class="publish-logo data-v-d86c95b2" src="static/unida/tabbar/publish-logo.png"><span class="publish-text data-v-d86c95b2">发布</span></div></div>')


CSS = load_css("errand-hall", TAB_CSS)

CATS = [("ico-bag.webp", "快递代取", "purple"), ("ico-megaphone.webp", "外卖代拿", "orange"),
        ("ico-calendar.webp", "物品代送", "pink"), ("ico-bubble.webp", "其他互助", "green")]
cats_html = "".join(
    f'<div class="eh__cat"><div class="eh__cat-icon eh__cat-icon--{tone}"><img class="eh__cat-img" src="static/unida/msg/{ico}"></div>'
    f'<span class="eh__cat-label">{label}</span></div>' for ico, label, tone in CATS)

ORDERS = [
    ("快递代取", "8", "帮忙取个快递（中通北区驿站）", "北区驿站", "东园3栋", "今天 18:00 前", "阿星", "东园3栋", "a"),
    ("外卖代拿", "5", "一楼拿外卖送到宿舍楼下", "东门", "西园1栋", "现在", "小林", "西园1栋", "b"),
    ("物品代送", "12", "帮忙送一份资料到教学楼", "图书馆", "3教201", "明天 8:00", "Leo", "南园5栋", "c"),
]
orders_html = "".join(
    f'<div class="eh__item"><div class="eh__item-head">'
    f'<img class="eh__item-tag" src="static/unida/msg/tag-order.webp">'
    f'<div class="eh__reward"><span class="eh__reward-s">¥</span><span class="eh__reward-n">{reward}</span></div></div>'
    f'<span class="eh__item-title">{title}</span>'
    f'<div class="eh__item-meta">'
    f'<div class="eh__meta-row"><img class="eh__meta-ico" src="static/icons-dark/pin.png"><span class="eh__meta-t">{frm} → {to}</span></div>'
    f'<div class="eh__meta-row"><img class="eh__meta-ico" src="static/icons-dark/clock.png"><span class="eh__meta-t">{time}</span></div></div>'
    f'<div class="eh__item-foot"><div class="eh__user"><div class="eh__avatar eh__avatar--{tone}"><span class="eh__avatar-ch">{user[0]}</span></div>'
    f'<span class="eh__user-t">{user} · {dorm}</span></div>'
    f'<div class="eh__status"><span class="eh__status-t">立即接单</span></div></div></div>'
    for typ, reward, title, frm, to, time, user, dorm, tone in ORDERS)

BODY = (f'<div class="eh unida-page"><div class="eh__hero">'
        f'<img class="eh__hero-bubble" src="static/unida/msg/ico-bubble.webp">'
        f'<div class="eh__hero-txt"><span class="eh__title">跑腿大厅</span><span class="eh__sub">同学互助，小事不用愁</span></div>'
        f'<img class="eh__hero-mascot" src="static/unida/msg/mascot-wave.webp"></div>'
        f'<div class="eh__search"><img class="eh__search-ico" src="static/unida/msg/ico-search.webp">'
        f'<span class="eh__search-ph">搜索跑腿需求（快递、外卖…）</span></div>'
        f'<div class="eh__cats">{cats_html}</div>'
        f'<div class="eh__cta"><img class="eh__cta-scene" src="static/unida/msg/scene-takeout.webp">'
        f'<div class="eh__cta-info"><span class="eh__cta-title">需要帮忙？发布需求</span>'
        f'<span class="eh__cta-sub">同学接单，快速搞定</span>'
        f'<div class="eh__cta-btn"><span class="eh__cta-btn-t">去发布 ›</span></div></div></div>'
        f'<div class="eh__sect"><span class="eh__sect-t">附近需求</span><span class="eh__sect-s">3 个待接单</span></div>'
        f'{orders_html}<div class="eh__bottom-space"></div>{tabbar(1)}</div>')

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#ddd; font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }
.phone { width:375px; margin:0 auto; background:#F5F0FF; }
img { display:block; }
span { display:inline; }
__CSS__
</style></head><body><div class="phone">__BODY__</div></body></html>"""
out = os.path.join(ROOT, "preview_errand_hall_v2.html")
open(out, "w", encoding="utf-8").write(HTML.replace("__CSS__", CSS).replace("__BODY__", BODY))

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_page(viewport={"width": 375, "height": 900})
    pg.goto("file:///" + out.replace("\\", "/"))
    pg.wait_for_timeout(800)
    pg.evaluate("document.querySelector('.phone').style.height='auto';document.querySelectorAll('.phone *').forEach(e=>{if(getComputedStyle(e).overflow==='hidden')e.style.overflow='visible'})")
    pg.wait_for_timeout(200)
    shot = os.path.join(ROOT, "docs", "audit", "errand_hall_v2_preview.png")
    pg.screenshot(path=shot, full_page=True)
    print("shot", shot)
    b.close()
