# -*- coding: utf-8 -*-
"""
UNIDA 素材构建脚本  build_assets.py
===================================================================
输入：H:\\UniDA\\PNG            —— 原始设计稿（AI 出图/手绘稿，体积极大，永不进包）
      中间：assets/unida/**     —— 素材库（完整尺寸，可反复复用，不进包）
输出：static/unida/**           —— 发布版（按真实显示尺寸压缩，进小程序包）

为什么分两层：
微信小程序主包上限 2MB，全部原图塞进 static 会直接上传失败。
所以「库」和「发布」必须分开，只有当前页面真正用到的文件才进 static。

处理三件事：
1. 去彩边 defringe —— AI 出图的洋红/蓝紫描边光晕，小尺寸下会变成脏边
2. 裁白边 + 缩放 —— 按最大显示尺寸 ×2 降采样
3. 格式选择      —— 有透明通道用 WebP（PNG 的 17%），不透明用 JPEG

运行：E:/anaco/envs/sam_gpu/python.exe scripts/build_assets.py
"""
import json
import os

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

SRC = r"H:\UniDA\PNG"
ROOT = r"H:\UniDA\unida"
LIB = os.path.join(ROOT, "assets", "unida")     # 素材库
PUB = os.path.join(ROOT, "static", "unida")     # 发布目录


# ----------------------------------------------------------------- 图像工具
def load(path):
    return Image.open(path).convert("RGBA")


def defringe(im, erode=2, tint=0.65):
    """去掉透明边缘的彩色光晕。

    两步：
    - 颜色去污：用内部实色向外扩散的颜色替换半透明边缘的 RGB，洋红描边不再显形；
    - alpha 侵蚀：削掉最外 1~3px 软边，再轻微羽化保持柔和。
    """
    arr = np.array(im).astype(np.float32)
    rgb, a = arr[..., :3], arr[..., 3]

    core = (a > 205).astype(np.float32)
    k = 9
    core_blur = ndimage.uniform_filter(core, k)
    rgb_blur = np.stack(
        [ndimage.uniform_filter(rgb[..., i] * core, k) for i in range(3)], -1
    )
    bled = rgb_blur / np.maximum(core_blur, 1e-3)[..., None]
    has_core = core_blur > 0.02

    edge = (a < 250) & (a > 0) & has_core
    w = (tint * (1.0 - a / 250.0))[..., None]
    rgb_new = np.where(edge[..., None], rgb * (1 - w) + bled * w, rgb)

    alpha = Image.fromarray(a.astype(np.uint8), "L")
    if erode > 0:
        alpha = alpha.filter(ImageFilter.MinFilter(erode * 2 + 1))
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.7))

    out = np.dstack([np.clip(rgb_new, 0, 255), np.array(alpha)]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def trim(im, pad=4, athr=8):
    a = np.array(im.getchannel("A"))
    ys, xs = np.where(a > athr)
    if len(xs) == 0:
        return im
    return im.crop((
        max(xs.min() - pad, 0), max(ys.min() - pad, 0),
        min(xs.max() + pad + 1, im.width), min(ys.max() + pad + 1, im.height),
    ))


def fit(im, max_w=None, max_h=None):
    w, h = im.size
    s = 1.0
    if max_w and w > max_w:
        s = min(s, max_w / w)
    if max_h and h > max_h:
        s = min(s, max_h / h)
    if s >= 1:
        return im
    return im.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)


def _save(im, path, fmt, quality):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if fmt == "png":
        im.save(path, "PNG", optimize=True)
    elif fmt == "webp":
        im.save(path, "WEBP", quality=quality, method=6)
    else:  # jpg
        im.convert("RGB").save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    return os.path.getsize(path)


def emit(im, rel, lib_w, pub_w, fmt, quality=84, log=None):
    """同时写素材库（大图）与发布目录（小图）。"""
    base, _ = os.path.splitext(rel)
    ext = {"png": ".png", "webp": ".webp", "jpg": ".jpg"}[fmt]

    lib_im = fit(im, lib_w)
    n_lib = _save(lib_im, os.path.join(LIB, base + ".png"), "png", 0)

    pub_im = fit(im, pub_w)
    n_pub = _save(pub_im, os.path.join(PUB, base + ext), fmt, quality)

    if log is not None:
        log.append({
            "path": rel, "lib": base + ".png", "pub": base + ext,
            "lib_size": lib_im.size, "pub_size": pub_im.size,
            "lib_bytes": n_lib, "pub_bytes": n_pub,
        })


# ----------------------------------------------------------------- 任务表
# (源文件, 库内路径, 库最大宽, 发布最大宽, 格式)
JOBS = [
    # 品牌 —— logo 需要锐利，保持 PNG
    ("有你搭字.png",   "brand/logo-horizontal.png", 1400, 640, "png"),
    ("UniDA logo.png", "brand/logo-lockup.png",      900, 560, "png"),

    # 吉祥物 U 星球 —— 透明 + 小尺寸，PNG 更稳妥
    ("Ulogo.png",      "mascot/u-planet.png",        600, 260, "png"),

    # 人物立绘 —— 透明大图，WebP 省 80% 体积
    ("三人背景.png",   "characters/trio-back.png",   900, 700, "webp"),
    ("男生.png",       "characters/char-boy.png",    700, 380, "webp"),
    ("女生.png",       "characters/char-girl-guitar.png", 700, 380, "webp"),
    ("女生2.png",      "characters/char-girl-cap.png",    700, 380, "webp"),

    # 三人正面（自带浅色雾面底，不是透明图，按插画处理）
    ("三人可抠图.png", "illustrations/trio-front.jpg", 900, 720, "jpg"),
]

# 元素1 内嵌 10 个 3D 元素（连通域实测边界）
ELEM1 = [
    ("icon-study.png",  (91, 227, 345, 475)),
    ("icon-run.png",    (415, 230, 679, 471)),
    ("icon-horn.png",   (756, 226, 983, 466)),
    ("icon-gift.png",   (1079, 235, 1380, 460)),
    ("icon-team.png",   (138, 615, 456, 888)),
    ("icon-planet.png", (561, 596, 883, 882)),
    ("swatch-1.png",    (1001, 625, 1123, 746)),
    ("swatch-2.png",    (1134, 625, 1256, 746)),
    ("swatch-3.png",    (1001, 756, 1123, 876)),
    ("swatch-4.png",    (1134, 756, 1256, 876)),
]

# 元素2 里挑出的可复用装饰贴纸
ELEM2 = [
    ("deco-sparkle-1.png", (74, 278, 157, 361)),
    ("deco-sparkle-2.png", (203, 279, 285, 360)),
    ("deco-shield.png",    (1050, 386, 1159, 502)),
    ("deco-chat.png",      (1222, 390, 1380, 502)),
    ("deco-orbit-1.png",   (81, 648, 447, 781)),
    ("deco-cloud.png",     (58, 966, 305, 1057)),
    ("deco-heart.png",     (449, 820, 555, 919)),
    ("deco-appicon.png",   (69, 800, 218, 946)),
]

# 背景（不透明，全部 JPEG）
BG = [
    ("校园青春欢跑乐章.png", "backgrounds/bg-campus-sky.jpg",   (0, 0, 853, 460), 1100, 750),
    ("校园青春欢跑乐章.png", "backgrounds/bg-grass.jpg",        (0, 1500, 853, 1844), 900, 640),
    ("个人.png",             "backgrounds/bg-campus-building.jpg", (1000, 230, 1395, 570), 800, 560),
]


def main():
    log = []
    missing = []

    for src, rel, lw, pw, fmt in JOBS:
        p = os.path.join(SRC, src)
        if not os.path.exists(p):
            missing.append(src)
            continue
        im = load(p)
        if fmt in ("png", "webp"):
            im = trim(defringe(im))
        emit(im, rel, lw, pw, fmt, 84, log)

    p1 = os.path.join(SRC, "元素1.png")
    if os.path.exists(p1):
        sheet = load(p1)
        for name, box in ELEM1:
            c = trim(defringe(sheet.crop(box), erode=1, tint=0.75))
            emit(c, "illustrations/" + name, 220, 150, "png", 0, log)

    p2 = os.path.join(SRC, "元素2.png")
    if os.path.exists(p2):
        sheet = load(p2)
        for name, box in ELEM2:
            c = trim(defringe(sheet.crop(box), erode=1, tint=0.7))
            emit(c, "illustrations/" + name, 240, 160, "png", 0, log)

    for src, rel, box, lw, pw in BG:
        p = os.path.join(SRC, src)
        if not os.path.exists(p):
            missing.append(src)
            continue
        im = Image.open(p).convert("RGB").crop(box)
        emit(im, rel, lw, pw, "jpg", 88, log)

    # ------------------------------------------------------------- 报表
    print(f"{'素材':42s} {'库':12s} {'发布':12s} {'发布体积':>10s}")
    print("-" * 82)
    lib_total = pub_total = 0
    for r in sorted(log, key=lambda x: -x["pub_bytes"]):
        lib_total += r["lib_bytes"]
        pub_total += r["pub_bytes"]
        print(f"{r['path']:42s} {r['lib_size'][0]}x{r['lib_size'][1]:<7} "
              f"{r['pub_size'][0]}x{r['pub_size'][1]:<7} {r['pub_bytes']/1024:>8.0f}KB")
    print("-" * 82)
    print(f"库合计 {lib_total/1024/1024:.2f} MB    发布合计 {pub_total/1024/1024:.2f} MB")
    if missing:
        print("缺失源文件:", sorted(set(missing)))

    with open(os.path.join(LIB, "asset-manifest.json"), "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    print(f"清单已写入 {os.path.join(LIB, 'asset-manifest.json')}")


if __name__ == "__main__":
    main()
