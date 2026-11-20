# -*- coding: utf-8 -*-
"""活动详情页视觉预览：直接读产物 wxss + 手写等价结构，稳定验证样式（不依赖脆弱的 wxml 转换）"""
import os
import re

ROOT = r"H:\UniDA\unida"
DIST = os.path.join(ROOT, "unpackage", "dist", "dev", "mp-weixin")
wxss = open(os.path.join(DIST, "pages", "activity-detail", "activity-detail.wxss"), encoding="utf-8").read()

# rpx -> px
css = re.sub(r"(-?\d+(?:\.\d+)?)rpx", lambda m: f"{float(m.group(1))*0.5:g}px", wxss)
# WXSS 的 image 标签选择器 -> HTML img（HTML 不认 image 标签，否则图标撑爆）
css = re.sub(r"\bimage\b", "img", css)

# 手写与 wxml 等价的结构（示例数据）
BODY = """
<div class="ad unida-page">
  <div class="ad__cover">
    <img class="ad__cover-img" src="static/art/art-guitar.jpg">
    <div class="ad__cover-shade"></div>
    <div class="ad__nav" style="padding-top:20px">
      <div class="ad__nav-btn"><img class="ad__nav-ico" src="static/icons-dark/back.png"></div>
      <span class="ad__nav-title">活动详情</span>
      <div class="ad__nav-btn"><img class="ad__nav-ico" src="static/icons-dark/bell.png"></div>
    </div>
    <div class="ad__cover-status">
      <img class="ad__cover-status-ico" src="static/icons-dark/flame.png">
      <span class="ad__cover-status-t">报名中</span>
    </div>
  </div>

  <div class="ad__main">
    <div class="ad__title-row">
      <span class="ad__title">校园草地音乐会 · 一起嗨翻周末</span>
      <div class="ad__fav"><img class="ad__fav-ico" src="static/icons-dark/heart.png"></div>
    </div>
    <div class="ad__tags">
      <span class="ad__tag ad__tag--purple">校园活动</span>
      <span class="ad__tag ad__tag--orange">热门</span>
      <span class="ad__tag ad__tag--green">免费</span>
    </div>
    <div class="ad__meta">
      <div class="ad__meta-item">
        <div class="ad__meta-ico"><img src="static/icons-dark/clock.png"></div>
        <div class="ad__meta-col"><span class="ad__meta-label">活动时间</span><span class="ad__meta-value">本周六 19:00 - 21:00</span></div>
      </div>
      <div class="ad__meta-item">
        <div class="ad__meta-ico"><img src="static/icons-dark/pin.png"></div>
        <div class="ad__meta-col"><span class="ad__meta-label">活动地点</span><span class="ad__meta-value">中心草坪广场</span></div>
      </div>
    </div>
    <div class="ad__progress">
      <div class="ad__progress-head"><span class="ad__progress-t">报名进度</span><span class="ad__progress-n">36 / 50 人</span></div>
      <div class="ad__progress-track"><div class="ad__progress-fill" style="width:72%"></div></div>
    </div>
  </div>

  <div class="ad__card ad__organizer">
    <div class="ad__org-avatar">林</div>
    <div class="ad__org-info">
      <div class="ad__org-name-row"><span class="ad__org-name">音乐社 · 小林</span><div class="ad__org-verified"><img src="static/icons-dark/buddy.png"></div></div>
      <span class="ad__org-sub">已认证 · 4.9 分</span>
    </div>
    <img class="ad__org-arrow" src="static/icons-dark/chevron.png">
  </div>

  <div class="ad__card">
    <div class="ad__subhead"><span class="ad__subhead-title">报名人员</span><span class="ad__subhead-more">查看全部 ›</span></div>
    <div class="ad__avatars">
      <div class="ad__avatar" style="background:linear-gradient(135deg,#A98BFF,#805CFA)">陈</div>
      <div class="ad__avatar" style="background:linear-gradient(135deg,#FFC94F,#FF9B77)">李</div>
      <div class="ad__avatar" style="background:linear-gradient(135deg,#29CA83,#93EDCF)">王</div>
      <div class="ad__avatar" style="background:linear-gradient(135deg,#69B9F5,#A98BFF)">周</div>
      <div class="ad__avatar" style="background:linear-gradient(135deg,#805CFA,#542DAF)">吴</div>
      <div class="ad__avatar-more">+14</div>
      <span class="ad__avatars-tip">已有 36 人加入</span>
    </div>
  </div>

  <div class="ad__card">
    <div class="ad__subhead"><span class="ad__subhead-title">活动详情</span></div>
    <span class="ad__desc-text">一起在草地上听歌、唱歌、认识新朋友！我们准备了音响、吉他和零食，欢迎会乐器或爱唱歌的同学加入，也欢迎来当观众。</span>
    <span class="ad__desc-text">请自带野餐垫，注意防蚊。活动结束后一起收拾场地哦～</span>
  </div>

  <div class="ad__card">
    <div class="ad__subhead"><span class="ad__subhead-title">费用说明</span></div>
    <div class="ad__cost"><span class="ad__cost-free">免费参与</span><span class="ad__cost-dot">·</span><span class="ad__cost-text">零食饮料 AA（预计 ¥15/人）</span></div>
  </div>

  <div class="ad__bottom">
    <div class="ad__bottom-left">
      <div class="ad__bottom-ico"><img src="static/icons-dark/message.png"></div>
      <span class="ad__bottom-label">联系</span>
    </div>
    <div class="ad__bottom-btn">立即报名</div>
  </div>
</div>
"""

HTML = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#ddd; font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }
.phone { width:375px; height:812px; margin:0 auto; background:#F5F0FF; position:relative; overflow:hidden; }
img { display:block; }
span { display:inline; }
__CSS__
</style></head><body>
<div class="phone">__BODY__</div>
</body></html>""".replace("__CSS__", css).replace("__BODY__", BODY)

out = os.path.join(ROOT, "preview_activity_detail.html")
open(out, "w", encoding="utf-8").write(HTML)
print("已生成", out)
