# -*- coding: utf-8 -*-
"""收尾批次：用户协议/微信登录/手机登录/旧入口页 批量视觉预览"""
import os
import re

ROOT = r"H:\UniDA\unida"
DIST = os.path.join(ROOT, "unpackage", "dist", "dev", "mp-weixin")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def load_css(page):
    wxss = open(os.path.join(DIST, "pages", page, page + ".wxss"), encoding="utf-8").read()
    css = re.sub(r"(-?\d+(?:\.\d+)?)rpx", lambda m: f"{float(m.group(1))*0.5:g}px", wxss)
    css = re.sub(r"\bimage\b", "img", css)
    return css


def html_for(body, css):
    html = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#ddd; font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }
.phone { width:375px; margin:0 auto; background:#F5F0FF; }
img { display:block; }
span { display:inline; }
input,textarea { border:none; outline:none; background:transparent; }
button { border:none; font-family:inherit; }
__CSS__
</style></head><body><div class="phone">__BODY__</div></body></html>"""
    return html.replace("__CSS__", css).replace("__BODY__", body)


# ---------- agreement ----------
css_ag = load_css("agreement")
CLAUSES = [
    ("服务说明", "UNIDA 是面向大学生的校园社交与生活互助平台，提供找搭子、校园活动、技能教学、跑腿互助、校园社区等功能。用户须为在校大学生或经校园认证的用户。"),
    ("用户账号", "使用微信一键登录或手机号登录即表示你同意创建 UNIDA 账号。你应妥善保管账号信息，因账号泄露产生的责任由用户自行承担。"),
    ("信息收集与使用", "我们遵循最小必要原则收集信息，包括：微信开放标识、手机号（经授权）、学校信息、用户主动填写的资料与发布内容。我们不会在未经授权的情况下向第三方提供你的个人信息。"),
    ("用户内容规范", "用户发布的内容须合法、真实、健康，不得包含违法违规、虚假、低俗、侵权信息。平台有权对违规内容进行处理，并提供举报渠道。"),
    ("免责声明", "平台仅提供信息发布与撮合服务，线下活动的安全与责任由参与者自行承担。请在参与活动时注意人身与财产安全。"),
    ("协议更新", "本协议可能随业务发展更新，更新后将在小程序内公示。继续使用服务即视为接受更新后的协议。")
]
clause_html = "".join(
    f'<div class="ag__clause"><div class="ag__clause-head"><div class="ag__clause-no"><span class="ag__clause-no-t">{i+1}</span></div>'
    f'<span class="ag__h2">{t}</span></div><span class="ag__p">{p}</span></div>'
    for i, (t, p) in enumerate(CLAUSES))
body_ag = (f'<div class="ag unida-page"><div class="ag__nav">'
           f'<div class="ag__back"><img class="ag__back-img" src="static/icons-dark/back.png"></div>'
           f'<span class="ag__title">用户协议</span><div class="ag__ph"></div></div>'
           f'<div class="ag__doc"><div class="ag__head"><img class="ag__head-badge" src="static/unida/bubbles/brand-badge-u.webp">'
           f'<div class="ag__head-info"><span class="ag__h">UNIDA（有你搭）用户协议</span><span class="ag__date">更新日期：2026年11月18日</span></div></div>'
           f'<span class="ag__p">欢迎使用 UNIDA（有你搭）。本协议适用于由校园用户使用的 UNIDA 微信小程序服务。请在使用前仔细阅读并理解本协议的全部内容。</span>'
           f'{clause_html}'
           f'<div class="ag__footer"><img class="ag__footer-ico" src="static/unida/bubbles/shield-u.webp">'
           f'<span class="ag__footer-note">如有疑问，请通过「我的 - 举报与反馈」联系我们。</span></div></div></div>')

# ---------- login-wechat ----------
css_lw = load_css("login-wechat")
FEATURES_LW = [("flame.png", "快速登录", "一键进入，无需填写", "orange"),
               ("buddy.png", "安全可信", "微信官方授权保障", "green"),
               ("calendar.png", "校园专属", "仅限校园用户加入", "purple")]
f_html_lw = "".join(
    f'<div class="lw__feature"><div class="lw__feature-icon lw__feature-icon--{tone}"><img class="lw__feature-img" src="static/icons-dark/{ico}"></div>'
    f'<span class="lw__feature-title">{title}</span><span class="lw__feature-sub">{sub}</span></div>'
    for ico, title, sub, tone in FEATURES_LW)
body_lw = (f'<div class="lw unida-page"><div class="lw__blob lw__blob--1"></div><div class="lw__blob lw__blob--2"></div>'
           f'<div class="lw__back"><img class="lw__back-img" src="static/icons-dark/back.png"><span class="lw__back-t">返回</span></div>'
           f'<div class="lw__center"><div class="lw__wx"><img class="lw__wx-img" src="static/unida/bubbles/brand-badge-u.webp">'
           f'<img class="lw__wx-check" src="static/unida/bubbles/check-green.webp"></div>'
           f'<span class="lw__title">微信一键登录</span><span class="lw__desc">使用微信登录 UNIDA<br>免注册，安全便捷</span></div>'
           f'<div class="lw__features">{f_html_lw}</div>'
           f'<div class="lw__actions"><button class="lw__btn"><span class="lw__btn-t">微信一键登录</span></button>'
           f'<div class="lw__switch"><span class="lw__switch-t">切换手机号登录</span></div>'
           f'<div class="lw__agree"><div class="lw__checkbox lw__checkbox--on"><img class="lw__checkbox-img" src="static/unida/bubbles/check-purple.webp"></div>'
           f'<span class="lw__agree-t">我已阅读并同意 </span><span class="lw__link">《用户协议》</span><span class="lw__link">《隐私政策》</span></div></div></div>')

# ---------- phone-login ----------
css_pl = load_css("phone-login")
body_pl = (f'<div class="pl unida-page"><div class="pl__back"><img class="pl__back-img" src="static/icons-dark/back.png"><span class="pl__back-t">返回</span></div>'
           f'<div class="pl__head"><img class="pl__head-badge" src="static/unida/bubbles/pin-purple-u.webp">'
           f'<span class="pl__title">手机号登录</span><span class="pl__sub">输入手机号，快捷登录 UNIDA</span></div>'
           f'<div class="pl__form"><div class="pl__item"><div class="pl__prefix"><span class="pl__prefix-t">+86</span><img class="pl__prefix-chev" src="static/icons-dark/chevron.png"></div>'
           f'<input class="pl__input" placeholder="请输入手机号" value="13800138000"></div>'
           f'<div class="pl__item"><input class="pl__input pl__input--code" placeholder="请输入验证码">'
           f'<div class="pl__code"><span class="pl__code-t">获取验证码</span></div></div></div>'
           f'<div class="pl__agree"><div class="pl__checkbox pl__checkbox--on"><img class="pl__checkbox-img" src="static/unida/bubbles/check-purple.webp"></div>'
           f'<span class="pl__agree-t">我已阅读并同意 </span><span class="pl__link">《用户协议》</span><span class="pl__link">《隐私政策》</span></div>'
           f'<div class="pl__btn"><span class="pl__btn-t">登录</span></div><span class="pl__tip">未注册手机号将自动创建账号</span></div>')

# ---------- index ----------
css_ix = load_css("index")
FEATURES_IX = [("buddy.png", "找搭子", "自习 · 吃饭 · 运动，同频同行", "purple"),
               ("calendar.png", "校园活动", "讲座 · 比赛 · 舞台，不错过精彩", "orange"),
               ("box.png", "生活互助", "跑腿 · 代取 · 借还，同学来帮忙", "green")]
f_html_ix = "".join(
    f'<div class="ix__feature"><div class="ix__feature-icon ix__feature-icon--{tone}"><img class="ix__feature-img" src="static/icons-dark/{ico}"></div>'
    f'<div class="ix__feature-info"><span class="ix__feature-t">{title}</span><span class="ix__feature-s">{sub}</span></div></div>'
    for ico, title, sub, tone in FEATURES_IX)
body_ix = (f'<div class="ix unida-page"><div class="ix__glow"></div>'
           f'<div class="ix__hero"><div class="ix__frame"><img class="ix__frame-img" src="static/unida/bubbles/frame-unida-cloud.webp">'
           f'<img class="ix__badge" src="static/unida/bubbles/brand-badge-u.webp"></div>'
           f'<span class="ix__brand">UNIDA</span><span class="ix__slogan">有你搭 · 在校园，找到同频的伙伴</span></div>'
           f'<div class="ix__features">{f_html_ix}</div>'
           f'<div class="ix__actions"><div class="ix__btn"><span class="ix__btn-t">开启校园之旅</span></div>'
           f'<div class="ix__sub-btn"><span class="ix__sub-btn-t">已有账号？登录</span></div></div></div>')

JOBS = [
    ("agreement", body_ag, css_ag),
    ("login_wechat", body_lw, css_lw),
    ("phone_login", body_pl, css_pl),
    ("index", body_ix, css_ix),
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
