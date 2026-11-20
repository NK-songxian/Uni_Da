# -*- coding: utf-8 -*-
"""从元素4 裁切 U 星球各状态（my-orders 页用）+ 连通域清理发光残影"""
import os
import numpy as np
from PIL import Image
from scipy import ndimage

SRC = r"H:\UniDA\PNG\元素4.png"
OUT = r"H:\UniDA\unida\static\unida\planet"

# (名称, x0, y0, x1, y1) 精细网格边界（含光晕星星，不碰邻）
BOXES = [
    ("planet-run",     81,  45, 483, 385),   # 奔跑（进行中）
    ("planet-bell",   524,  35, 880, 372),   # 响铃（待进行/提醒）
    ("planet-cheer",  995,  35, 1352, 352),  # 欢呼（已完成）
    ("planet-bubble", 524, 393, 1348, 1018), # 大星球+气泡+加号（空态主视觉）
    ("planet-cal",     81, 688, 483, 1058),  # 日历打勾（报名/签到）
    ("planet-glow",    81, 414, 483, 668),   # 光芒（发现/推荐）
]
TARGET = 260  # 输出方形边长


def clean_alpha(arr):
    """保留最大连通域，清掉分离的发光残影碎片"""
    alpha = arr[:, :, 3] > 8
    lab, cnt = ndimage.label(alpha)
    if cnt <= 1:
        return arr
    sizes = ndimage.sum(alpha, lab, range(1, cnt + 1))
    keep = int(np.argmax(sizes)) + 1
    # 残影碎片通常是主体 1/8 以下
    mask = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= sizes[keep - 1] / 8 or i + 1 == keep])
    arr = arr.copy()
    arr[:, :, 3] = np.where(mask, arr[:, :, 3], 0)
    return arr


def main():
    os.makedirs(OUT, exist_ok=True)
    im = Image.open(SRC).convert("RGBA")
    for name, x0, y0, x1, y1 in BOXES:
        crop = im.crop((x0, y0, x1, y1))
        arr = np.asarray(crop).copy()
        arr = clean_alpha(arr)
        crop = Image.fromarray(arr)
        # alpha bbox 收紧
        bbox = crop.getbbox()
        if bbox:
            crop = crop.crop(bbox)
        # 等比缩放进 TARGET 方形（保留 aspect，贴边）
        w, h = crop.size
        scale = TARGET / max(w, h)
        crop = crop.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
        # 铺到方形画布居中
        canvas = Image.new("RGBA", (TARGET, TARGET), (0, 0, 0, 0))
        canvas.alpha_composite(crop, ((TARGET - crop.width) // 2, (TARGET - crop.height) // 2))
        path = os.path.join(OUT, name + ".png")
        canvas.save(path)
        print(name, canvas.size, round(os.path.getsize(path) / 1024, 1), "KB")


if __name__ == "__main__":
    main()
