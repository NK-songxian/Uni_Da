# -*- coding: utf-8 -*-
"""
把 home.vue 的 scoped 样式转成浏览器可渲染的 CSS，套一个等价静态结构，
用真实素材出一张 375×812 的 iPhone 预览图，用于交付前视觉自检。
（rpx → px：以 375pt 宽屏为基准，1rpx = 0.5px）
"""
import re
import os

ROOT = r"H:\UniDA\unida"
VUE = os.path.join(ROOT, "pages", "home", "home.vue")
TOK = os.path.join(ROOT, "common", "unida-tokens.scss")
OUT = os.path.join(ROOT, "preview.html")

src = open(VUE, encoding="utf-8").read()
style = src.split("<style lang=\"scss\" scoped>")[1].split("</style>")[0]
tokens_src = open(TOK, encoding="utf-8").read()

# 1) SCSS 变量 → CSS 变量
tokens = dict(re.findall(r"^\$([a-z0-9\-]+):\s*([^;]+);", tokens_src, re.M))
def _px(v):
    return re.sub(r"(-?\d+(?:\.\d+)?)rpx", lambda m: f"{float(m.group(1))*0.5:g}px", v.strip())
decls = "\n".join(f"  --{k}: {_px(v)};" for k, v in tokens.items())

def sub_var(m):
    name = m.group(1)
    return f"var(--{name})" if name in tokens else m.group(0)

style = re.sub(r"\$([a-z0-9\-]+)", sub_var, style)

# 2) rpx → px（1rpx = 0.5px）
style = re.sub(r"(-?\d+(?:\.\d+)?)rpx", lambda m: f"{float(m.group(1))*0.5:g}px", style)

# 3) 去掉 scss 专有语法
style = re.sub(r"@import[^;]+;", "", style)

CSS = f":root {{\n{decls}\n}}\n{style}"

BODY = """
<div class="phone">
<!-- 顶栏 -->
<div class="hd">
  <div class="hd__bar">
    <div class="hd__school"><img class="hd__ico" src="static/icons-dark/pin.png"><span class="hd__name">江南大学</span><img class="hd__chev" src="static/icons-dark/chevron.png"></div>
    <img class="hd__logo" src="static/unida/brand/logo-topbar.png" style="height:22px">
    <div class="hd__bell"><img class="hd__ico" src="static/icons-dark/bell.png"><div class="hd__dot"></div></div>
  </div>
</div>

<!-- Hero 融合 Banner -->
<div class="hero">
  <div class="hero__slide hero__slide--brand">
    <img class="hero__sky" src="static/unida/backgrounds/bg-campus-sky.jpg">
    <div class="hero__tint"></div>
    <div class="hero__spark hero__spark--1"></div>
    <div class="hero__spark hero__spark--2"></div>
    <div class="hero__spark hero__spark--3"></div>
    <div class="hero__copy">
      <div class="hero__pill"><div class="hero__live"></div><span class="hero__pill-txt">今天 <span class="hero__num">1,284</span> 位同学找到了搭子</span></div>
      <span class="hero__title">在校园，</span>
      <span class="hero__title hero__title--2">找到和你同频的人</span>
      <div class="hero__search"><img class="hero__search-ico" src="static/icons-dark/search.png"><span class="hero__search-ph">搜活动、搭子、社团</span></div>
    </div>
    <img class="hero__trio" src="static/unida/characters/trio-back.webp">
    <img class="hero__planet" src="static/unida/mascot/u-planet.png">
    <div class="hero__fade"></div>
  </div>
  <div class="hero__dots"><div class="hero__dot hero__dot--on"></div><div class="hero__dot"></div><div class="hero__dot"></div><div class="hero__dot"></div></div>
</div>

<!-- 任务大卡预览（模拟第2屏） -->
<div class="hero hero--task">
  <div class="hero__slide hero__slide--task" style="background:linear-gradient(135deg,#EFE7FF 0%,#F6EEFF 100%)">
    <div class="task__tag" style="background:linear-gradient(135deg,#9B7BFF,#6C3FF2)">校园推广</div>
    <div class="task__body">
      <span class="task__eyebrow">校园精选 · 高积分任务</span>
      <span class="task__title">图书馆自习搭子招募</span>
      <span class="task__desc">发布即得 200 积分 · 今日剩 3 席</span>
      <div class="task__cta"><span class="task__cta-t">去完成</span></div>
    </div>
    <div class="task__point"><span class="task__point-num">200</span><span class="task__point-unit">积分</span></div>
    <img class="task__art" src="static/unida/characters/trio-back.webp">
    <div class="task__halo"></div>
  </div>
  <div class="hero__dots"><div class="hero__dot"></div><div class="hero__dot hero__dot--on"></div><div class="hero__dot"></div><div class="hero__dot"></div></div>
</div>

<!-- 类目 -->
<div class="cats">
  <div class="cats__item"><div class="cats__fig" style="background:rgba(128,92,250,.10)"><img class="cats__img" src="static/unida/illustrations/icon-study.png"></div><span class="cats__label">学习组队</span></div>
  <div class="cats__item"><div class="cats__fig" style="background:rgba(41,202,131,.10)"><img class="cats__img" src="static/unida/illustrations/icon-run.png"></div><span class="cats__label">运动搭子</span></div>
  <div class="cats__item"><div class="cats__fig" style="background:rgba(255,201,79,.16)"><img class="cats__img" src="static/unida/illustrations/icon-horn-v2.png"></div><span class="cats__label">校园活动</span></div>
  <div class="cats__item"><div class="cats__fig" style="background:rgba(128,92,250,.09)"><img class="cats__img" src="static/unida/illustrations/icon-gift-v2.png"></div><span class="cats__label">生活互助</span></div>
  <div class="cats__item"><div class="cats__fig" style="background:rgba(105,185,245,.11)"><img class="cats__img" src="static/unida/illustrations/icon-team-v2.png"></div><span class="cats__label">社团招新</span></div>
  <div class="cats__item"><div class="cats__fig" style="background:rgba(169,139,255,.14)"><img class="cats__img" src="static/unida/illustrations/icon-planet.png"></div><span class="cats__label">同校广场</span></div>
</div>

<!-- 现在可以搭 -->
<div class="sec">
  <div class="sec__hd"><div class="sec__hd-l"><span class="sec__title">现在可以搭</span><span class="sec__sub">2 小时内 · 还缺人</span></div><span class="sec__more">全部</span></div>
  <div class="rail"><div class="rail__inner">
    <div class="now">
      <div class="now__cover"><img class="now__img" src="static/art/art-cheer.jpg"><div class="now__rank">1</div><div class="now__clock">40 分钟后</div></div>
      <div class="now__body">
        <span class="now__title">周五夜跑 · 环湖 5 公里</span>
        <div class="now__meta"><img class="now__ico" src="static/icons-dark/clock.png"><span class="now__meta-txt">19:30</span><div class="now__sep"></div><img class="now__ico" src="static/icons-dark/pin.png"><span class="now__meta-txt">中心湖广场</span></div>
        <div class="now__foot">
          <div class="now__people">
            <div class="now__av" style="background:linear-gradient(135deg,#805CFA,#A98BFF)">星</div>
            <div class="now__av" style="background:linear-gradient(135deg,#29CA83,#93EDCF)">林</div>
            <div class="now__av" style="background:linear-gradient(135deg,#FFC94F,#FFE39B)">L</div>
            <span class="now__count">3/8</span>
          </div>
          <div class="now__join">加入</div>
        </div>
      </div>
    </div>
    <div class="now">
      <div class="now__cover"><img class="now__img" src="static/art/art-tennis.jpg"><div class="now__rank">2</div><div class="now__clock">1 小时后</div></div>
      <div class="now__body">
        <span class="now__title">羽毛球双打，缺 1 人</span>
        <div class="now__meta"><img class="now__ico" src="static/icons-dark/clock.png"><span class="now__meta-txt">20:00</span><div class="now__sep"></div><img class="now__ico" src="static/icons-dark/pin.png"><span class="now__meta-txt">体育馆 3 号场</span></div>
        <div class="now__foot">
          <div class="now__people">
            <div class="now__av" style="background:linear-gradient(135deg,#69B9F5,#B9E2FB)">陈</div>
            <div class="now__av" style="background:linear-gradient(135deg,#805CFA,#A98BFF)">周</div>
            <span class="now__count">3/4</span>
          </div>
          <div class="now__join">加入</div>
        </div>
      </div>
    </div>
  </div></div>
</div>

<!-- 动态 -->
<div class="sec">
  <div class="sec__hd"><div class="sec__hd-l"><span class="sec__title">同校动态</span></div><span class="sec__more">进广场</span></div>
  <div class="tabs"><div class="tabs__inner">
    <div class="tabs__item tabs__item--on">全部</div><div class="tabs__item">找搭子</div><div class="tabs__item">求助</div><div class="tabs__item">出闲置</div>
  </div></div>
  <div class="feed">
    <div class="feed__head">
      <div class="feed__av" style="background:linear-gradient(135deg,#805CFA,#A98BFF)">星</div>
      <div class="feed__who">
        <div class="feed__row"><span class="feed__name">阿星</span><div class="feed__id" style="color:#805CFA;background:rgba(128,92,250,.10)">找搭子</div></div>
        <span class="feed__meta">计算机学院 · 大二 · 5 分钟前</span>
      </div>
      <div class="feed__more">···</div>
    </div>
    <div class="feed__main">
      <div class="feed__left">
        <span class="feed__text">有没有人一起去吃新开的烤肉店？AA 制，本周六晚，人多可以拼桌～</span>
        <div class="feed__topics"><span class="feed__topic">#周末探店</span><span class="feed__topic feed__topic--soft">#校园搭子</span></div>
      </div>
      <img class="feed__thumb" src="static/art/art-cheer.jpg">
    </div>
    <div class="feed__acts">
      <div class="feed__act"><img class="feed__act-ico" src="static/icons-dark/heart.png"><span class="feed__act-n">42</span></div>
      <div class="feed__act"><img class="feed__act-ico" src="static/icons-dark/message.png"><span class="feed__act-n">12</span></div>
      <div class="feed__join" style="color:#805CFA;border-color:#805CFA">加入搭子 ›</div>
    </div>
  </div>
</div>

<div class="foot"><div class="foot__end"><div class="foot__line"></div><span class="foot__t">没有更多了</span><div class="foot__line"></div></div></div>

<!-- 活动 -->
<div class="sec">
  <div class="sec__hd"><div class="sec__hd-l"><span class="sec__title">校园活动</span><span class="sec__sub">官方 · 社团</span></div><span class="sec__more">更多</span></div>
  <div class="rail"><div class="rail__inner">
    <div class="act">
      <img class="act__img" src="static/art/art-guitar.jpg">
      <div class="act__mask"></div>
      <div class="act__flag act__flag--sun">即将开始</div>
      <div class="act__info">
        <span class="act__title">校园音乐节 · 夏夜草坪</span>
        <div class="act__meta"><span class="act__meta-txt">周六 19:00</span><div class="act__dot"></div><span class="act__meta-txt">中心草坪</span></div>
        <div class="act__foot"><span class="act__host">校学生会</span><span class="act__join">128 人已报名</span></div>
      </div>
    </div>
  </div></div>
</div>

<!-- 同频 -->
<div class="sec">
  <div class="sec__hd"><div class="sec__hd-l"><span class="sec__title">和你同频</span><span class="sec__sub">兴趣重合度排序</span></div><span class="sec__more">换一批</span></div>
  <div class="rail"><div class="rail__inner">
    <div class="mate">
      <div class="mate__av" style="background:linear-gradient(135deg,#805CFA,#A98BFF)"><span class="mate__ch">苏</span><div class="mate__on"></div></div>
      <span class="mate__name">苏叶</span><span class="mate__college">数媒 · 大二</span>
      <div class="mate__tags"><span class="mate__tag">羽毛球</span><span class="mate__tag">摄影</span></div>
      <div class="mate__hi">打招呼</div>
    </div>
    <div class="mate">
      <div class="mate__av" style="background:linear-gradient(135deg,#29CA83,#93EDCF)"><span class="mate__ch">陈</span><div class="mate__on"></div></div>
      <span class="mate__name">陈一鸣</span><span class="mate__college">机械 · 大三</span>
      <div class="mate__tags"><span class="mate__tag">夜跑</span><span class="mate__tag">吉他</span></div>
      <div class="mate__hi">打招呼</div>
    </div>
  </div></div>
</div>

<!-- 结尾 -->
<div class="end">
  <img class="end__planet" src="static/unida/mascot/u-planet.png">
  <span class="end__t">UNIDA 想更认识你</span>
  <span class="end__d">补完兴趣标签，推荐会准很多</span>
  <div class="end__btn">完善我的兴趣</div>
</div>
</div>
"""

BASE = """
* { margin:0; padding:0; box-sizing:border-box; }
html, body { background:#ddd; overflow-x:hidden; }
.phone {
  width:375px; margin:0; background:#F5F0FF;
  font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;
  padding-bottom:100px; overflow-x:hidden;
}
img { display:block; }
.rail { overflow-x:auto; overflow-y:hidden; }
.rail::-webkit-scrollbar { display:none; }
.hero__trio { animation:none !important; }
.hero__sky, .now__img, .act__img { object-fit: cover; }
.cats__img, .hero__search-ico, .now__ico, .feed__act-ico, .hd__ico, .hd__chev, .end__planet, .task__art { object-fit: contain; }
.hero__trio, .task__art, .feed__thumb { object-fit: cover; }
.feed__thumb { object-position: center; }
.hero--task { margin-top: 12px; }
.task__cta-t { line-height: 30px; }
"""

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<style>{BASE}{CSS}</style></head><body>{BODY}</body></html>"""

open(OUT, "w", encoding="utf-8").write(html)
print("已生成", OUT, len(html), "字符")
for k in ("--c-primary", "--t-main", "--page-x", "--r-md"):
    print("  token", k, "=", tokens.get(k.strip("-"), "缺失"))
