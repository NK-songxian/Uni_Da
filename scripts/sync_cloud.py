# -*- coding: utf-8 -*-
"""
同步 common/cloud.js 到编译产物（ES module → CommonJS）
以及把 api 文件里的 import 转成 require。
"""
import os

ROOT = r"H:\UniDA\unida"
DIST = os.path.join(ROOT, "unpackage", "dist", "dev", "mp-weixin")
SRC = os.path.join(ROOT, "common", "cloud.js")
DST = os.path.join(DIST, "common", "cloud.js")


def cloud_to_commonjs(src):
    s = src
    s = s.replace("export const ", "const ")
    s = s.replace("export function ", "function ")
    # uniCloud 只在云端模式启用，产物里加保护避免未关联服务空间时报错
    s = s.replace(
        "return uniCloud.callFunction({",
        "if (typeof uniCloud === 'undefined') {\n"
        "\t\tthrow new Error('uniCloud 未启用：请在 HBuilderX 关联服务空间并上传云函数');\n"
        "\t}\n"
        "\treturn uniCloud.callFunction({")
    s += "\nmodule.exports = { CLOUD_MODE, callCloud, saveSession, getToken, getUser, clearSession };\n"
    return s


def patch_api_imports(src):
    """把 api 文件里对 cloud.js 的 import 转成 require（产物路径 ../cloud.js）"""
    import re
    s = src
    s = re.sub(
        r"import\s*\{([^}]+)\}\s*from\s*'@/common/cloud\.js';",
        lambda m: "const {%s} = require('../cloud.js');" % m.group(1),
        s
    )
    return s


def sync_cloud():
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with open(SRC, encoding="utf-8") as f:
        src = f.read()
    with open(DST, "w", encoding="utf-8") as f:
        f.write(cloud_to_commonjs(src))
    return DST


if __name__ == "__main__":
    p = sync_cloud()
    print("已同步云模块:", p)
