# -*- coding: utf-8 -*-
"""消息页素材诊断：alpha 投影分析，输出元素分布供裁切定位"""
from PIL import Image
import numpy as np
import os

D = "H:/UniDA/PNG/消息"
FILES = [
    "ChatGPT 图像 2026年11月21日 19_22_04.png",
    "ChatGPT 图像 2026年11月21日 19_22_38.png",
    "ChatGPT 图像 2026年11月21日 19_22_49.png",
    "ChatGPT 图像 2026年11月21日 19_22_58.png",
    "ChatGPT 图像 2026年11月21日 19_23_08.png",
]


def spans(mask, thresh):
    out, s = [], None
    for i, v in enumerate(mask):
        if v >= thresh and s is None:
            s = i
        if v < thresh and s is not None:
            out.append((s, i))
            s = None
    if s is not None:
        out.append((s, len(mask)))
    return out


for f in FILES:
    im = Image.open(os.path.join(D, f)).convert("RGBA")
    a = np.array(im)[:, :, 3]
    bb = im.getbbox()
    print("\n===", f[-12:], im.size, "bbox", bb)
    rows = (a > 24).sum(axis=1)
    cols = (a > 24).sum(axis=0)
    print("  行分布(>=40px):", spans(rows, 40))
    print("  列分布(>=40px):", spans(cols, 40))
    # 缩略预览（白底）
    th = im.copy()
    th.thumbnail((420, 420))
    bg = Image.new("RGBA", th.size, (245, 240, 255, 255))
    bg.alpha_composite(th)
    out = "H:/UniDA/unida/docs/audit/ref/msg_" + f[-12:-4] + "_thumb.png"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bg.convert("RGB").save(out)
    print("  预览:", out)
