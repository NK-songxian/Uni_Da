# -*- coding: utf-8 -*-
"""
生成 UNIDA 素材清单  gen_manifest.py
把 build_assets.py 的构建日志 + 人工维护的用途表，合并成 asset-manifest.json
运行：E:/anaco/envs/sam_gpu/python.exe scripts/gen_manifest.py
"""
import json
import os

ROOT = r"H:\UniDA\unida"
LOG = os.path.join(ROOT, "assets", "unida", "asset-manifest.json")
OUT = os.path.join(ROOT, "assets", "unida", "asset-manifest.json")

# 人工维护：库内路径 -> (用途, 推荐显示尺寸, 所属页面, 使用状态)
META = {
    "brand/logo-horizontal.png": (
        "品牌横版组合（U图标+有你搭字标），用于顶栏/登录页/关于页",
        "320×92rpx", ["global", "login", "mine"], "ready"),
    "brand/logo-lockup.png": (
        "官方完整组合（UNIDA + 有你搭，白色圆角底），仅用于启动页/关于页",
        "280×101rpx", ["splash", "mine/about"], "ready"),
    "mascot/u-planet.png": (
        "U 星球吉祥物（3D 光泽带行星环），品牌符号与情感载体",
        "120×116rpx", ["tabbar", "empty", "publish"], "ready"),
    "characters/char-boy.png": (
        "单人立绘·男生（网球拍+UNIDA卫衣），发现页/引导页主视觉",
        "380×838px", ["discover", "onboarding"], "ready"),
    "characters/char-girl-guitar.png": (
        "单人立绘·女生吉他（紫卫衣+耳机），音乐类活动与推荐位",
        "380×581px", ["discover", "activity-detail"], "ready"),
    "characters/char-girl-cap.png": (
        "单人立绘·女生鸭舌帽（羽毛球拍+牛仔），运动类活动与组局",
        "380×669px", ["discover", "party-detail"], "ready"),
    "characters/trio-back.png": (
        "三人背影（背 UNIDA 书包走向校园），首页 hero 底图；源图底部即裁切位，需贴容器底对齐",
        "700×545px", ["home"], "ready-底边裁切"),
    "illustrations/trio-front.jpg": (
        "三人正面合影（自带浅色雾面底，非透明），登录/引导/分享卡",
        "720×900px", ["login", "share-card"], "ready-需淡边融入"),
    "illustrations/icon-study.png": (
        "3D 图标·学习组队（学士帽+书堆）", "88×86rpx", ["home", "discover"], "ready"),
    "illustrations/icon-run.png": (
        "3D 图标·运动搭子（奔跑小人）", "88×80rpx", ["home", "discover"], "ready"),
    "illustrations/icon-horn.png": (
        "3D 图标·校园活动（喇叭）", "88×93rpx", ["home", "discover"], "ready"),
    "illustrations/icon-gift.png": (
        "3D 图标·互助/福利（礼盒）", "88×60rpx", ["home", "discover"], "ready"),
    "illustrations/icon-team.png": (
        "3D 图标·同校动态/社团（旗帜+人群）", "88×75rpx", ["home", "discover"], "ready"),
    "illustrations/icon-planet.png": (
        "3D 图标·找搭子/广场（星球+社媒气泡）", "88×78rpx", ["home", "discover"], "ready"),
    "illustrations/deco-appicon.png": (
        "扁平 U 应用图标（紫渐变 squircle），消息流/列表页头像框与角标底",
        "72×71rpx", ["message", "mine"], "ready"),
    "illustrations/deco-chat.png": (
        "装饰·对话气泡贴纸（白紫+橙点）", "100×71rpx", ["message", "empty"], "ready"),
    "illustrations/deco-heart.png": (
        "装饰·手绘爱心（紫色线稿）", "64×60rpx", ["activity-detail", "mine"], "ready"),
    "illustrations/deco-shield.png": (
        "装饰·认证盾牌（紫+对勾）", "56×60rpx", ["mine", "verify"], "ready"),
    "illustrations/deco-cloud.png": (
        "装饰·云朵（浅紫立体）", "120×44rpx", ["login", "empty"], "ready"),
    "illustrations/deco-orbit-1.png": (
        "装饰·金色椭圆光轨（极淡，仅作低对比背景装饰）", "160×58rpx", ["home"], "ready-对比度低"),
    "illustrations/deco-sparkle-1.png": (
        "装饰·四角星闪光（黄）", "48×48rpx", ["global"], "ready"),
    "illustrations/deco-sparkle-2.png": (
        "装饰·四角星闪光（紫）", "48×48rpx", ["global"], "ready"),
    "illustrations/swatch-1.png": (
        "色卡·品牌紫渐变（仅作配色参考，不作画面元素）", "-", ["reference"], "reference"),
    "illustrations/swatch-2.png": (
        "色卡·阳光黄渐变（仅作配色参考）", "-", ["reference"], "reference"),
    "illustrations/swatch-3.png": (
        "色卡·天空蓝渐变（仅作配色参考）", "-", ["reference"], "reference"),
    "illustrations/swatch-4.png": (
        "色卡·蜜桃粉渐变（仅作配色参考）", "-", ["reference"], "reference"),
    "backgrounds/bg-campus-sky.jpg": (
        "背景·校园天空（蓝天白云+黄叶+紫花树），顶栏与 hero 后景",
        "750×404px", ["home", "discover"], "ready"),
    "backgrounds/bg-grass.jpg": (
        "背景·草坪花丛（绿草+紫花），页面底部收边",
        "640×258px", ["home"], "ready"),
    "backgrounds/bg-campus-building.jpg": (
        "背景·UNIDA 教学楼一角（紫调建筑+樱花），个人页头图",
        "395×340px", ["mine"], "ready-分辨率偏低"),
}

# 缺失清单：明确记录，不假装已有
MISSING = [
    ("独立成就徽章 PNG", "badges/", "展板里的 5 枚勋章与展台底座粘连，无法单独取用；需要独立透明徽章 ×6（学习/运动/社交/活动/连续/校园之星）"),
    ("底部导航图标集（品牌版）", "icons/tabbar/", "展板导航图标内嵌在设计稿里不可取；现有 static/icons 的 20 个是自绘白色线性图标，非品牌资产，需按 U 风格重绘（默认灰 + 选中紫双态 + 发布态）"),
    ("分类图标选中态变体", "illustrations/", "现有 6 个 3D 图标只有常态，缺选中/激活态"),
    ("空状态插画", "illustrations/empty/", "无数据、无网络、无消息、无结果 共 4 张，是去模板化最关键的一组，目前完全缺失"),
    ("真实活动封面图", "activities/", "现有 art-*.png 是从登录页裁的局部插画，不是活动实景；正式运营需要 12+ 张活动封面（球局/音乐节/露营/自习/招新/志愿）"),
    ("等级与成长值视觉", "badges/level/", "Lv.1~Lv.6 等级徽章 + 经验条刻度，个人页成长体系必需"),
    ("头像占位图集", "characters/avatars/", "6 张不同风格的默认头像（男生/女生/中性 × 2）"),
    ("学校认证角标", "badges/", "「在校认证」小角标，个人卡与动态卡高频使用"),
    ("兴趣标签图标集", "icons/interest/", "展板上的兴趣标签图标是设计稿内嵌，需独立导出 12 个（羽毛球/音乐/学习/摄影/编程/艺术/运动/美食/旅行/游戏/电影/志愿）"),
    ("分享海报模板", "share/", "活动分享卡 9:16 底图，用于生成朋友圈海报"),
    ("加载与刷新动效", "motion/", "U 星球转圈 loading、下拉刷新 U 弹跳，建议用 CSS 实现不占包体"),
]


def main():
    with open(LOG, "r", encoding="utf-8") as f:
        build = json.load(f)

    items = []
    for b in build:
        p = b["path"]
        purpose, display, pages, status = META.get(
            p, ("（未登记用途，需补充）", "-", [], "unknown"))
        items.append({
            "文件名": os.path.basename(b["pub"]),
            "文件路径": "/static/unida/" + b["pub"],
            "素材库路径": "assets/unida/" + b["lib"],
            "素材用途": purpose,
            "图片尺寸": f'{b["pub_size"][0]}x{b["pub_size"][1]}',
            "库内尺寸": f'{b["lib_size"][0]}x{b["lib_size"][1]}',
            "是否透明背景": "是" if b["pub"].endswith((".png", ".webp")) and
                            not p.endswith((".jpg",)) else "否",
            "推荐显示尺寸": display,
            "所属页面": pages,
            "使用状态": status,
            "体积KB": round(b["pub_bytes"] / 1024),
        })

    doc = {
        "项目": "UNIDA 有你搭",
        "版本": "v1.0",
        "更新时间": "2026-11-19",
        "说明": "发布目录 static/unida 进小程序包；素材库 assets/unida 为原尺寸备份，不进包。",
        "统计": {
            "文件数": len(items),
            "发布总体积MB": round(sum(i["体积KB"] for i in items) / 1024, 2),
            "可用": sum(1 for i in items if i["使用状态"].startswith("ready")),
            "仅参考": sum(1 for i in items if i["使用状态"] == "reference"),
            "缺失项": len(MISSING),
        },
        "素材": items,
        "缺失素材": [{"名称": n, "目标目录": d, "说明": s} for n, d, s in MISSING],
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)

    print(f"清单已写入 {OUT}")
    print(f"素材 {len(items)} 项 / 发布 {doc['统计']['发布总体积MB']} MB / 缺失 {len(MISSING)} 项")
    unknown = [i["文件路径"] for i in items if i["使用状态"] == "unknown"]
    if unknown:
        print("未登记用途:", unknown)


if __name__ == "__main__":
    main()
