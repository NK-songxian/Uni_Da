# -*- coding: utf-8 -*-
"""
Tabbar 素材处理  scripts/cut_tabbar_assets.py
===================================================================
1. 从 H:/UniDA/PNG/元素3.png 下排裁出 4 个 3D 立体 tab 图标（首页/发现/消息/我的）
2. Ulogo.png 裁 alpha 边界并压缩为发布键图片
3. 重画波浪底座：左右两段波峰、中间下沉让出发布球（"+"独立于波浪）
输出到 static/unida/tabbar/ 与 static/art/wave-tab-v2.png
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PNG = r"H:\UniDA\PNG"
ROOT = r"H:\UniDA\unida"
OUT_TAB = os.path.join(ROOT, "static", "unida", "tabbar")
os.makedirs(OUT_TAB, exist_ok=True)


def segments_from_alpha(arr_alpha, axis, min_gap=18, min_width=40):
    """沿 axis 方向按 alpha 投影切出连续非空段，返回 [(start,end),...]"""
    proj = arr_alpha.sum(axis=axis)
    nz = np.where(proj > 800)[0]  # 过滤噪点
    if len(nz) == 0:
        return []
    segs, s, prev = [], nz[0], nz[0]
    for v in nz[1:]:
        if v - prev > min_gap:
            if prev - s >= min_width:
                segs.append((int(s), int(prev)))
            s = v
        prev = v
    if prev - s >= min_width:
        segs.append((int(s), int(prev)))
    return segs


def crop_alpha_bbox(im, box):
    region = im.crop(box)
    bbox = region.getchannel("A").getbbox()
    if bbox:
        return region.crop(bbox)
    return region


# ---------- 1. 元素3 下排立体图标 ----------
src = Image.open(os.path.join(PNG, "元素3.png")).convert("RGBA")
arr = np.array(src)
H, W = arr.shape[:2]
print("元素3:", W, "x", H)

# 先按列投影把 5 个图标分段（全高投影即可，上下排 x 对齐）
col_segs = segments_from_alpha(arr[:, :, 3], axis=0, min_gap=30)
print("列分段:", col_segs)

# 下排裁切：手工边界（加号球发光大，均分网格会把它左缘混进指南针）
# 参考列分段: 房(63,272) 指南针+球(335,870) 气(904,1113) 人(1177,1383)；加号球中心=W/2
boxes = {
    "tab-home":     (30, 320),
    "tab-discover": (320, 600),   # 排除加号球左缘
    "tab-message":  (902, 1140),  # 左界避开加号球右缘发光
    "tab-mine":     (1150, 1420),
}
CROP = 208  # 输出画布（留发光边）
LOWER_Y = int(H * 0.42)
for name, (gx0, gx1) in boxes.items():
    sub = arr[LOWER_Y:, gx0:gx1, 3]
    rowsum = sub.sum(axis=1)
    lower = np.where(rowsum > 800)[0]
    if len(lower) == 0:
        print("!! 未找到下排内容:", name)
        continue
    y0 = max(0, int(lower[0]) + LOWER_Y - 14)
    y1 = min(H, int(lower[-1]) + LOWER_Y + 14)
    icon = crop_alpha_bbox(src, (gx0, y0, gx1, y1))
    # 居中放到统一画布
    scale = min((CROP - 24) / icon.width, (CROP - 24) / icon.height, 1.0)
    if scale < 1.0:
        icon = icon.resize((int(icon.width * scale), int(icon.height * scale)), Image.LANCZOS)
    canvas = Image.new("RGBA", (CROP, CROP), (0, 0, 0, 0))
    canvas.paste(icon, ((CROP - icon.width) // 2, (CROP - icon.height) // 2), icon)
    out = os.path.join(OUT_TAB, name + ".png")
    canvas.save(out, optimize=True)
    print("已保存", name, canvas.size, os.path.getsize(out) // 1024, "KB")

# ---------- 2. Ulogo 发布键 ----------
ul = Image.open(os.path.join(PNG, "Ulogo.png")).convert("RGBA")
ul = crop_alpha_bbox(ul, (0, 0, ul.width, ul.height))
ul = ul.resize((240, 240), Image.LANCZOS)
out = os.path.join(OUT_TAB, "publish-logo.png")
ul.save(out, optimize=True)
print("已保存 publish-logo.png", ul.size, os.path.getsize(out) // 1024, "KB")

# ---------- 3. 重画波浪：左右波峰 + 中间下沉（发布球独立） ----------
# 画布 1500x600 = 逻辑 375x150 @4x，与组件里 300rpx 高 scaleToFill 对齐
CW, CH = 1500, 600
pts = [
    (0, 240),
    (340, 150),   # 峰1（首页/发现）
    (660, 360),
    (750, 388),   # 谷底（发布球让位，谷口留出"发布"文字空间）
    (840, 360),
    (1160, 150),  # 峰2（消息/我的）
    (1500, 240),
]
# Catmull-Rom 平滑插值
def catmull_rom(pts, samples=40):
    P = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(len(P) - 3):
        p0, p1, p2, p3 = P[i], P[i + 1], P[i + 2], P[i + 3]
        for t in np.linspace(0, 1, samples, endpoint=False):
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(pts[-1])
    return out

curve = catmull_rom(pts)
wave = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
d = ImageDraw.Draw(wave)
poly = curve + [(CW, CH), (0, CH)]
# 白色主体 + 底部微紫渐变模拟立体
d.polygon(poly, fill=(255, 255, 255, 255))
grad = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
gd = ImageDraw.Draw(grad)
for yy in range(CH):
    # 底部略带紫灰，向上变纯白
    t = max(0.0, (yy - 300) / (CH - 300))
    a = int(28 * t)
    gd.line([(0, yy), (CW, yy)], fill=(228, 218, 248, a))
wave = Image.alpha_composite(wave, grad)
wave.putalpha(wave.getchannel("A"))
# 曲线上缘柔光描边
edge = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
ed = ImageDraw.Draw(edge)
ed.line(curve, fill=(186, 160, 255, 130), width=6, joint="curve")
edge = edge.filter(ImageFilter.GaussianBlur(4))
wave = Image.alpha_composite(wave, edge)
# 白色内高光再压一层，保持柔和
hl = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
hd = ImageDraw.Draw(hl)
hd.line([(x, y + 6) for x, y in curve], fill=(255, 255, 255, 170), width=4, joint="curve")
hl = hl.filter(ImageFilter.GaussianBlur(3))
wave = Image.alpha_composite(wave, hl)

out = os.path.join(ROOT, "static", "art", "wave-tab-v2.png")
wave.save(out, optimize=True)
print("已保存 wave-tab-v2.png", wave.size, os.path.getsize(out) // 1024, "KB")
print("完成")
