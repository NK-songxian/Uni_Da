# -*- coding: utf-8 -*-
"""次级页批次3：他人主页/活动日历/活动评价/举报/资料设置 批量视觉预览"""
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


def html_for(body, css):
    html = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#ddd; font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }
.phone { width:375px; margin:0 auto; background:#F5F0FF; }
img { display:block; }
span { display:inline; }
input,textarea { border:none; outline:none; background:transparent; }
__CSS__
</style></head><body><div class="phone">__BODY__</div></body></html>"""
    return html.replace("__CSS__", css).replace("__BODY__", body)


# ---------- user-home ----------
css_uh = load_css("user-home")
TAGS = ["label-sport", "label-study", "label-fun", "label-hot"]
t_html_uh = "".join(f'<img class="uh__tag-img" src="static/unida/bubbles/{t}.webp">' for t in TAGS)
FEEDS = [("linear-gradient(135deg,#FF8A3D,#FFD76A)", "heart.png", "中心湖的晚霞，随手拍都是大片！", "10分钟前"),
         ("linear-gradient(135deg,#805CFA,#B59BFF)", "buddy.png", "周末约球，有没有一起的？", "昨天")]
f_html = "".join(
    f'<div class="uh__feed"><div class="uh__feed-cover" style="background:{bg}"><img class="uh__feed-img" src="static/icons-dark/{ico}"></div>'
    f'<div class="uh__feed-body"><span class="uh__feed-text">{text}</span><div class="uh__feed-meta"><img class="uh__feed-meta-ico" src="static/icons-dark/clock.png"><span class="uh__feed-meta-t">{time}</span></div></div>'
    f'<img class="uh__chev" src="static/icons-dark/chevron.png"></div>'
    for bg, ico, text, time in FEEDS)
STATS = [("12", "动态"), ("86", "获赞"), ("24", "关注"), ("132", "粉丝")]
s_html_uh = "".join(f'<div class="uh__stat"><span class="uh__stat-num">{n}</span><span class="uh__stat-label">{l}</span></div>' for n, l in STATS)
body_uh = (f'<div class="uh unida-page"><div class="uh__hero"><div class="uh__nav">'
           f'<div class="uh__nav-btn"><img class="uh__nav-img" src="static/icons-dark/back.png"></div>'
           f'<span class="uh__nav-title">个人主页</span>'
           f'<div class="uh__nav-btn"><img class="uh__nav-img" src="static/icons-dark/bell.png"></div></div>'
           f'<div class="uh__profile"><div class="uh__avatar"><span class="uh__avatar-ch">星</span></div>'
           f'<div class="uh__info"><div class="uh__name-row"><span class="uh__name">阿星</span><img class="uh__shield" src="static/unida/bubbles/shield-check.webp"></div>'
           f'<span class="uh__sub">阳光大学 · 已认证 <span class="uh__dot">·</span> <span class="uh__score">4.9</span> 分</span></div></div>'
           f'<span class="uh__bio">热爱运动，喜欢认识新朋友～ 一起让校园生活更有趣！</span></div>'
           f'<div class="uh__stats">{s_html_uh}</div>'
           f'<div class="uh__actions"><div class="uh__btn uh__btn--primary"><img class="uh__btn-img" src="static/icons-dark/message.png"><span class="uh__btn-t">私信</span></div>'
           f'<div class="uh__btn uh__btn--outline"><span class="uh__btn-t">+ 关注</span></div></div>'
           f'<div class="uh__sect"><span class="uh__sect-t">兴趣标签</span><div class="uh__tags">{t_html_uh}</div></div>'
           f'<div class="uh__sect"><span class="uh__sect-t">TA 的动态</span>{f_html}</div></div>')

# ---------- calendar ----------
css_cal = load_css("calendar")
# 2026年11月1日是周日 → 无空格；30天；17/20/21 有日程
days_html = ""
for n in range(1, 31):
    on = " cal__day--on" if n == 21 else ""
    dot = '<div class="cal__dot"></div>' if n in (17, 20, 21) else ""
    days_html += f'<div class="cal__day{on}"><span class="cal__day-t">{n}</span>{dot}</div>'
weeks_html = "".join(f'<span class="cal__week-t">{w}</span>' for w in ["日", "一", "二", "三", "四", "五", "六"])
SCHEDULES = [("摄影分享会 · 校园风景速成", "15:00-16:30", "图书馆报告厅", "#805CFA", True),
             ("预约了羽毛球场地", "18:30-20:00", "体育馆 3 号场", "#29CA83", False),
             ("小组作业讨论", "20:00-21:00", "3 教 405", "#FF9B77", False)]
item_html = "".join(
    f'<div class="cal__item"><div class="cal__item-line" style="background:{c}"></div>'
    f'<div class="cal__item-body"><span class="cal__item-title">{t}</span>'
    f'<div class="cal__item-meta"><img class="cal__item-ico" src="static/icons-dark/clock.png"><span class="cal__item-meta-t">{tm}</span></div>'
    f'<div class="cal__item-meta"><img class="cal__item-ico" src="static/icons-dark/pin.png"><span class="cal__item-meta-t">{pl}</span></div></div>'
    f'<div class="cal__status{(" cal__status--done" if done else "")}"><span class="cal__status-t">{"已完成" if done else "待进行"}</span></div></div>'
    for t, tm, pl, c, done in SCHEDULES)
body_cal = (f'<div class="cal unida-page"><div class="cal__nav">'
            f'<div class="cal__back"><img class="cal__back-img" src="static/icons-dark/back.png"></div>'
            f'<span class="cal__title">我的日程</span>'
            f'<div class="cal__add"><img class="cal__add-img" src="static/icons-dark/plus.png"></div></div>'
            f'<div class="cal__calendar"><div class="cal__month">'
            f'<div class="cal__month-btn"><img class="cal__month-img" src="static/icons-dark/back.png"></div>'
            f'<span class="cal__month-t">2026 年 11 月</span>'
            f'<div class="cal__month-btn"><img class="cal__month-img cal__month-img--next" src="static/icons-dark/back.png"></div></div>'
            f'<div class="cal__week">{weeks_html}</div><div class="cal__days">{days_html}</div>'
            f'<div class="cal__legend"><div class="cal__legend-item"><div class="cal__dot cal__dot--legend"></div><span class="cal__legend-t">有日程</span></div>'
            f'<div class="cal__legend-item"><img class="cal__legend-img" src="static/unida/bubbles/cal-check.webp"><span class="cal__legend-t">今日已签</span></div></div></div>'
            f'<div class="cal__sect"><div class="cal__sect-head"><div class="cal__sect-head-l"><span class="cal__sect-t">11月21日</span>'
            f'<img class="cal__sect-badge" src="static/unida/bubbles/time-now.webp"></div><span class="cal__sect-s">共 3 项</span></div>{item_html}</div></div>')

# ---------- review ----------
css_rv = load_css("review")
stars_html = "".join(f'<div class="rv__star{" rv__star--on" if i < 5 else ""}"></div>' for i in range(5))
TAGS_RV = ["组织有序", "氛围超好", "认识新朋友", "场地不错", "值得一来", "下次还来"]
tags_html = "".join(f'<div class="rv__tag{(" rv__tag--on" if i in (0, 1, 4) else "")}"><span class="rv__tag-t">{t}</span></div>' for i, t in enumerate(TAGS_RV))
body_rv = (f'<div class="rv unida-page"><div class="rv__nav">'
           f'<div class="rv__back"><img class="rv__back-img" src="static/icons-dark/back.png"></div>'
           f'<span class="rv__title">活动评价</span><div class="rv__ph"></div></div>'
           f'<div class="rv__event"><div class="rv__event-cover"><img class="rv__event-img" src="static/unida/bubbles/pennant-star.webp"></div>'
           f'<div class="rv__event-info"><span class="rv__event-title">校园草地音乐会</span><div class="rv__event-meta"><img class="rv__event-ico" src="static/icons-dark/calendar.png"><span class="rv__event-meta-t">本周六 · 中心草坪</span></div></div>'
           f'<img class="rv__event-badge" src="static/unida/bubbles/label-hot.webp"></div>'
           f'<div class="rv__card"><span class="rv__label">整体体验</span><div class="rv__stars">{stars_html}</div><span class="rv__hint">超棒！</span></div>'
           f'<div class="rv__card"><span class="rv__label">快速评价 <span class="rv__label-sub">（可多选）</span></span><div class="rv__tags">{tags_html}</div></div>'
           f'<div class="rv__card"><span class="rv__label">说说你的感受</span><textarea class="rv__textarea" placeholder="活动怎么样？有什么想说的～"></textarea><span class="rv__count">0/200</span></div>'
           f'<div class="rv__submit"><span class="rv__submit-t">提交评价</span></div></div>')

# ---------- report ----------
css_rp = load_css("report")
REASONS = ["色情低俗", "虚假信息 / 诈骗", "人身攻击", "广告骚扰", "侵权内容", "其他原因"]
reason_html = ""
for i, r in enumerate(REASONS):
    on = i == 1
    dot_html = '<div class="rp__radio-dot"></div>' if on else ""
    check_html = '<img class="rp__reason-check" src="static/unida/bubbles/check-purple.webp">' if on else ""
    reason_html += (f'<div class="rp__reason{" rp__reason--on" if on else ""}">'
                    f'<div class="rp__radio{" rp__radio--on" if on else ""}">{dot_html}</div>'
                    f'<span class="rp__reason-t">{r}</span>{check_html}</div>')
body_rp = (f'<div class="rp unida-page"><div class="rp__nav">'
           f'<div class="rp__back"><img class="rp__back-img" src="static/icons-dark/back.png"></div>'
           f'<span class="rp__title">举报</span><div class="rp__ph"></div></div>'
           f'<div class="rp__tip"><img class="rp__tip-img" src="static/unida/bubbles/shield-check.webp">'
           f'<span class="rp__tip-text">请选择举报原因，我们会尽快核实处理。恶意举报将被处罚。</span></div>'
           f'<div class="rp__card"><div class="rp__label-row"><span class="rp__label">举报原因</span><span class="rp__req">*</span></div>{reason_html}</div>'
           f'<div class="rp__card"><span class="rp__label">补充说明 <span class="rp__label-sub">（选填）</span></span>'
           f'<textarea class="rp__textarea" placeholder="请描述具体情况，帮助我们更快处理…"></textarea><span class="rp__count">0/200</span></div>'
           f'<div class="rp__submit"><span class="rp__submit-t">提交举报</span></div></div>')

# ---------- profile-setup（步骤1/2/3）----------
css_st = load_css("profile-setup")
INTERESTS = [("heart.png", "purple", "学习"), ("flame.png", "orange", "运动"), ("music.png", "pink", "娱乐"),
             ("bulb.png", "sky", "教学"), ("box.png", "green", "跑腿"), ("calendar.png", "sun", "活动")]
interest_html = "".join(
    f'<div class="st__interest{(" st__interest--on" if i in (0, 1) else "")}"><div class="st__interest-icon st__interest-icon--{tone}">'
    f'<img class="st__interest-img" src="static/icons-dark/{ico}"></div><span class="st__interest-label">{label}</span></div>'
    for i, (ico, tone, label) in enumerate(INTERESTS))


def setup_top(step):
    def dot(n):
        cls = "st__dot" if ((step == 1 and n == 1) or (step == 2 and n == 2) or (step == 3 and n == 3) or (step > n)) else "st__dot"
        return f'<div class="{cls}"><span class="st__dot-t">{n}</span></div>'
    def stepcls(n):
        on = " st__step--on" if step == n else ""
        done = " st__step--done" if step > n else ""
        return f'class="st__step{on}{done}"'
    l1 = " st__line--on" if step > 1 else ""
    l2 = " st__line--on" if step > 2 else ""
    return (f'<div class="st__top"><div class="st__back"><img class="st__back-img" src="static/icons-dark/back.png"></div>'
            f'<div class="st__steps"><div {stepcls(1)}>{dot(1)}<span class="st__step-t">校园验证</span></div>'
            f'<div class="st__line{l1}"></div><div {stepcls(2)}>{dot(2)}<span class="st__step-t">完善信息</span></div>'
            f'<div class="st__line{l2}"></div><div {stepcls(3)}>{dot(3)}<span class="st__step-t">完成</span></div></div></div>')


body_st1 = (f'<div class="st unida-page">{setup_top(1)}<div class="st__body">'
            f'<span class="st__title">完善校园信息</span><span class="st__sub">开启你的 UNIDA 校园之旅</span>'
            f'<div class="st__field"><div class="st__label-row"><img class="st__label-ico" src="static/icons-dark/calendar.png">'
            f'<span class="st__label">选择你的学校</span><span class="st__req">*</span></div>'
            f'<div class="st__select"><span class="st__select-t st__select-t--ph">请选择所在学校</span><img class="st__select-arrow" src="static/icons-dark/chevron.png"></div></div>'
            f'<div class="st__field"><div class="st__label-row"><img class="st__label-ico" src="static/icons-dark/bulb.png">'
            f'<span class="st__label">选择你的兴趣</span><span class="st__label-sub">（可多选）</span></div>'
            f'<div class="st__interests">{interest_html}</div></div>'
            f'<div class="st__footer"><div class="st__next"><span class="st__next-t">下一步</span></div>'
            f'<span class="st__skip">先看看，稍后再完善 ›</span></div></div></div>')
body_st2 = (f'<div class="st unida-page">{setup_top(2)}<div class="st__body">'
            f'<span class="st__title">完善个人资料</span><span class="st__sub">让大家更快认识你</span>'
            f'<div class="st__avatar-wrap"><div class="st__avatar"><span class="st__avatar-ch">我</span></div>'
            f'<div class="st__avatar-tip"><img class="st__avatar-pen" src="static/icons-dark/bulb.png"><span class="st__avatar-tip-t">点击更换头像</span></div></div>'
            f'<div class="st__field"><span class="st__label">昵称</span><input class="st__input" placeholder="给自己起个好听的名字"><span class="st__input-count">0/16</span></div>'
            f'<div class="st__footer"><div class="st__next"><span class="st__next-t">完成</span></div></div></div></div>')
body_st3 = (f'<div class="st unida-page">{setup_top(3)}<div class="st__done">'
            f'<img class="st__done-badge" src="static/unida/bubbles/check-cap.webp">'
            f'<span class="st__done-title">欢迎加入 UNIDA！</span><span class="st__done-sub">在校园，找到和你同频的人</span>'
            f'<div class="st__next st__next--inline"><span class="st__next-t">开启校园之旅</span></div></div></div>')

JOBS = [
    ("user_home", body_uh, css_uh),
    ("calendar", body_cal, css_cal),
    ("review", body_rv, css_rv),
    ("report", body_rp, css_rp),
    ("profile_setup_step1", body_st1, css_st),
    ("profile_setup_step2", body_st2, css_st),
    ("profile_setup_step3", body_st3, css_st),
]

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_page(viewport={"width": 375, "height": 900})
    for name, body, css in JOBS:
        out = os.path.join(ROOT, "preview_%s.html" % name)
        open(out, "w", encoding="utf-8").write(html_for(body, css))
        pg.goto("file:///" + out.replace("\\", "/"))
        pg.wait_for_timeout(700)
        pg.evaluate("document.querySelector('.phone').style.height='auto';document.querySelectorAll('.phone *').forEach(e=>{if(getComputedStyle(e).overflow==='hidden')e.style.overflow='visible'})")
        pg.wait_for_timeout(200)
        shot = os.path.join(ROOT, "docs", "audit", "%s_preview.png" % name)
        pg.screenshot(path=shot, full_page=True)
        print("shot", shot)
    b.close()
