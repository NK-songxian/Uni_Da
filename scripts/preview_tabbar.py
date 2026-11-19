# -*- coding: utf-8 -*-
"""Tabbar 视觉预览：按编译产物 wxss 还原 375px 宽效果"""
import re, os

ROOT = r"H:\UniDA\unida"
wxss = open(os.path.join(ROOT, "unpackage", "dist", "dev", "mp-weixin", "components", "unida-tabbar", "unida-tabbar.wxss"), encoding="utf-8").read()

def px(v):
    return re.sub(r"(-?\d+(?:\.\d+)?)rpx", lambda m: f"{float(m.group(1))*0.5:g}px", v)

# 简单替换 rpx → px（wxss 无 scss 嵌套，已是纯 CSS）
css = px(wxss)
# fixed 改 absolute 便于预览
css = css.replace("position: fixed", "position: absolute")

HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:#ddd; font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }}
.phone {{ width:375px; height:760px; margin:20px auto; background:#F5F0FF; position:relative; overflow:hidden; border-radius:24px; }}
img {{ display:block; }}
/* 模拟页面底部内容，检验谷区透出效果 */
.fake {{ position:absolute; left:20px; right:20px; top:560px; height:120px; background:#fff; border-radius:14px; padding:12px; color:#2A2440; font-size:14px; }}
{css}
</style></head><body>
<div class="phone">
  <div class="fake">模拟页面卡片内容——检查它透过波浪谷区是否可辨、发布文字是否可读</div>
  <view class="unida-tabbar" style="width:375px">
    <view class="wave-solid"></view>
    <img class="wave-bg" src="static/art/wave-tab-v2.png" style="object-fit:fill">
    <view class="tabbar-content">
      <view class="tab-item active" style="pointer-events:none">
        <view class="icon-wrap"><img class="tab-ico" src="static/unida/tabbar/tab-home.png" style="object-fit:contain"></view>
        <text class="tab-text">首页</text><view class="active-line"></view>
      </view>
      <view class="tab-item" style="pointer-events:none">
        <view class="icon-wrap"><img class="tab-ico" src="static/unida/tabbar/tab-discover.png" style="object-fit:contain"></view>
        <text class="tab-text">发现</text>
      </view>
      <view class="tab-item publish-space"></view>
      <view class="tab-item" style="pointer-events:none">
        <view class="icon-wrap message-wrap"><img class="tab-ico" src="static/unida/tabbar/tab-message.png" style="object-fit:contain"><view class="message-badge">3</view></view>
        <text class="tab-text">消息</text>
      </view>
      <view class="tab-item" style="pointer-events:none">
        <view class="icon-wrap"><img class="tab-ico" src="static/unida/tabbar/tab-mine.png" style="object-fit:contain"></view>
        <text class="tab-text">我的</text>
      </view>
    </view>
    <view class="publish-center" style="pointer-events:none">
      <view class="publish-glow"></view>
      <img class="publish-logo" src="static/unida/tabbar/publish-logo.png" style="object-fit:contain">
      <text class="publish-text">发布</text>
    </view>
  </view>
</div>
</body></html>"""
out = os.path.join(ROOT, "preview_tabbar.html")
open(out, "w", encoding="utf-8").write(HTML)
print("已生成", out)
