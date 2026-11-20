# -*- coding: utf-8 -*-
"""生成 UNIDA tabbar 白栏 + U 型凹槽 PNG（@2x，真机必渲染，替代真机失效的 CSS mask）

凹槽透明露出页面背景，白栏主体纯白；顶部 curve 用 cos^2 钟形函数保证谷底与两肩平滑；
阴影用 alpha 下移+高斯模糊，跟随凹槽曲线，不用 CSS box-shadow（矩形阴影不跟随凹口）。
"""
import math, os
import numpy as np
from PIL import Image, ImageFilter

ROOT = r"H:\UniDA\unida"
OUT = os.path.join(ROOT, "static", "unida", "tabbar", "tabbar-sheet.png")

W, H = 750, 200          # @2x 高清；widthFix 满屏宽时显示 750rpx × 200rpx
CX = W // 2
BASE_Y = 26              # 白栏顶边两肩（@2x px）= 13rpx
HALF_W = 170             # 凹槽半宽（@2x px）——谷口宽 340px@2x = 170rpx
DEPTH = 92               # 凹槽深度（@2x px）= 46rpx，谷底 y=118px=59rpx
CORNER = 44              # 白栏顶部两角圆角半径（@2x px）


def main():
    alpha = np.zeros((H, W), dtype=np.uint8)
    top = []
    for x in range(W):
        y = float(BASE_Y)
        # U 型凹槽：cos^2 钟形，|u|<1 时中心最深、两肩零斜率平滑归零
        u = (x - CX) / HALF_W
        if abs(u) < 1:
            y += DEPTH * (math.cos(math.pi / 2 * u) ** 2)
        # 顶部两角圆角
        if x < CORNER:
            y += CORNER - math.sqrt(max(0, CORNER ** 2 - (CORNER - x) ** 2))
        elif x > W - CORNER:
            y += CORNER - math.sqrt(max(0, CORNER ** 2 - (x - (W - CORNER)) ** 2))
        top.append(y)

    for x in range(W):
        y0 = int(round(top[x]))
        if y0 < H:
            alpha[y0:H, x] = 255
    mask = Image.fromarray(alpha, "L")

    # 阴影层：alpha 下移 7px + 高斯模糊，品牌紫 16% 不透明度
    sh = Image.new("L", (W, H), 0)
    sh.paste(mask, (0, 7))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    sh_arr = np.asarray(sh, dtype=np.float32) * 0.16
    sh_rgba = np.zeros((H, W, 4), dtype=np.uint8)
    sh_rgba[:, :, :3] = (123, 97, 255)
    sh_rgba[:, :, 3] = sh_arr.astype(np.uint8)

    # 白栏层：纯白（底部极淡紫渐变，干净不脏）
    bar = np.zeros((H, W, 4), dtype=np.uint8)
    for yy in range(H):
        t = yy / (H - 1)
        bar[yy, :, 0] = int(255 - 3 * t)
        bar[yy, :, 1] = int(255 - 5 * t)
        bar[yy, :, 2] = 255
    bar[:, :, 3] = alpha

    out = Image.alpha_composite(Image.fromarray(sh_rgba, "RGBA"), Image.fromarray(bar, "RGBA"))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out.save(OUT)
    print("已生成", OUT, out.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
