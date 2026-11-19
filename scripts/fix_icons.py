# -*- coding: utf-8 -*-
"""
重切 6 个 3D 类目图标  fix_icons.py
--------------------------------------------------
解决两个问题：
1. 原图元素1 上有一层半透明白色发光，直接裁切会带出一块浅灰方形底
2. 各元素原始占比不同，放进同一尺寸容器里视觉大小不一致

做法：
- 把 alpha < 阈值 的柔光直接清零（方形底消失），剩余 alpha 重新铺满 0~255
- 按内容裁紧，再补成正方形，四周留统一边距 → 六个图标视觉大小一致
"""
import os

import numpy as np
from PIL import Image

SRC = r"H:\UniDA\PNG\元素1.png"
LIB = r"H:\UniDA\unida\assets\unida\illustrations"
PUB = r"H:\UniDA\unida\static\unida\illustrations"

BOXES = [
    ("icon-study.png",  (91, 227, 345, 475)),
    ("icon-run.png",    (415, 230, 679, 471)),
    ("icon-horn.png",   (756, 226, 983, 466)),
    ("icon-gift.png",   (1079, 235, 1380, 460)),
    ("icon-team.png",   (138, 615, 456, 888)),
    ("icon-planet.png", (561, 596, 883, 882)),
]

ALPHA_CUT = 46      # 低于这个 alpha 的柔光清零
PAD_RATIO = 0.04    # 正方形画布四周留白比例


def clean(crop):
    a = np.array(crop).astype(np.float32)
    alpha = a[..., 3]
    out = alpha.copy()
    out[alpha < ALPHA_CUT] = 0
    # 把剩余部分线性拉回 0~255，避免整体发虚
    m = out > 0
    out[m] = np.clip((out[m] - ALPHA_CUT) / (255.0 - ALPHA_CUT) * 255.0, 0, 255)
    a[..., 3] = out
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def trim(im, thr=10):
    arr = np.array(im.getchannel("A"))
    ys, xs = np.where(arr > thr)
    if len(xs) == 0:
        return im
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def square(im, size, pad=PAD_RATIO):
    w, h = im.size
    side = max(w, h)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(im, ((side - w) // 2, (side - h) // 2), im)
    inner = int(size * (1 - pad * 2))
    canvas = canvas.resize((inner, inner), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(canvas, ((size - inner) // 2, (size - inner) // 2), canvas)
    return out


def main():
    sheet = Image.open(SRC).convert("RGBA")
    for name, box in BOXES:
        c = clean(sheet.crop(box))
        c = trim(c)
        big = square(c, 240)
        small = square(c, 152)
        big.save(os.path.join(LIB, name), "PNG", optimize=True)
        small.save(os.path.join(PUB, name), "PNG", optimize=True)
        print(f"{name:20s} 库 {big.size} {os.path.getsize(os.path.join(LIB,name))//1024:3d}KB   "
              f"发布 {small.size} {os.path.getsize(os.path.join(PUB,name))//1024:3d}KB")


if __name__ == "__main__":
    main()
