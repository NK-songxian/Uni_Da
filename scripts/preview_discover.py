# -*- coding: utf-8 -*-
"""
发现页静态预览：从 discover.vue 抽取 scoped 样式，套等价结构，
用真实素材出发现页预览图，用于交付前视觉自检。
"""
import re
import os

ROOT = r"H:\UniDA\unida"
VUE = os.path.join(ROOT, "pages", "discover", "discover.vue")
TOK = os.path.join(ROOT, "common", "unida-tokens.scss")
OUT = os.path.join(ROOT, "preview_discover.html")

src = open(VUE, encoding="utf-8").read()
style = src.split('<style lang="scss" scoped>')[1].split("</style>")[0]
tokens_src = open(TOK, encoding="utf-8").read()

tokens = dict(re.findall(r"^\$([a-z0-9\-]+):\s*([^;]+);", tokens_src, re.M))
def _px(v):
    return re.sub(r"(-?\d+(?:\.\d+)?)rpx", lambda m: f"{float(m.group(1))*0.5:g}px", v.strip())
decls = "\n".join(f"  --{k}: {_px(v)};" for k, v in tokens.items())

def sub_var(m):
    return f"var(--{m.group(1)})" if m.group(1) in tokens else m.group(0)
style = re.sub(r"\$([a-z0-9\-]+)", sub_var, style)
style = re.sub(r"(-?\d+(?:\.\d+)?)rpx", lambda m: f"{float(m.group(1))*0.5:g}px", style)
style = re.sub(r"@import[^;]+;", "", style)
CSS = f":root {{\n{decls}\n}}\n{style}"

CARD = """
<div class="card">
  <div class="card__cover">
    <img class="card__img" src="{cover}">
    {hot}
    <div class="card__slot">{time}</div>
    <div class="card__ring" style="border-color:{bar}"><span class="card__ring-t" style="color:{bar}">缺{need}</span></div>
  </div>
  <div class="card__body">
    <div class="card__cate" style="color:{bar};background:{soft}">{cate}</div>
    <span class="card__title">{title}</span>
    <div class="card__meta"><img class="card__meta-ico" src="static/icons-dark/pin.png"><span class="card__meta-t">{place}</span></div>
    <div class="card__foot">
      <div class="card__avatars"><div class="card__av" style="background:{bar}">{ch}</div><span class="card__joined">{joined}/{total}</span></div>
      <span class="card__price" style="color:{priceC}">{price}</span>
    </div>
  </div>
</div>"""

cards = [
    dict(cover="static/art/art-campus.jpg", hot='<div class="card__flag">热门</div>', time="每天 20:00", bar="#805CFA", soft="rgba(128,92,250,.10)", need="8", cate="学习", title="一起准备英语四级 · 每日打卡互相监督", place="图书馆 4F", ch="星", joined="12", total="20", price="免费", priceC="#29CA83"),
    dict(cover="static/art/art-cheer.jpg", hot='<div class="card__flag">热门</div>', time="周日 05:30", bar="#29CA83", soft="rgba(41,202,131,.10)", need="4", cate="运动", title="周末爬山 · 登顶看日出，缺 4 人", place="南山公园", ch="陈", joined="6", total="10", price="AA", priceC="#29CA83"),
    dict(cover="static/art/art-tennis.jpg", hot="", time="今晚 20:00", bar="#69B9F5", soft="rgba(105,185,245,.12)", need="1", cate="运动", title="羽毛球双打 · 缺 1 人，水平不限", place="体育馆 3 号场", ch="林", joined="3", total="4", price="免费", priceC="#29CA83"),
    dict(cover="static/art/art-balls.jpg", hot="", time="即时", bar="#FFB020", soft="rgba(255,176,32,.14)", need="1", cate="跑腿", title="代取外卖到宿舍楼下 · 东门出发", place="东门驿站", ch="快", joined="0", total="1", price="¥4", priceC="#FFB020"),
    dict(cover="static/art/art-guitar.jpg", hot="", time="周六 18:00", bar="#805CFA", soft="rgba(128,92,250,.10)", need="4", cate="娱乐", title="找周末探店搭子 · 新开的烤肉店", place="大学城", ch="安", joined="2", total="6", price="AA", priceC="#29CA83"),
    dict(cover="static/art/art-campus.jpg", hot="", time="预约时间", bar="#29CA83", soft="rgba(41,202,131,.10)", need="2", cate="学习", title="PS 技能速成 · 1v1 教学，包教会", place="线上 / 面授", ch="苏", joined="3", total="5", price="¥50", priceC="#29CA83"),
]
cards_html = "\n".join(CARD.format(**c) for c in cards)

BODY = f"""
<div class="phone" style="padding-top:44px">
<div class="hd" style="background:transparent">
  <div class="hd__bar">
    <div class="hd__title"><span class="hd__title-main">发现</span><span class="hd__title-sub">找到现在就能一起的人</span></div>
    <div class="hd__search"><img class="hd__search-ico" src="static/icons-dark/search.png"><span class="hd__search-ph">搜索搭子、活动</span></div>
  </div>
</div>
<div class="maintabs">
  <div class="maintabs__item maintabs__item--on"><img class="maintabs__ico" src="static/unida/illustrations/icon-run.png"><span class="maintabs__label">找搭子</span></div>
  <div class="maintabs__item"><img class="maintabs__ico" src="static/unida/illustrations/icon-horn-v2.png"><span class="maintabs__label">校园活动</span></div>
  <div class="maintabs__item"><img class="maintabs__ico" src="static/unida/illustrations/icon-team-v2.png"><span class="maintabs__label">社团招新</span></div>
</div>
<div class="chips"><div class="chips__inner">
  <div class="chips__item chips__item--on">全部</div><div class="chips__item">学习</div><div class="chips__item">运动</div><div class="chips__item">娱乐</div><div class="chips__item">生活</div><div class="chips__item">社团</div>
</div></div>
<div class="sortbar">
  <div class="sortbar__l"><div class="sortbar__item sortbar__item--on">综合</div><div class="sortbar__item">最新</div><div class="sortbar__item">最热</div></div>
  <span class="sortbar__count">共 12 条</span>
</div>
<div class="grid">{cards_html}</div>
</div>
"""

BASE = """
* { margin:0; padding:0; box-sizing:border-box; }
html, body { background:#ddd; overflow-x:hidden; }
.phone { width:375px; margin:0; background:#F5F0FF; font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; padding-bottom:40px; }
img { display:block; }
.card__img { object-fit:cover; }
.maintabs__ico,.hd__search-ico,.card__meta-ico{object-fit:contain}
"""
html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>{BASE}{CSS}</style></head><body>{BODY}</body></html>"""
open(OUT, "w", encoding="utf-8").write(html)
print("已生成", OUT, len(html), "字符")
