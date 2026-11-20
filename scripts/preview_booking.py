# -*- coding: utf-8 -*-
"""报名链路两页视觉预览：读产物 wxss + 手写等价结构"""
import os
import re

ROOT = r"H:\UniDA\unida"
DIST = os.path.join(ROOT, "unpackage", "dist", "dev", "mp-weixin", "pages")


def load(page):
    css = open(os.path.join(DIST, page, page + ".wxss"), encoding="utf-8").read()
    css = re.sub(r"(-?\d+(?:\.\d+)?)rpx", lambda m: f"{float(m.group(1))*0.5:g}px", css)
    css = re.sub(r"\bimage\b", "img", css)
    return css


WRAP = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#ddd; font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }
.phone { width:375px; height:812px; margin:0 auto; background:#F5F0FF; position:relative; overflow:hidden; }
img { display:block; }
span { display:inline; }
textarea { border:none; outline:none; font-family:inherit; resize:none; }
__CSS__
</style></head><body><div class="phone">__BODY__</div></body></html>"""

CONFIRM = """
<div class="bc unida-page">
  <div class="bc__nav" style="padding-top:20px">
    <div class="bc__nav-btn"><img class="bc__nav-ico" src="static/icons-dark/back.png"></div>
    <span class="bc__nav-title">报名确认</span>
    <div class="bc__nav-btn"></div>
  </div>
  <div class="bc__act">
    <img class="bc__act-cover" src="static/art/art-guitar.jpg">
    <div class="bc__act-body">
      <span class="bc__act-title">校园草地音乐会 · 一起嗨翻周末</span>
      <div class="bc__act-meta"><img class="bc__act-ico" src="static/icons-dark/clock.png"><span class="bc__act-t">本周六 19:00 - 21:00</span></div>
      <div class="bc__act-meta"><img class="bc__act-ico" src="static/icons-dark/pin.png"><span class="bc__act-t">中心草坪广场</span></div>
    </div>
  </div>
  <div class="bc__card">
    <div class="bc__sec-title">预约信息</div>
    <div class="bc__row"><span class="bc__row-k">预约时间</span><span class="bc__row-v">本周六 19:00</span></div>
    <div class="bc__row">
      <span class="bc__row-k">参与人数</span>
      <div class="bc__stepper">
        <div class="bc__step"><div class="bc__step-bar"></div></div>
        <span class="bc__step-num">1</span>
        <div class="bc__step"><img class="bc__step-plus" src="static/icons-dark/plus.png"></div>
      </div>
    </div>
    <div class="bc__row"><span class="bc__row-k">联系电话</span><span class="bc__row-v">138****8888</span></div>
  </div>
  <div class="bc__card">
    <div class="bc__sec-title">参与备注<span class="bc__opt">（选填）</span></div>
    <textarea class="bc__ta" placeholder="想对发起人说什么？例如：我会弹吉他～"></textarea>
    <span class="bc__count">0/100</span>
  </div>
  <div class="bc__notice">
    <img class="bc__notice-ico" src="static/icons-dark/bulb.png">
    <span class="bc__notice-t">本活动免费，现场零食饮料 AA 自愿参与。请准时到场，如需取消请提前 2 小时操作。</span>
  </div>
  <div class="bc__bottom">
    <div class="bc__agree">
      <div class="bc__cb bc__cb--on"><div class="bc__cb-tick"></div></div>
      <span class="bc__agree-t">我已阅读并同意活动参与须知</span>
    </div>
    <div class="bc__submit"><span class="bc__submit-t">提交报名</span></div>
  </div>
</div>
"""

SUCCESS = """
<div class="bs unida-page">
  <div class="bs__hero" style="padding-top:80px">
    <img class="bs__sp bs__sp--1" src="static/unida/illustrations/deco-sparkle-1.png">
    <img class="bs__sp bs__sp--2" src="static/unida/illustrations/deco-sparkle-2.png">
    <img class="bs__sp bs__sp--3" src="static/unida/illustrations/deco-sparkle-1.png">
    <div class="bs__planet"><img class="bs__planet-img" src="static/unida/mascot/u-planet.png"></div>
    <span class="bs__title">报名成功</span>
    <span class="bs__sub">已加入这场校园活动，期待与你相遇</span>
  </div>
  <div class="bs__card">
    <div class="bs__card-head">
      <span class="bs__card-title">报名信息</span>
      <div class="bs__badge"><div class="bs__badge-dot"></div><span class="bs__badge-t">已报名</span></div>
    </div>
    <div class="bs__row"><span class="bs__row-k">活动名称</span><span class="bs__row-v">校园草地音乐会</span></div>
    <div class="bs__row"><span class="bs__row-k">活动时间</span><span class="bs__row-v">本周六 19:00</span></div>
    <div class="bs__row"><span class="bs__row-k">活动地点</span><span class="bs__row-v">中心草坪广场</span></div>
    <div class="bs__row"><span class="bs__row-k">报名编号</span><span class="bs__row-code">UNI 2026 1120 193</span></div>
  </div>
  <div class="bs__qr-card">
    <div class="bs__qr-head">
      <div class="bs__qr-title-row"><img class="bs__qr-ico" src="static/icons-dark/calendar.png"><span class="bs__qr-title">现场签到码</span></div>
      <span class="bs__qr-hint">活动开始前 30 分钟生效</span>
    </div>
    <div class="bs__qr-box"><img class="bs__qr-img" src="static/unida/qr/booking-qr.png"></div>
    <span class="bs__qr-tip">到场后向发起人出示此码完成签到</span>
  </div>
  <div class="bs__notice"><img class="bs__notice-ico" src="static/icons-dark/bell.png"><span class="bs__notice-t">活动开始前会收到提醒。如需取消，请在我的报名中提前操作。</span></div>
  <div class="bs__actions">
    <div class="bs__btn bs__btn--primary"><span class="bs__btn-t">查看我的报名</span></div>
    <div class="bs__btn bs__btn--ghost"><span class="bs__btn-t2">返回首页</span></div>
  </div>
</div>
"""

for page, body in [("booking-confirm", CONFIRM), ("booking-success", SUCCESS)]:
    html = WRAP.replace("__CSS__", load(page)).replace("__BODY__", body)
    out = os.path.join(ROOT, "preview_%s.html" % page.replace("-", "_"))
    open(out, "w", encoding="utf-8").write(html)
    print("已生成", out)
