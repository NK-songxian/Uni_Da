# -*- coding: utf-8 -*-
"""消息/会话/跑腿大厅/跑腿详情 批量视觉预览"""
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
    order = [0, 1, "space", 3, 4]
    for o in order:
        if o == "space":
            items.append('<div class="tab-item publish-space"></div>')
            continue
        key = names[o]
        on = " active" if o == active_idx else ""
        items.append(f'<div class="tab-item data-v-d86c95b2{on}"><div class="icon-wrap data-v-d86c95b2"><img class="tab-ico data-v-d86c95b2" src="static/unida/tabbar/tab-{key}.png"></div><span class="tab-text data-v-d86c95b2">{labels[key]}</span></div>')
    return (f'<div class="unida-tabbar data-v-d86c95b2"><img class="tabbar-sheet data-v-d86c95b2" src="static/unida/tabbar/tabbar-sheet.png">'
            f'<div class="tabbar-content data-v-d86c95b2">{"".join(items)}</div>'
            f'<div class="publish-center data-v-d86c95b2"><img class="publish-logo data-v-d86c95b2" src="static/unida/tabbar/publish-logo.png"><span class="publish-text data-v-d86c95b2">发布</span></div></div>')


def html_for(body, css):
    html = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#ddd; font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }
.phone { width:375px; margin:0 auto; background:#F5F0FF; }
img { display:block; }
span { display:inline; }
input { border:none; outline:none; }
__CSS__
</style></head><body><div class="phone">__BODY__</div></body></html>"""
    return html.replace("__CSS__", css).replace("__BODY__", body)


# ---------- message ----------
css_ms = load_css("message", TAB_CSS)
NOTICES = [("calendar.png", "活动通知", 2, "purple"), ("heart.png", "预约通知", 1, "green"), ("box.png", "订单通知", 0, "orange"), ("bell.png", "系统通知", 0, "sky")]
n_html = "".join(
    f'<div class="ms__notice"><div class="ms__notice-ico ms__notice-ico--{tone}"><img class="ms__notice-img" src="static/icons-dark/{ico}">'
    + (f'<div class="ms__notice-count"><span class="ms__notice-count-t">{c}</span></div>' if c else "")
    + f'</div><span class="ms__notice-label">{label}</span></div>'
    for ico, label, c, tone in NOTICES)
CHATS = [("阿星", "a", "10:32", "周六的夜跑还剩一个位置，来吗？", 1), ("摄影社-小林", "b", "昨天", "照片修好啦，发你邮箱了～", 1), ("Leo", "c", "昨天", "快递已经放到楼下了，记得取哦", 0)]
c_html = "".join(
    f'<div class="ms__chat"><div class="ms__avatar ms__avatar--{tone}"><span class="ms__avatar-ch">{name[0]}</span><div class="ms__dot"></div></div>'
    f'<div class="ms__main"><div class="ms__row"><span class="ms__name">{name}</span><span class="ms__time">{time}</span></div>'
    f'<span class="ms__preview">{preview}</span></div><img class="ms__chev" src="static/icons-dark/chevron.png"></div>'
    for name, tone, time, preview, unread in CHATS)
body_ms = (f'<div class="ms unida-page"><div class="ms__top"><span class="ms__title">消息</span>'
           f'<div class="ms__compose"><img class="ms__compose-img" src="static/icons-dark/plus.png"></div></div>'
           f'<div class="ms__notices">{n_html}</div>'
           f'<div class="ms__sect"><span class="ms__sect-t">最近会话</span><span class="ms__sect-s">全部 ›</span></div>{c_html}'
           f'<div class="ms__bottom-space"></div>{tabbar(2)}</div>')

# ---------- chat ----------
css_ch = load_css("chat")
msgs = ["你好！看到你发布的跑腿需求，我可以帮你取～", "我在东区，离北区驿站挺近的"]
m_html = "".join(
    f'<div class="ch__msg ch__msg--in"><div class="ch__msg-avatar"><span class="ch__msg-ch">周</span></div>'
    f'<div class="ch__bubble">{t}</div></div>' for t in msgs)
emojis = ["emoji-heart", "emoji-like", "emoji-clap", "emoji-party", "emoji-fire", "emoji-smile"]
e_html = "".join(f'<img class="ch__emoji" src="static/unida/bubbles/{e}.webp">' for e in emojis)
body_ch = (f'<div class="ch"><div class="ch__nav">'
           f'<div class="ch__back"><img class="ch__back-img" src="static/icons-dark/back.png"></div>'
           f'<div class="ch__peer"><div class="ch__peer-avatar"><span class="ch__peer-ch">周</span></div>'
           f'<div class="ch__peer-info"><span class="ch__peer-name">周同学</span>'
           f'<div class="ch__peer-status"><img class="ch__peer-shield" src="static/unida/bubbles/shield-check.webp"><span class="ch__peer-status-t">在线 · 已认证</span></div></div></div>'
           f'<div class="ch__more"><img class="ch__more-img" src="static/icons-dark/compass.png"></div></div>'
           f'<div class="ch__msgs"><div class="ch__msgs-pad"></div><div class="ch__time">今天 10:24</div>{m_html}'
           f'<div class="ch__ordercard"><div class="ch__ordercard-head"><div class="ch__ordercard-tag"><img class="ch__ordercard-tag-img" src="static/icons-dark/box.png"><span class="ch__ordercard-tag-t">跑腿订单</span></div><span class="ch__ordercard-status">待接单</span></div>'
           f'<span class="ch__ordercard-title">帮忙取快递（中通北区）</span><span class="ch__ordercard-reward">赏金 ¥8.00</span></div>'
           f'<div class="ch__msg ch__msg--out"><div class="ch__bubble">太好了！取件码我私你，送到东园3栋楼下就行～</div><div class="ch__msg-avatar ch__msg-avatar--me"><span class="ch__msg-ch">我</span></div></div>'
           f'<div class="ch__msgs-pad"></div></div>'
           f'<div class="ch__emojis">{e_html}</div>'
           f'<div class="ch__inputbar"><div class="ch__tool"><img class="ch__tool-img" src="static/icons-dark/plus.png"></div>'
           f'<input class="ch__input" placeholder="发消息…"><div class="ch__send">发送</div></div></div>')

# ---------- errand-hall ----------
css_eh = load_css("errand-hall", TAB_CSS)
CATS = [("box.png", "快递代取", "purple"), ("mini-food.webp", "外卖代拿", "orange"), ("mark-purple.webp", "物品代送", "pink"), ("buddy.png", "其他互助", "green")]
cat_html = "".join(f'<div class="eh__cat"><div class="eh__cat-icon eh__cat-icon--{tone}"><img class="eh__cat-img" src="static/unida/bubbles/{ico}" if ico.endswith("webp") else "static/icons-dark/{ico}"></div><span class="eh__cat-label">{label}</span></div>' for ico, label, tone in CATS)
ORDERS = [("快递代取", "8", "帮忙取个快递（中通北区驿站）", "北区驿站", "东园3栋", "今天 18:00 前", "阿星", "东园3栋", "a"),
          ("外卖代拿", "5", "一楼拿外卖送到宿舍楼下", "东门", "西园1栋", "现在", "小林", "西园1栋", "b"),
          ("物品代送", "12", "帮忙送一份资料到教学楼", "图书馆", "3教201", "明天 8:00", "Leo", "南园5栋", "c")]
o_html = "".join(
    f'<div class="eh__item"><div class="eh__item-head"><div class="eh__item-type"><span class="eh__item-type-t">{typ}</span></div>'
    f'<div class="eh__item-reward"><span class="eh__item-reward-s">¥</span><span class="eh__item-reward-n">{reward}</span></div></div>'
    f'<span class="eh__item-title">{title}</span>'
    f'<div class="eh__item-meta"><div class="eh__item-meta-row"><img class="eh__meta-ico" src="static/icons-dark/pin.png"><span class="eh__meta-t">{frm} → {to}</span></div>'
    f'<div class="eh__item-meta-row"><img class="eh__meta-ico" src="static/icons-dark/clock.png"><span class="eh__meta-t">{time}</span></div></div>'
    f'<div class="eh__item-foot"><div class="eh__item-user"><div class="eh__item-avatar eh__item-avatar--{tone}"><span class="eh__item-avatar-ch">{user[0]}</span></div><span class="eh__item-user-t">{user} · {dorm}</span></div>'
    f'<div class="eh__item-btn"><span class="eh__item-btn-t">立即接单</span></div></div></div>'
    for typ, reward, title, frm, to, time, user, dorm, tone in ORDERS)
body_eh = (f'<div class="eh unida-page"><div class="eh__top"><span class="eh__title">跑腿大厅</span>'
           f'<div class="search"><img class="search__ico" src="static/icons/search.png"><span class="search__ph">搜索跑腿需求（快递、外卖…）</span></div></div>'
           f'<div class="eh__cats">{cat_html}</div>'
           f'<div class="eh__cta"><div class="eh__cta-info"><span class="eh__cta-title">需要帮忙？发布跑腿需求</span><span class="eh__cta-sub">同学接单，快速搞定</span></div>'
           f'<img class="eh__cta-img" src="static/unida/bubbles/catering-pin.webp"><div class="eh__cta-btn"><span class="eh__cta-btn-t">去发布</span></div></div>'
           f'<div class="eh__sect"><span class="eh__sect-t">附近需求</span><span class="eh__sect-s">3 个待接单</span></div>{o_html}'
           f'<div class="eh__bottom-space"></div>{tabbar(1)}</div>')
# search 样式（unida-search 组件等价）
css_eh += """
.search { display:flex; align-items:center; height:36px; background:#fff; border-radius:999px; padding:0 14px; box-shadow:0 4px 12px rgba(123,97,255,0.08); }
.search__ico { width:14px; height:14px; opacity:0.5; margin-right:8px; }
.search__ph { font-size:12.5px; color:#B8B2C8; }
"""

# ---------- errand-detail ----------
css_ed = load_css("errand-detail")
STEPS = ["发布需求", "接单", "执行中", "已交付", "评价"]
s_html = "".join(
    f'<div class="ed__step"><div class="ed__step-dot{" ed__step-dot--on" if i <= 1 else ""}"><span class="ed__step-dot-t">{"✓" if i <= 1 else i+1}</span></div>'
    f'<span class="ed__step-label{" ed__step-label--on" if i <= 1 else ""}">{s}</span>'
    + (f'<div class="ed__step-line{" ed__step-line--on" if i < 1 else ""}"></div>' if i < 4 else "")
    + '</div>' for i, s in enumerate(STEPS))
LINES = [("需求描述", "帮忙取个快递，中通北区驿站，取件码已私聊"), ("取件地点", "北区快递驿站"), ("送达地点", "东园3栋宿舍楼下"), ("期望时间", "今天 18:00 前"), ("订单编号", "RT20261118001")]
l_html = "".join(f'<div class="ed__line"><span class="ed__line-k">{k}</span><span class="ed__line-v{(" ed__line-v--num") if "RT" in v else ""}">{v}</span></div>' for k, v in LINES)
body_ed = (f'<div class="ed unida-page"><div class="ed__nav">'
           f'<div class="ed__back"><img class="ed__back-img" src="static/icons-dark/back.png"></div>'
           f'<span class="ed__title">跑腿订单详情</span><div class="ed__ph"></div></div>'
           f'<div class="ed__status"><img class="ed__status-img" src="static/unida/bubbles/catering-pin.webp">'
           f'<div class="ed__status-info"><span class="ed__status-title">待接单</span><span class="ed__status-sub">快递代取 · 赏金 <span class="ed__status-num">¥8.00</span></span></div>'
           f'<div class="ed__status-badge"><span class="ed__status-badge-t">进行中</span></div></div>'
           f'<div class="ed__progress">{s_html}</div>'
           f'<div class="ed__card"><span class="ed__card-title">需求详情</span>{l_html}</div>'
           f'<div class="ed__card ed__user"><div class="ed__user-avatar"><span class="ed__user-ch">阿</span></div>'
           f'<div class="ed__user-info"><span class="ed__user-name">阿星</span>'
           f'<div class="ed__user-sub"><img class="ed__user-shield" src="static/unida/bubbles/shield-check.webp"><span class="ed__user-sub-t">已认证 · 好评率 4.9</span></div></div>'
           f'<img class="ed__chev" src="static/icons-dark/chevron.png"></div>'
           f'<div class="ed__bottom"><div class="ed__btn ed__btn--ghost"><img class="ed__btn-img" src="static/unida/bubbles/chat-purple.webp"><span class="ed__btn-ghost-t">联系TA</span></div>'
           f'<div class="ed__btn ed__btn--primary"><span class="ed__btn-t">立即接单</span></div></div></div>')

JOBS = [
    ("message", body_ms, css_ms),
    ("chat", body_ch, css_ch),
    ("errand-hall", body_eh, css_eh),
    ("errand-detail", body_ed, css_ed),
]

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_page(viewport={"width": 375, "height": 900})
    for name, body, css in JOBS:
        out = os.path.join(ROOT, "preview_%s.html" % name.replace("-", "_"))
        open(out, "w", encoding="utf-8").write(html_for(body, css))
        pg.goto("file:///" + out.replace("\\", "/"))
        pg.wait_for_timeout(700)
        pg.evaluate("document.querySelector('.phone').style.height='auto';document.querySelectorAll('.phone *').forEach(e=>{if(getComputedStyle(e).overflow==='hidden')e.style.overflow='visible'})")
        pg.wait_for_timeout(200)
        shot = os.path.join(ROOT, "docs", "audit", "%s_preview.png" % name.replace("-", "_"))
        pg.screenshot(path=shot, full_page=True)
        print("shot", shot)
    b.close()
