# -*- coding: utf-8 -*-
"""我的报名页视觉预览：读产物 wxss + 手写等价结构"""
import os
import re

ROOT = r"H:\UniDA\unida"
DIST = os.path.join(ROOT, "unpackage", "dist", "dev", "mp-weixin", "pages", "my-orders")
wxss = open(os.path.join(DIST, "my-orders.wxss"), encoding="utf-8").read()
css = re.sub(r"(-?\d+(?:\.\d+)?)rpx", lambda m: f"{float(m.group(1))*0.5:g}px", wxss)
css = re.sub(r"\bimage\b", "img", css)

ORDER = """
<div class="mo__order">
  <div class="mo__order-head">
    <div class="mo__order-type"><img class="mo__type-ico" src="static/icons-dark/__ICO__"><span class="mo__type-t">__TYPE__</span></div>
    <div class="mo__status mo__status--__SK__"><div class="mo__status-dot"></div><span class="mo__status-t">__ST__</span></div>
  </div>
  <span class="mo__order-title">__TITLE__</span>
  <div class="mo__order-meta">
    <img class="mo__meta-ico" src="static/icons-dark/clock.png"><span class="mo__meta-t">__TIME__</span>
    <img class="mo__meta-ico mo__meta-ico--pin" src="static/icons-dark/pin.png"><span class="mo__meta-t">__PLACE__</span>
  </div>
  <div class="mo__order-foot">
    <span class="mo__order-price __PRICECLS__">__PRICE__</span>
    <div class="mo__order-actions"><span class="mo__order-btn __BTNCLS__">__BTN__</span></div>
  </div>
</div>
"""

def order(ico, typ, sk, st, title, time, place, price, pricecls, btn, btncls):
    return (ORDER.replace("__ICO__", ico).replace("__TYPE__", typ).replace("__SK__", sk)
            .replace("__ST__", st).replace("__TITLE__", title).replace("__TIME__", time)
            .replace("__PLACE__", place).replace("__PRICE__", price).replace("__PRICECLS__", pricecls)
            .replace("__BTN__", btn).replace("__BTNCLS__", btncls))

CARDS = (
    order("box.png", "跑腿服务", "wait", "待接单", "帮忙取快递（中通北区驿站）", "今天 18:00 前", "北区驿站", "¥8", "", "确认完成", "")
    + order("music.png", "校园活动", "ongoing", "进行中", "校园草地音乐会", "本周六 19:00", "中心草坪广场", "免费", "mo__order-price--free", "查看进度", "mo__order-btn--ghost")
    + order("box.png", "跑腿服务", "done", "已完成", "代拿外卖到宿舍楼下", "昨天", "东门", "¥5", "", "去评价", "")
)

BODY = """
<div class="mo unida-page">
  <div class="mo__nav" style="padding-top:20px">
    <div class="mo__nav-btn"><img class="mo__nav-ico" src="static/icons-dark/back.png"></div>
    <span class="mo__nav-title">我的报名</span>
    <div class="mo__nav-btn"></div>
  </div>
  <div class="mo__hero">
    <img class="mo__hero-img" src="static/unida/planet/planet-cal.png">
    <div class="mo__hero-info">
      <span class="mo__hero-title">我的报名</span>
      <div class="mo__hero-stats">
        <div class="mo__stat"><span class="mo__stat-n">3</span><span class="mo__stat-k">全部</span></div>
        <div class="mo__stat-divider"></div>
        <div class="mo__stat"><span class="mo__stat-n">1</span><span class="mo__stat-k">进行中</span></div>
        <div class="mo__stat-divider"></div>
        <div class="mo__stat"><span class="mo__stat-n">1</span><span class="mo__stat-k">已完成</span></div>
      </div>
    </div>
  </div>
  <div class="mo__tabs">
    <div class="mo__tab mo__tab--on"><span class="mo__tab-t">全部</span></div>
    <div class="mo__tab"><span class="mo__tab-t">待进行</span></div>
    <div class="mo__tab"><span class="mo__tab-t">进行中</span></div>
    <div class="mo__tab"><span class="mo__tab-t">已完成</span></div>
  </div>
  <div class="mo__list">__CARDS__
    <div class="mo__empty">
      <img class="mo__empty-img" src="static/unida/planet/planet-bubble.png">
      <span class="mo__empty-t">这里还空空的</span>
      <span class="mo__empty-sub">去发现页搭个伴吧</span>
    </div>
  </div>
</div>
""".replace("__CARDS__", CARDS)

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

out = os.path.join(ROOT, "preview_my_orders.html")
open(out, "w", encoding="utf-8").write(HTML)
print("已生成", out)
