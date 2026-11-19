# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
from scipy import ndimage

for n in ["tab-discover.png", "tab-message.png", "tab-home.png", "tab-mine.png"]:
    p = f"H:/UniDA/unida/static/unida/tabbar/{n}"
    im = Image.open(p)
    a = np.array(im)[:, :, 3].astype(np.int64)
    cs = a.sum(axis=0)
    print(n, "size", im.size, "alpha max", a.max(), "col-sum max", cs.max())
    nz = np.where(cs > 0)[0]
    if len(nz) == 0:
        print("  全透明!")
        continue
    gaps = np.where(np.diff(nz) > 3)[0]
    segs = []
    s = nz[0]; prev = nz[0]
    for g in gaps:
        segs.append((int(s), int(prev)))
        s = nz[g + 1]; prev = nz[g + 1]
    segs.append((int(s), int(prev)))
    print("  alpha段:", segs)
    # 连通域：保留最大域，清掉残影
    mask = a > 8
    lab, num = ndimage.label(mask)
    if num > 1:
        sizes = ndimage.sum(mask, lab, range(1, num + 1))
        keep = int(np.argmax(sizes)) + 1
        removed = num - 1
        a[lab != keep] = 0
        print(f"  连通域 {num} 个，已清掉 {removed} 个残影域")
        out = np.dstack([np.array(im)[:, :, :3], a.astype(np.uint8)])
        Image.fromarray(out, "RGBA").save(p, optimize=True)
    else:
        print("  单连通域，干净")
