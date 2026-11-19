# -*- coding: utf-8 -*-
"""UNIDA 线性图标生成器：统一白色线性图标，透明底，用于彩色渐变块上。
运行：E:/anaco/envs/sam_gpu/python.exe gen_icons.py
"""
from PIL import Image, ImageDraw
import os

S = 128
SS = 4
SZ = S * SS
OUT = os.path.join(os.path.dirname(__file__), '..', 'static', 'icons')
os.makedirs(OUT, exist_ok=True)

W = int(9 * SS)  # 统一线宽


def P(*pts):
    return [(int(x * SS), int(y * SS)) for x, y in pts]


def new():
    im = Image.new('RGBA', (SZ, SZ), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def save(im, name):
    im.resize((S, S), Image.LANCZOS).save(os.path.join(OUT, name + '.png'))


def line(d, pts, fill=(255, 255, 255, 255), w=W):
    d.line(P(*pts), fill=fill, width=w, joint='curve')


def poly(d, pts, fill=None, outline=(255, 255, 255, 255), w=W):
    d.polygon(P(*pts), fill=fill)
    if outline:
        d.line(P(*pts, pts[0]), fill=outline, width=w, joint='curve')


def ell(d, box, outline=(255, 255, 255, 255), w=W, fill=None):
    d.ellipse([int(v * SS) for v in box], outline=outline, width=w, fill=fill)


def arc(d, box, a0, a1, outline=(255, 255, 255, 255), w=W):
    d.arc([int(v * SS) for v in box], a0, a1, fill=outline, width=w)


def rrect(d, box, r, outline=(255, 255, 255, 255), w=W, fill=None):
    d.rounded_rectangle([int(v * SS) for v in box], radius=int(r * SS), outline=outline, width=w, fill=fill)


def dot(d, cx, cy, r):
    ell(d, (cx - r, cy - r, cx + r, cy + r), outline=None, fill=(255, 255, 255, 255))


# ---------- 底部导航 ----------
def home():
    im, d = new()
    line(d, [(18, 62), (64, 24), (110, 62)])
    line(d, [(30, 54), (30, 108), (98, 108), (98, 54)])
    line(d, [(54, 108), (54, 76), (74, 76), (74, 108)])
    save(im, 'home')


def compass():
    im, d = new()
    ell(d, (16, 16, 112, 112))
    poly(d, [(50, 78), (60, 60), (78, 50), (68, 68)], fill=(255, 255, 255, 255), outline=None)
    dot(d, 64, 64, 4)
    save(im, 'compass')


def message():
    im, d = new()
    rrect(d, (16, 24, 112, 92), 26)
    poly(d, [(36, 88), (30, 110), (58, 92)], fill=(255, 255, 255, 255), outline=None)
    dot(d, 46, 58, 5)
    dot(d, 64, 58, 5)
    dot(d, 82, 58, 5)
    save(im, 'message')


def user():
    im, d = new()
    ell(d, (44, 22, 84, 62))
    arc(d, (26, 62, 102, 138), 180, 360)
    save(im, 'user')


# ---------- 顶部 ----------
def search():
    im, d = new()
    ell(d, (20, 20, 86, 86))
    line(d, [(80, 80), (112, 112)])
    save(im, 'search')


def bell():
    im, d = new()
    arc(d, (28, 24, 100, 100), 180, 360)
    line(d, [(28, 62), (28, 84), (100, 84), (100, 62)])
    line(d, [(46, 96), (48, 108), (80, 108), (82, 96)])
    save(im, 'bell')


def pin():
    im, d = new()
    ell(d, (40, 18, 88, 66))
    line(d, [(42, 54), (64, 112), (86, 54)])
    ell(d, (54, 32, 74, 52), outline=None, fill=(255, 255, 255, 255))
    save(im, 'pin')


# ---------- 六/八分类 ----------
def buddy():
    im, d = new()
    ell(d, (30, 22, 62, 54))
    ell(d, (66, 22, 98, 54))
    arc(d, (16, 56, 72, 112), 180, 360)
    arc(d, (56, 56, 112, 112), 180, 360)
    save(im, 'buddy')


def calendar():
    im, d = new()
    rrect(d, (20, 30, 108, 110), 16)
    line(d, [(20, 54), (108, 54)])
    line(d, [(42, 18), (42, 40)])
    line(d, [(86, 18), (86, 40)])
    dot(d, 44, 76, 5)
    dot(d, 64, 76, 5)
    save(im, 'calendar')


def racket():
    im, d = new()
    ell(d, (20, 16, 96, 92))
    line(d, [(56, 90), (78, 116)])
    line(d, [(58, 24), (58, 86)])
    line(d, [(78, 24), (78, 86)])
    line(d, [(26, 54), (90, 54)])
    line(d, [(30, 36), (86, 36)])
    line(d, [(30, 72), (86, 72)])
    save(im, 'racket')


def book():
    im, d = new()
    line(d, [(64, 30), (64, 108)])
    line(d, [(64, 34), (26, 28), (26, 98), (64, 106)])
    line(d, [(64, 34), (102, 28), (102, 98), (64, 106)])
    save(im, 'book')


def bulb():
    im, d = new()
    arc(d, (34, 20, 94, 82), 180, 360)
    line(d, [(34, 52), (34, 60), (94, 60), (94, 52)])
    line(d, [(48, 82), (48, 94), (80, 94), (80, 82)])
    line(d, [(52, 104), (76, 104)])
    save(im, 'bulb')


def box():
    im, d = new()
    poly(d, [(22, 46), (64, 26), (106, 46), (64, 66)], fill=None)
    line(d, [(22, 46), (22, 100), (64, 122), (64, 66)])
    line(d, [(106, 46), (106, 100), (64, 122)])
    save(im, 'box')


def music():
    im, d = new()
    ell(d, (26, 78, 58, 106), outline=None, fill=(255, 255, 255, 255))
    ell(d, (66, 66, 98, 94), outline=None, fill=(255, 255, 255, 255))
    line(d, [(54, 92), (54, 26), (94, 16), (94, 70)])
    save(im, 'music')


def grid():
    im, d = new()
    for cx in (40, 88):
        for cy in (40, 88):
            rrect(d, (cx - 14, cy - 14, cx + 14, cy + 14), 8, outline=None, fill=(255, 255, 255, 255))
    save(im, 'grid')


# ---------- 辅助 ----------
def clock():
    im, d = new()
    ell(d, (16, 16, 112, 112))
    line(d, [(64, 34), (64, 66), (88, 78)])
    save(im, 'clock')


def flame():
    im, d = new()
    d.polygon(P((64, 14), (86, 48), (80, 62), (98, 56), (100, 88), (64, 116), (28, 88), (34, 54), (50, 62), (44, 44)),
              outline=(255, 255, 255, 255), width=W)
    save(im, 'flame')


def chevron():
    im, d = new()
    line(d, [(44, 30), (86, 64), (44, 98)])
    save(im, 'chevron')


def plus():
    im, d = new()
    line(d, [(64, 26), (64, 102)])
    line(d, [(26, 64), (102, 64)])
    save(im, 'plus')


def back():
    im, d = new()
    line(d, [(78, 24), (40, 64), (78, 104)])
    save(im, 'back')


for fn in (home, compass, message, user, search, bell, pin, buddy, calendar,
           racket, book, bulb, box, music, grid, clock, flame, chevron, plus, back):
    fn()

print('icons generated:', len([f for f in os.listdir(OUT) if f.endswith('.png')]), '->', OUT)
