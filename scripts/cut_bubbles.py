# -*- coding: utf-8 -*-
"""气泡/标签素材通用裁切器：投影找行→行内找列→逐元素切出→拼图目检"""
from PIL import Image, ImageDraw
import numpy as np
import os

SRC = "H:/UniDA/PNG"
STAGE = "H:/UniDA/unida/docs/audit/ref/bubbles_stage"


def cut_all(name, min_h=25, min_w=30):
    im = Image.open(os.path.join(SRC, name)).convert("RGBA")
    a = np.array(im)[:, :, 3]
    os.makedirs(STAGE, exist_ok=True)
    rows = (a > 20).sum(axis=1)
    sp = []
    s = None
    for i, v in enumerate(rows > 8):
        if v and s is None:
            s = i
        if not v and s is not None:
            if i - s >= min_h:
                sp.append((s, i))
            s = None
    if s is not None and len(rows) - s >= min_h:
        sp.append((s, len(rows)))
    idx = 0
    cells = []
    for y1, y2 in sp:
        cols = (a[y1:y2] > 20).sum(axis=0)
        csp = []
        s = None
        for i, v in enumerate(cols > 4):
            if v and s is None:
                s = i
            if not v and s is not None:
                if i - s >= min_w:
                    csp.append((s, i))
                s = None
        if s is not None and len(cols) - s >= min_w:
            csp.append((s, len(cols)))
        for x1, x2 in csp:
            cell = im.crop((x1, y1, x2, y2))
            bb = cell.getbbox()
            if bb:
                cell = cell.crop(bb)
            fn = f"{name[:-4]}_r{y1}_c{x1}.png"
            cell.save(os.path.join(STAGE, fn))
            cells.append((fn, cell))
            idx += 1
    # 拼目检图
    W = 1000
    x = y = 8
    rh = 0
    sheet = Image.new("RGBA", (W, 1200), (244, 240, 252, 255))
    d = ImageDraw.Draw(sheet)
    for fn, cell in cells:
        im2 = cell.copy()
        im2.thumbnail((150, 90))
        if x + im2.width > W - 8:
            x = 8
            y += rh + 30
            rh = 0
        sheet.alpha_composite(im2, (x, y))
        d.text((x, y + im2.height + 2), fn.replace(".png", "")[-22:], fill=(120, 0, 0))
        x += im2.width + 8
        rh = max(rh, im2.height)
    sheet = sheet.crop((0, 0, W, min(1200, y + rh + 40)))
    out = os.path.join(STAGE, f"sheet_{name[:-4]}.jpg")
    sheet.convert("RGB").save(out, quality=88)
    print(name, "共", idx, "个元素 ->", out)


if __name__ == "__main__":
    cut_all("气泡1.png")
    cut_all("气泡3.png")
    cut_all("气泡4.png")
