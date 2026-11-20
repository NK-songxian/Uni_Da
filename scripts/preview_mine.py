# -*- coding: utf-8 -*-
"""「我的」个人中心页视觉预览：读产物 wxss + 手写等价结构（含 tabbar）"""
import os
import re

ROOT = r"H:\UniDA\unida"
DIST = os.path.join(ROOT, "unpackage", "dist", "dev", "mp-weixin")

wxss = open(os.path.join(DIST, "pages", "mine", "mine.wxss"), encoding="utf-8").read()
tab_css = open(os.path.join(DIST, "components", "unida-tabbar", "unida-tabbar.wxss"), encoding="utf-8").read()
css = wxss + tab_css
css = re.sub(r"(-?\d+(?:\.\d+)?)rpx", lambda m: f"{float(m.group(1))*0.5:g}px", css)
css = re.sub(r"\bimage\b", "img", css)

def life(icon, label):
    return f'<div class="mn__life"><img class="mn__life-ico" src="static/unida/mine/{icon}"><span class="mn__life-t">{label}</span></div>'

def widget(head_ico, title, body, deco, dcls):
    return (f'<div class="mn__widget"><div class="mn__whead">'
            f'<div class="mn__wbadge"><img class="mn__wbadge-ico" src="static/icons-dark/{head_ico}"></div>'
            f'<span class="mn__wt">{title}</span>'
            f'<img class="mn__chev" src="static/icons-dark/chevron.png"></div>'
            f'<div class="mn__wbody">{body}<img class="mn__wdeco {dcls}" src="static/unida/mine/{deco}"></div></div>')

GOAL = ('<div class="mn__wmain"><div class="mn__goalnum"><span class="mn__goal-big">3</span>'
        '<span class="mn__goal-sub">/5</span><span class="mn__goal-tip">项已完成</span></div>'
        '<div class="mn__bar"><div class="mn__bar-fill mn__bar-fill--60"></div></div></div>')
STREAK = ('<div class="mn__wmain"><div class="mn__streak"><span class="mn__streak-big">7</span>'
          '<span class="mn__streak-day">天</span></div>'
          '<span class="mn__streak-tip">再签 3 天得成长徽章！</span></div>')
CAL_DATES = "".join(
    f'<div class="mn__cal-cell{" mn__cal-cell--on" if d == 22 else ""}"><span class="mn__cal-d">{d}</span>'
    + ('<div class="mn__cal-dots"><div class="mn__dot mn__dot--y"></div><div class="mn__dot mn__dot--p"></div></div>' if d == 22 else '')
    + '</div>' for d in [20, 21, 22, 23, 24, 25, 26])
CAL = ('<div class="mn__cal"><div class="mn__cal-week">'
       + "".join(f'<span class="mn__cal-w">{w}</span>' for w in ["一", "二", "三", "四", "五", "六", "日"])
       + f'</div><div class="mn__cal-dates">{CAL_DATES}</div></div>')
BADGE = ('<div class="mn__wmain"><div class="mn__lvrow"><span class="mn__lv">Lv.4</span>'
         '<span class="mn__lv-name">活跃成长者</span></div>'
         '<div class="mn__bar"><div class="mn__bar-fill mn__bar-fill--68"></div></div>'
         '<div class="mn__growth"><span class="mn__growth-l">成长值</span><span class="mn__growth-v">680</span>'
         '<span class="mn__growth-s">/ 1,000</span></div></div>')

def lrow(icon, label, count=None):
    c = f'<div class="mn__count"><span class="mn__count-n">{count}</span></div>' if count is not None else ""
    return (f'<div class="mn__lrow"><img class="mn__lrow-ico" src="static/unida/mine/{icon}">'
            f'<span class="mn__lrow-t">{label}</span>{c}'
            f'<img class="mn__chev mn__chev--row" src="static/icons-dark/chevron.png"></div>')

TABS = """
<div class="unida-tabbar data-v-d86c95b2">
  <img class="tabbar-sheet data-v-d86c95b2" src="static/unida/tabbar/tabbar-sheet.png">
  <div class="tabbar-content data-v-d86c95b2">
    <div class="tab-item data-v-d86c95b2"><div class="icon-wrap data-v-d86c95b2"><img class="tab-ico data-v-d86c95b2" src="static/unida/tabbar/tab-home.png"></div><span class="tab-text data-v-d86c95b2">首页</span></div>
    <div class="tab-item data-v-d86c95b2"><div class="icon-wrap data-v-d86c95b2"><img class="tab-ico data-v-d86c95b2" src="static/unida/tabbar/tab-discover.png"></div><span class="tab-text data-v-d86c95b2">发现</span></div>
    <div class="tab-item publish-space data-v-d86c95b2"></div>
    <div class="tab-item data-v-d86c95b2"><div class="icon-wrap data-v-d86c95b2"><img class="tab-ico data-v-d86c95b2" src="static/unida/tabbar/tab-message.png"></div><span class="tab-text data-v-d86c95b2">消息</span></div>
    <div class="tab-item active data-v-d86c95b2"><div class="icon-wrap data-v-d86c95b2"><img class="tab-ico data-v-d86c95b2" src="static/unida/tabbar/tab-mine.png"></div><span class="tab-text data-v-d86c95b2">我的</span></div>
  </div>
  <div class="publish-center data-v-d86c95b2"><img class="publish-logo data-v-d86c95b2" src="static/unida/tabbar/publish-logo.png"><span class="publish-text data-v-d86c95b2">发布</span></div>
</div>
"""

BODY = f"""
<div class="mn">
  <div class="mn__head">
    <img class="mn__strip" src="static/unida/mine/header-strip.webp">
    <div class="mn__navzone mn__navzone--search"></div>
    <div class="mn__navzone mn__navzone--bell"></div>
  </div>
  <div class="mn__hero">
    <img class="mn__hero-img" src="static/unida/mine/hero-card.webp">
    <div class="mn__tap mn__tap--edit"></div>
    <div class="mn__tap mn__tap--s1"></div><div class="mn__tap mn__tap--s2"></div>
    <div class="mn__tap mn__tap--s3"></div><div class="mn__tap mn__tap--s4"></div>
  </div>
  <div class="mn__card">
    <div class="mn__cardhead">
      <div class="mn__cardtitle"><span class="mn__ct">我的校园生活</span><div class="mn__uline"></div></div>
      <span class="mn__cardsub">一站式管理我的校园体验</span>
    </div>
    <div class="mn__liferow">
      {life('life-act.png', '我的活动')}{life('life-team.png', '我的组队')}{life('life-fav.png', '我的收藏')}
      {life('life-pub.png', '我的发布')}{life('life-sign.png', '我的报名')}
    </div>
  </div>
  <div class="mn__sect">
    <div class="mn__sect-l"><div class="mn__spark mn__spark--a"></div><div class="mn__spark mn__spark--b"></div>
      <span class="mn__sect-t">我的小组件</span><span class="mn__sect-sub">我的成长 · 我的节奏 · 我的小宇宙</span></div>
    <div class="mn__manage">管理组件</div>
  </div>
  <div class="mn__grid">
    {widget('flame.png', '本周目标', GOAL, 'w-clip.png', 'mn__wdeco--clip')}
    {widget('calendar.png', '连续签到', STREAK, 'w-mascot.png', 'mn__wdeco--mascot')}
    {widget('clock.png', '活动日历', CAL, 'w-cal.png', 'mn__wdeco--cal')}
    {widget('heart.png', '成长徽章', BADGE, 'w-badge.png', 'mn__wdeco--badge')}
  </div>
  <div class="mn__card mn__list">
    {lrow('row-pub.png', '我的发布', 36)}{lrow('row-buddy.png', '我的搭子', 128)}
    {lrow('row-fav.png', '我的收藏', 42)}{lrow('row-order.png', '我的报名', 12)}
  </div>
  <div class="mn__card mn__list">
    {lrow('row-set.png', '设置')}{lrow('row-help.png', '帮助与反馈')}
  </div>
  <div class="mn__bottom-space"></div>
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

out = os.path.join(ROOT, "preview_mine.html")
open(out, "w", encoding="utf-8").write(HTML)

# 截图
from playwright.sync_api import sync_playwright
shot = os.path.join(ROOT, "docs", "audit", "mine_preview.png")
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
