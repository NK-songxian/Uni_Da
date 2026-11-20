# -*- coding: utf-8 -*-
"""次级页批次：签到/积分/积分商城/社区/帖子详情 批量视觉预览"""
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


# ---------- checkin ----------
css_ck = load_css("checkin")
body_ck = (f'<div class="ck unida-page"><div class="ck__hero">'
           f'<div class="ck__spark ck__spark--a"></div><div class="ck__spark ck__spark--b"></div><div class="ck__spark ck__spark--c"></div>'
           f'<img class="ck__badge" src="static/unida/bubbles/check-cap.webp">'
           f'<span class="ck__title">打卡成功！</span><span class="ck__sub">已完成签到，玩得开心</span></div>'
           f'<div class="ck__reward"><div class="ck__reward-ico"><img class="ck__reward-img" src="static/icons-dark/flame.png"></div>'
           f'<div class="ck__reward-info"><span class="ck__reward-t">签到奖励</span><span class="ck__reward-s">积分已到账</span></div>'
           f'<span class="ck__reward-num">+20</span></div>'
           f'<div class="ck__btn">完成</div></div>')

# ---------- points ----------
css_pc = load_css("points")
TASKS = [("calendar.png", "每日签到", "每天一次", "5", True, "purple"),
         ("buddy.png", "完善个人资料", "填写头像和兴趣", "10", False, "green"),
         ("heart.png", "参加 1 个活动", "线下活动签到", "20", False, "orange"),
         ("bulb.png", "评价一次活动", "给出你的体验", "15", False, "pink")]
t_html = "".join(
    f'<div class="pc__task"><div class="pc__task-icon pc__task-icon--{tone}"><img class="pc__task-img" src="static/icons-dark/{ico}"></div>'
    f'<div class="pc__task-info"><span class="pc__task-title">{title}</span><span class="pc__task-sub">{sub}</span></div>'
    f'<div class="pc__task-btn{(" pc__task-btn--done" if done else "")}"><span class="pc__task-btn-t">{"已完成" if done else "+" + pt}</span></div></div>'
    for ico, title, sub, pt, done, tone in TASKS)
body_pc = (f'<div class="pc unida-page"><div class="pc__nav">'
           f'<div class="pc__back"><img class="pc__back-img" src="static/icons-dark/back.png"></div>'
           f'<span class="pc__title">积分中心</span><div class="pc__ph"></div></div>'
           f'<div class="pc__hero"><span class="pc__hero-label">我的积分</span><span class="pc__hero-num">1,280</span>'
           f'<div class="pc__hero-row"><div class="pc__hero-badge"><img class="pc__hero-badge-img" src="static/unida/bubbles/label-pop.webp"><span class="pc__hero-badge-t">Lv.5 活力星人</span></div>'
           f'<div class="pc__hero-sign"><span class="pc__hero-sign-t">每日签到 +5</span></div></div></div>'
           f'<div class="pc__sect"><span class="pc__sect-t">每日任务</span><span class="pc__sect-s">今日已完成 1/4</span></div>{t_html}'
           f'<div class="pc__mall"><div class="pc__mall-info"><span class="pc__mall-title">积分兑换好礼</span><span class="pc__mall-sub">精美礼品、专属特权等你来换</span></div>'
           f'<img class="pc__mall-img" src="static/unida/bubbles/corner-sticker-y.webp">'
           f'<img class="pc__chev" src="static/icons-dark/chevron.png"></div></div>')

# ---------- points-mall ----------
css_pm = load_css("points-mall")
GOODS = [("box.png", "定制帆布袋", "purple", "500"), ("clock.png", "咖啡兑换券", "orange", "800"),
         ("static/unida/bubbles/brand-badge-u.webp", "校园纪念徽章", "green", "400"), ("music.png", "电影票抵扣券", "pink", "1,500"),
         ("bulb.png", "专属头像框", "sky", "200"), ("heart.png", "免跑腿券", "purple", "600")]
CATS = ["全部", "实物礼品", "生活用品", "专属特权"]
g_html = "".join(
    f'<div class="pm__goods"><div class="pm__goods-cover pm__goods-cover--{tone}"><img class="pm__goods-ico" src="{ico if ico.startswith("static/") else "static/icons-dark/" + ico}"></div>'
    f'<div class="pm__goods-body"><span class="pm__goods-name">{name}</span>'
    f'<div class="pm__goods-foot"><span class="pm__goods-point">{pt} 积分</span>'
    f'<div class="pm__goods-btn"><span class="pm__goods-btn-t">兑换</span></div></div></div></div>'
    for ico, name, tone, pt in GOODS)
c_html_pm = "".join(
    f'<text class="pm__cat{" pm__cat--on" if i == 0 else ""}">{c}</text>' for i, c in enumerate(CATS))
body_pm = (f'<div class="pm unida-page"><div class="pm__nav">'
           f'<div class="pm__back"><img class="pm__back-img" src="static/icons-dark/back.png"></div>'
           f'<span class="pm__title">积分商城</span><div class="pm__ph"></div></div>'
           f'<div class="pm__bar"><div class="pm__coin"><span class="pm__coin-t">P</span></div>'
           f'<span class="pm__bar-label">我的积分</span><span class="pm__bar-num">1,280</span>'
           f'<img class="pm__chev" src="static/icons-dark/chevron.png"></div>'
           f'<div class="pm__cats">{c_html_pm}</div>'
           f'<div class="pm__banner"><div class="pm__banner-txt"><span class="pm__banner-title">积分兑换好礼</span><span class="pm__banner-sub">精美礼品 · 专属特权 · 校园周边</span></div>'
           f'<img class="pm__banner-img" src="static/unida/bubbles/board-cap.webp"></div>'
           f'<div class="pm__grid">{g_html}</div></div>')

# ---------- community ----------
css_cm = load_css("community", TAB_CSS)
POSTS = [
    ("阿星", "purple", "10分钟前 · 阳光大学", "校园生活", "今天的晚霞也太美了吧！中心湖边随手一拍就是大片，分享给同样热爱生活的小伙伴们～",
     ["linear-gradient(135deg,#FF8A3D,#FFD76A)", "linear-gradient(135deg,#805CFA,#B59BFF)"], 128, 24, 36, False, False),
    ("小林同学", "green", "1小时前 · 阳光大学", "找搭子", "有人一起去图书馆刷题吗？期末了，互相监督！位置已经占好啦，三楼靠窗～",
     [], 45, 18, 12, True, False),
    ("丸子", "orange", "2小时前 · 阳光大学", "社团活动", "周六下午街舞社在天台有公开课，零基础也能来玩，带上水就行！",
     ["linear-gradient(135deg,#F472B6,#FF8A3D)"], 89, 31, 27, False, False)]
p_html = "".join(
    f'<div class="cm__post"><div class="cm__post-head">'
    f'<div class="cm__post-avatar cm__post-avatar--{tone}"><span class="cm__post-avatar-ch">{user[0]}</span></div>'
    f'<div class="cm__post-user"><span class="cm__post-name">{user}</span><span class="cm__post-time">{meta}</span></div>'
    f'<div class="cm__post-tag cm__post-tag--{tone}"><span class="cm__post-tag-t">{tag}</span></div></div>'
    f'<span class="cm__post-text">{text}</span>'
    + (f'<div class="cm__post-images">' + "".join(f'<div class="cm__post-img" style="background:{g}"></div>' for g in imgs) + '</div>' if imgs else "")
    + f'<div class="cm__post-actions">'
    f'<div class="cm__act"><img class="cm__act-ico" src="static/icons-dark/heart.png"><span class="cm__act-n">{likes}</span></div>'
    f'<div class="cm__act"><img class="cm__act-ico" src="static/icons-dark/message.png"><span class="cm__act-n">{comments}</span></div>'
    f'<div class="cm__act{(" cm__act--fav" if faved else "")}"><img class="cm__act-ico" src="static/icons-dark/box.png"><span class="cm__act-n">{favs}</span></div>'
    f'<div class="cm__act"><img class="cm__act-ico" src="static/icons-dark/chevron.png"><span class="cm__act-n">分享</span></div>'
    f'</div></div>'
    for user, tone, meta, tag, text, imgs, likes, comments, favs, liked, faved in POSTS)
tab_html_cm = "".join(
    f'<div class="cm__tab{(" cm__tab--on" if i == 0 else "")}"><span class="cm__tab-t">{t}</span></div>'
    for i, t in enumerate(["推荐", "关注", "同校"]))
body_cm = (f'<div class="cm unida-page"><div class="cm__top">'
           f'<span class="cm__title">社区</span><span class="cm__sub">看看同学们在玩什么</span>'
           f'<div class="cm__tabs">{tab_html_cm}</div></div>'
           f'<div class="cm__publish"><div class="cm__pub-avatar"><span class="cm__pub-avatar-ch">我</span></div>'
           f'<span class="cm__pub-ph">分享你的校园生活…</span>'
           f'<div class="cm__pub-btn"><span class="cm__pub-btn-t">发布</span></div></div>'
           f'{p_html}<div class="cm__bottom-space"></div>{tabbar(1)}</div>')

# ---------- post-detail ----------
css_pd = load_css("post-detail")
COMMENTS = [("小林", "green", "太好看了！哪个机位拍的？", "5分钟前"),
            ("Leo", "orange", "校园的晚霞真的绝了，改天一起去拍！", "2分钟前")]
c_html_pd = "".join(
    f'<div class="pd__comment"><div class="pd__cavatar pd__cavatar--{tone}"><span class="pd__cavatar-ch">{name[0]}</span></div>'
    f'<div class="pd__cbody"><span class="pd__cname">{name}</span><span class="pd__ctext">{text}</span><span class="pd__ctime">{time}</span></div></div>'
    for name, tone, text, time in COMMENTS)
body_pd = (f'<div class="pd unida-page"><div class="pd__nav">'
           f'<div class="pd__back"><img class="pd__back-img" src="static/icons-dark/back.png"></div>'
           f'<span class="pd__title">帖子详情</span>'
           f'<div class="pd__more"><img class="pd__more-img" src="static/icons-dark/bell.png"></div></div>'
           f'<div class="pd__post"><div class="pd__head">'
           f'<div class="pd__avatar"><span class="pd__avatar-ch">阿</span></div>'
           f'<div class="pd__user"><span class="pd__name">阿星</span><span class="pd__time">10分钟前 · 阳光大学</span></div>'
           f'<div class="pd__follow"><span class="pd__follow-t">+ 关注</span></div></div>'
           f'<span class="pd__text">今天的晚霞也太美了吧！中心湖边随手一拍就是大片，分享给同样热爱生活的小伙伴们～</span>'
           f'<div class="pd__images"><div class="pd__img" style="background:linear-gradient(135deg,#FF8A3D,#FFD76A)"></div>'
           f'<div class="pd__img" style="background:linear-gradient(135deg,#805CFA,#B59BFF)"></div></div>'
           f'<div class="pd__tags"><div class="pd__tag pd__tag--purple"><span class="pd__tag-t"># 校园生活</span></div>'
           f'<div class="pd__tag pd__tag--orange"><span class="pd__tag-t"># 摄影</span></div></div>'
           f'<div class="pd__stats">'
           f'<div class="pd__stat"><img class="pd__stat-ico" src="static/icons-dark/heart.png"><span class="pd__stat-n">128 赞</span></div>'
           f'<div class="pd__stat"><img class="pd__stat-ico" src="static/icons-dark/message.png"><span class="pd__stat-n">2 评论</span></div>'
           f'<div class="pd__stat"><img class="pd__stat-ico" src="static/icons-dark/box.png"><span class="pd__stat-n">36 收藏</span></div></div></div>'
           f'<div class="pd__comments"><span class="pd__ctitle">评论 (2)</span>{c_html_pd}</div>'
           f'<div class="pd__scroll-end"></div>'
           f'<div class="pd__inputbar"><input class="pd__input" placeholder="说点什么…">'
           f'<div class="pd__send"><span class="pd__send-t">发送</span></div></div></div>')

JOBS = [
    ("checkin", body_ck, css_ck),
    ("points", body_pc, css_pc),
    ("points-mall", body_pm, css_pm),
    ("community", body_cm, css_cm),
    ("post-detail", body_pd, css_pd),
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
