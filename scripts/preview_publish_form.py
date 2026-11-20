# -*- coding: utf-8 -*-
"""发布表单页视觉预览"""
import os
import re

ROOT = r"H:\UniDA\unida"
DIST = os.path.join(ROOT, "unpackage", "dist", "dev", "mp-weixin", "pages", "publish-form")
wxss = open(os.path.join(DIST, "publish-form.wxss"), encoding="utf-8").read()
css = re.sub(r"(-?\d+(?:\.\d+)?)rpx", lambda m: f"{float(m.group(1))*0.5:g}px", wxss)
css = re.sub(r"\bimage\b", "img", css)

TYPES = ["学习", "运动", "娱乐", "教学", "跑腿", "其他"]
PLACES = ["图书馆", "中心草坪", "北区驿站", "东门", "体育场"]
FEES = ["免费", "AA", "自定义"]
QUICKS = ["time-now", "time-5m", "time-30m", "time-1h"]

def chips(items, on_idx, key):
    return "".join(
        f'<span class="pf__chip{(" pf__chip--on") if i == on_idx else ""}" data-k="{key}">{t}</span>'
        for i, t in enumerate(items))

def quicks(on_idx):
    return "".join(
        f'<img class="pf__quick-img{(" pf__quick-img--on") if i == on_idx else ""}" src="static/unida/bubbles/{q}.webp">'
        for i, q in enumerate(QUICKS))

BODY = f"""
<div class="pf unida-page">
  <div class="pf__nav">
    <div class="pf__back"><img class="pf__back-img" src="static/icons-dark/back.png"></div>
    <span class="pf__title">发布活动</span><div class="pf__ph"></div>
  </div>
  <div class="pf__banner">
    <div class="pf__banner-txt"><span class="pf__banner-t">完善活动信息</span><span class="pf__banner-s">让更多同频的同学看到你</span></div>
    <img class="pf__banner-img" src="static/unida/bubbles/cal-star-big.webp">
  </div>
  <div class="pf__form">
    <div class="pf__field"><span class="pf__label">活动封面</span>
      <div class="pf__upload"><img class="pf__upload-img" src="static/icons-dark/plus.png"><span class="pf__upload-text">上传图片</span></div>
    </div>
    <div class="pf__field"><span class="pf__label">活动标题 <span class="pf__req">*</span></span>
      <input class="pf__input" placeholder="例如：周末一起看电影" value="周末一起看电影">
      <span class="pf__counter">8/30</span>
    </div>
    <div class="pf__field"><span class="pf__label">活动类型 <span class="pf__req">*</span></span>
      <div class="pf__chips">{chips(TYPES, 0, "type")}</div>
    </div>
    <div class="pf__field"><span class="pf__label">活动描述</span>
      <div class="pf__textarea">介绍活动内容、参与要求…</div>
      <span class="pf__counter">0/200</span>
    </div>
    <div class="pf__field"><span class="pf__label">开始时间 <span class="pf__req">*</span></span>
      <div class="pf__quick">{quicks(0)}</div>
      <div class="pf__pick"><span class="pf__pick-t">现在就开始</span><img class="pf__chev" src="static/icons-dark/chevron.png"></div>
    </div>
    <div class="pf__field"><span class="pf__label">活动地点 <span class="pf__req">*</span></span>
      <div class="pf__chips">{chips(PLACES, 1, "place")}</div>
    </div>
    <div class="pf__field pf__row"><span class="pf__label">参与人数</span>
      <div class="pf__num"><div class="pf__num-btn"><span class="pf__num-sym">−</span></div><span class="pf__num-val">10</span><div class="pf__num-btn"><span class="pf__num-sym">＋</span></div></div>
    </div>
    <div class="pf__field"><span class="pf__label">费用说明</span>
      <div class="pf__chips">{chips(FEES, 0, "fee")}</div>
    </div>
  </div>
  <div class="pf__submit">发布活动</div>
  <div class="pf__bottom-space"></div>
</div>
"""

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#ddd; font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }
.phone { width:375px; margin:0 auto; background:#F5F0FF; }
img { display:block; }
span { display:inline; }
input { border:none; outline:none; }
__CSS__
</style></head><body><div class="phone"><div style="height:40px"></div>__BODY__</div></body></html>"""
HTML = HTML.replace("__CSS__", css).replace("__BODY__", BODY)

out = os.path.join(ROOT, "preview_publish_form.html")
open(out, "w", encoding="utf-8").write(HTML)

from playwright.sync_api import sync_playwright
shot = os.path.join(ROOT, "docs", "audit", "publish_form_preview.png")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    pg = b.new_page(viewport={"width": 375, "height": 900})
    pg.goto("file:///" + out.replace("\\", "/"))
    pg.wait_for_timeout(800)
    pg.evaluate("document.querySelector('.phone').style.height='auto';document.querySelectorAll('.phone *').forEach(e=>{if(getComputedStyle(e).overflow==='hidden')e.style.overflow='visible'})")
    pg.wait_for_timeout(200)
    pg.screenshot(path=shot, full_page=True)
    b.close()
print("已生成", out, "截图", shot)
