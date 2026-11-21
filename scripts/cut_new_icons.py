# -*- coding: utf-8 -*-
"""
裁切用户 2026-11-21 新增的 unida 3D 图标集
============================================
输出：static/unida/msg/ 下
  ico-book.webp / ico-run.webp / ico-clock.webp / ico-heart.webp
  ico-bell.webp（含角标3版） / ico-bell-plain.webp（去角标版）
素材源：H:/UniDA/PNG/消息/
"""
import os
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = r"H:\UniDA\unida"
SRC = r"H:\UniDA\PNG\消息"
OUT = os.path.join(ROOT, "static", "unida", "msg")
os.makedirs(OUT, exist_ok=True)


def save_crop(im, box, name, target=120, q=78):
    x0, y0, x1, y1 = box
    pad = 8
    crop = im.crop((max(0, x0 - pad), max(0, y0 - pad),
                    min(im.width, x1 + pad), min(im.height, y1 + pad)))
    w, h = crop.size
    scale = target / max(w, h)
    crop = crop.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
    path = os.path.join(OUT, name)
    crop.save(path, "WEBP", quality=q, method=6)
    print(f"  {name}: {crop.size} {os.path.getsize(path)//1024}KB")


# ── 1) 贴纸集 4 枚（透明背景，投影连通域已实测）
sticker = Image.open(os.path.join(SRC, "紫色活力贴纸图标集.png")).convert("RGBA")
BOXES = {
    "ico-book.webp":  (54, 127, 514, 468),
    "ico-run.webp":   (609, 56, 989, 490),
    "ico-clock.webp": (1105, 94, 1480, 500),
    "ico-heart.webp": (564, 606, 989, 949),
}
print("裁切贴纸集：")
for name, box in BOXES.items():
    save_crop(sticker, box, name, target=140)

# ── 2) 铃铛（白底 → 反抠 alpha）
bell = Image.open(os.path.join(SRC, "紫色立体通知铃铛图标.png")).convert("RGBA")
a = np.array(bell)
rgb = a[:, :, :3].astype(int)
# 白底判定：三通道都很亮且接近；主体紫/橙/黄 saturation 高
mx, mn = rgb.max(axis=2), rgb.min(axis=2)
sat = mx - mn
alpha = np.clip((sat - 12) * 12, 0, 255).astype(np.uint8)
# 扩一点边缘抗锯齿
alpha = ndimage.maximum_filter(alpha, size=3)
a[:, :, 3] = alpha
bell_clean = Image.fromarray(a)
# 裁到主体（按新 alpha 投影）
mask = alpha > 60
ys, xs = np.where(mask)
if len(xs):
    box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
    print("铃铛主体 box", box)
    print("裁切铃铛：")
    save_crop(bell_clean, box, "ico-bell.webp", target=140)
