# UNIDA 云数据库集合设计（uniCloud 支付宝云）

## 集合一览

| 集合名 | 用途 | 对应云函数 | 是否必须 |
|--------|------|-----------|---------|
| `users` | 用户（openid/昵称/积分/登录态） | login | ✅ 登录自动写入 |
| `app_config` | 全局配置（学校名/今日匹配数） | getHomeData | 可选 |
| `home_categories` | 首页六大入口 | getHomeData | 可选 |
| `home_promos` | 首页任务轮播 | getHomeData | 可选 |
| `activities` | 现在可以搭 / 发现页搭子 | getHomeData / getDiscover | 可选 |
| `home_acts` | 首页校园活动横滑卡 | getHomeData | 可选 |
| `mates` | 首页同频推荐 | getHomeData | 可选 |
| `feed` | 同校动态（分页） | getHomeData | 可选 |
| `discover_items` | 发现页列表（分页/筛选/排序） | getDiscover | 可选 |

## 核心原则：不导入也能跑

所有云函数都做了**双保险**：集合存在且有数据 → 用数据库；集合为空或不存在 → 用云函数内嵌的种子数据。

所以你可以**先上传云函数跑通全链路**，之后再慢慢导入集合、把种子数据替换成真实数据。

## 导入方法

1. HBuilderX → 打开 `uniCloud-alipay/database/`
2. 右键 → 新建集合，按上表创建
3. 每个集合右键 → 导入 JSON（每行一个 JSON 对象，即 JSON Lines 格式）
4. 导入 `seed/` 目录下对应的 `.json` 文件

## users 集合字段（登录自动写入，无需手动导入）

```
openid      string   微信唯一标识
unionid     string   开放平台统一标识（可选）
token       string   登录态
nickname    string   昵称
avatar      string   头像
phone       string   手机号
points      number   积分
school      string   学校
createdAt   number   创建时间戳
lastLoginAt number   最后登录时间戳
```

## 权限建议

uniCloud 数据库权限：**仅云函数可读写**（客户端不直接访问数据库），所有读写都经过云函数，便于鉴权和防止越权。
