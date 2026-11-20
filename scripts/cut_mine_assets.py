# -*- coding: utf-8 -*-
"""裁切「我的」个人中心页素材（个人中心.png 设计稿 + 个人.png hero 卡）"""
from PIL import Image
import os

SRC = r"H:/UniDA/PNG/个人中心.png"
GEREN = r"H:/UniDA/PNG/个人.png"
OUT = r"H:/UniDA/unida/static/unida/mine"
os.makedirs(OUT, exist_ok=True)


def white_to_alpha(im, base=245, slope=4.0):
    """白底转透明：alpha = clamp((base - min(r,g,b)) * slope)"""
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            m = min(r, g, b)
            al = int(max(0, min(255, (base - m) * slope)))
            px[x, y] = (r, g, b, al)
    return im


src = Image.open(SRC).convert("RGB")

jobs = [
    # name, box, to_alpha
    ("header-strip",  (0, 35, 941, 225), False),
    ("life-act",      (98, 548, 182, 630), True),
    ("life-team",     (263, 548, 347, 630), True),
    ("life-fav",      (429, 548, 513, 630), True),
    ("life-pub",      (595, 548, 679, 630), True),
    ("life-sign",     (766, 548, 850, 630), True),
    ("w-clip",        (355, 755, 468, 888), True),
    ("w-mascot",      (758, 752, 888, 908), True),
    ("w-cal",         (345, 945, 470, 1075), True),
    ("w-badge",       (745, 940, 870, 1075), True),
    ("row-pub",       (40, 1109, 115, 1175), True),
    ("row-buddy",     (40, 1167, 115, 1233), True),
    ("row-fav",       (40, 1225, 115, 1291), True),
    ("row-order",     (40, 1283, 115, 1349), True),
    ("row-set",       (40, 1355, 115, 1421), True),
    ("row-help",      (40, 1410, 115, 1476), True),
]

for name, box, alpha in jobs:
    im = src.crop(box)
    if alpha:
        im = white_to_alpha(im)
        # bbox 收紧
        bbox = im.getbbox()
        if bbox:
            im = im.crop(bbox)
    im.save(os.path.join(OUT, name + ".png"))
    print(name, im.size, os.path.getsize(os.path.join(OUT, name + ".png")) // 1024, "KB")

# hero 卡（个人.png 主体，保留原透明边）
g = Image.open(GEREN).convert("RGBA")
hero = g.crop((54, 238, 1392, 847))
hero.save(os.path.join(OUT, "hero-card.png"))
print("hero-card", hero.size, os.path.getsize(os.path.join(OUT, "hero-card.png")) // 1024, "KB")
