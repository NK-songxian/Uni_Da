# -*- coding: utf-8 -*-
"""消息页设计素材裁切（精简版）：按设计稿实际显示尺寸缩放，控制主包体积。
输出 static/unida/msg/ 下的 webp，统一透明底。"""
from PIL import Image
import os

SRC = "H:/UniDA/PNG/消息"
OUT = "H:/UniDA/unida/static/unida/msg"
os.makedirs(OUT, exist_ok=True)

F_MASCOT_WAVE = "ChatGPT 图像 2026年11月21日 19_22_04.png"
F_MASCOT_STAR = "ChatGPT 图像 2026年11月21日 19_22_38.png"
F_ICONS = "ChatGPT 图像 2026年11月21日 19_22_49.png"
F_LABELS = "ChatGPT 图像 2026年11月21日 19_22_58.png"
F_SCENES = "ChatGPT 图像 2026年11月21日 19_23_08.png"
F_FULL = "UNIDA校园消息中心界面.png"


def trim(im, pad=6):
    bb = im.getbbox()
    if not bb:
        return im
    x1, y1, x2, y2 = bb
    return im.crop((max(0, x1-pad), max(0, y1-pad), min(im.width, x2+pad), min(im.height, y2+pad)))


def save(im, name, max_w, q=76):
    """等比缩放到 max_w 后存 webp"""
    if im.width > max_w:
        h = round(im.height * max_w / im.width)
        im = im.resize((max_w, h), Image.LANCZOS)
    p = os.path.join(OUT, name + ".webp")
    im.save(p, "WEBP", quality=q, method=6)
    print("saved", name.ljust(16), im.size, str(round(os.path.getsize(p)/1024, 1)) + "KB")


def cut(file, box, name, max_w, q=76, pad=8):
    im = Image.open(os.path.join(SRC, file)).convert("RGBA")
    if box:
        im = im.crop(box)
    save(trim(im, pad), name, max_w, q)


# ---------- 吉祥物（设计稿显示 ~180rpx=90px，源图缩到 320px 足够） ----------
cut(F_MASCOT_WAVE, None, "mascot-wave", 320, 74)
cut(F_MASCOT_STAR, None, "mascot-star", 320, 74)

# ---------- 3D 图标：实测网格 x=[68,347][392,723][744,1030][1075,1405] y=[197,491][611,916] ----------
icon_boxes = {
    "ico-search": (68, 197, 347, 491), "ico-chat": (392, 197, 723, 491),
    "ico-calendar": (744, 197, 1030, 491), "ico-megaphone": (1075, 197, 1405, 491),
    "ico-bag": (68, 611, 347, 916), "ico-shield": (392, 611, 723, 916),
    "ico-pin": (744, 611, 1030, 916), "ico-bubble": (1075, 611, 1405, 916),
}
for name, box in icon_boxes.items():
    cut(F_ICONS, box, name, 120, 76)

# ---------- 胶囊标签（保留设计稿自带的图标+文字，直接当图片用） ----------
label_boxes = {
    "badge-3": (81, 66, 307, 311), "badge-12": (369, 66, 596, 311),
    "badge-check": (662, 66, 884, 311), "badge-doing": (934, 66, 1401, 311),
    "tag-chat": (105, 359, 551, 544), "tag-book": (670, 359, 1286, 544),
    "tag-event": (92, 591, 690, 774), "tag-order": (772, 591, 1365, 774),
    "tag-system": (96, 807, 562, 1034), "pin-yellow": (704, 807, 967, 1034),
}
for name, box in label_boxes.items():
    cut(F_LABELS, box, name, 240 if name.startswith("tag-") else 160, 78)

# ---------- 场景插画（设计稿缩略图 ~130rpx，源图缩到 240px） ----------
scene_boxes = {
    "scene-booth": (388, 66, 1073, 546),
    "scene-fitness": (100, 608, 621, 1049),
    "scene-takeout": (870, 608, 1290, 1049),
}
for name, box in scene_boxes.items():
    cut(F_SCENES, box, name, 240, 76)

# ---------- hero 背景：完整稿状态栏下方到搜索框上方 ----------
full = Image.open(os.path.join(SRC, F_FULL)).convert("RGB")
hero = full.crop((0, 52, full.width, 226))
p = os.path.join(OUT, "msg-hero.jpg")
hero.save(p, quality=84)
print("saved msg-hero".ljust(23), hero.size, str(round(os.path.getsize(p)/1024, 1)) + "KB")

total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
print("\n素材总体积:", round(total/1024, 1), "KB")
