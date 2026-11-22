# UNIDA 系统实现盘点（2026-11-22）

> 对照开发总纲《UNIDA开发定位V1.md》与《UNIDA-PAGE-PLAN.md》，逐系统核对「文档要求 vs 当前实现」。
> 结论先行：**10 大系统全部有 UI（29 页 V2 达标），其中 7 个系统已接真实云端数据，3 个系统仍有演示/待开发部分。**

---

## 一、文档口径（开发文档要求）

| 维度 | 文档要求 |
|---|---|
| 业务系统 | **10 大系统**（A 登录身份 / B 首页 / C 发现 / D 活动 / E 发布 / F 跑腿 / G 社区 / H 消息 / I 积分 / J 个人中心） |
| 功能点 | A~J 共 **102 个功能点**（映射约 40+ 个独立 UI 界面，部分合并实现） |
| 数据库 | **18 个集合**（users/campuses/activities/bookings/orders/posts/comments/likes/favorites/follows/conversations/messages/notifications/point_ledgers/reviews/reports/categories/banners） |
| 组件库 | **23 个公共组件** |
| 底部导航 | 5 入口（首页/发现/发布/消息/我的）✅ |

## 二、当前实际

| 维度 | 现状 |
|---|---|
| UI 页面 | **29 个 C 端页面全部完成且 V2 视觉达标**（另有 index 模板残留页 1 个，提审前删除） |
| 云函数 | **13 个**：login / getHomeData / getDiscover / publishItem / saveProfile / joinActivity / getMyOrders / favorite / like / posts / chat / points / itemDetail |
| 集合 | **16 个**：users / discover_items / activities / activity_members / feed / app_config / home_categories / home_promos / home_acts / mates / favorites / likes / posts / post_comments / messages / checkins |
| 真实数据接入 | **16 个页面已接云端**（28 处 callCloud）：登录、首页、发现、活动详情、报名确认、报名成功、我的报名、社区、帖子详情、消息、聊天、积分、签到、我的、我的收藏、我的发布 |

## 三、逐系统真实度

| 系统 | 文档功能点 | 真实度 | 已实现（真实入库） | 未完成 / 演示态 |
|---|---|---|---|---|
| A 登录与身份 | 9 | ★★★★★ 90% | 登录、自动登录、微信一键登录、协议、学校/昵称/兴趣资料（saveProfile 真实入库） | 手机验证码（演示）、校园身份认证页、品牌启动页 |
| B 首页 | 10 | ★★★★☆ 80% | 8 大模块齐全，getHomeData 云端拉取（含 mock 兜底） | 搜索页、切换学校、附近活动 |
| C 发现 | 11 | ★★★★☆ 80% | tab/筛选/排序/双列瀑布，getDiscover 云端 | 搜索页 |
| D 活动系统 | 12 | ★★★★☆ 75% | 详情（itemDetail）、预约确认、报名（joinActivity）、预约成功、我的报名（getMyOrders）、收藏 | 取消预约、活动场景签到、活动评价（review 页演示）、发起人/报名人员卡片（静态） |
| E 发布系统 | 6 | ★★★☆☆ 55% | 发布中心 UI、通用发布表单真实入库（publishItem） | 6 类独立表单（当前入口 toast）、图片上传、精确时间/地点选择 |
| F 跑腿系统 | 12 | ★☆☆☆☆ 15% | 跑腿大厅 / 订单详情 UI | **整系统未真实化**：无 orders 集合、接单、进度、交付、我的接单、订单评价全部演示 |
| G 社区系统 | 10 | ★★★★☆ 85% | 帖子列表/发布/详情/评论/点赞/收藏（本轮全真实） | 分享卡片、用户主页（mock）、关注关系、举报提交（页有但演示） |
| H 消息系统 | 7 | ★★★★☆ 80% | 会话列表、私聊收发（5s 轮询）、官方系统通知、未读角标（本轮全真实） | 业务通知（活动/预约/订单通知，无 notifications 集合）、消息搜索 |
| I 积分系统 | 10 | ★★★★☆ 75% | 积分余额、每日签到、连签、任务状态、成长等级（服务端管理，本轮真实） | 积分流水（无 point_ledgers）、商城兑换（演示）、兑换记录、勋章系统 |
| J 个人中心 | 15 | ★★★☆☆ 65% | 资料、我的发布、我的收藏、我的报名、我的积分/等级（本轮真实） | 我的搭子、我的订单（跑腿）、我的评价、我的勋章、关注/粉丝、设置、隐私管理、反馈 |

**总体：约 7.5 / 10 个系统达到"可真实使用"，F 跑腿是最大缺口。**

## 四、数据库对照（文档 18 → 实际 16）

- ✅ 已有并使用：users、activities、posts、comments(post_comments)、likes、favorites、conversations+messages(messages)、categories(home_categories)、banners(home_promos)
- ✅ 概念对应：bookings→activity_members、campus 信息暂并入 users.school
- ❌ 缺：campuses、orders（跑腿）、follows、notifications、point_ledgers、reviews、reports
- 权限：全部 schema `read:false / write:false`，仅云函数读写 ✅

## 五、剩余工作清单（按优先级）

1. **F 跑腿闭环真实化**（orders 集合 + 接单/进度/交付/评价云函数）—— 文档要求的第二大业务闭环
2. **业务通知系统**（notifications 集合 + 报名成功/被点赞/被评论时写入 + 消息页通知列表）
3. **积分流水 point_ledgers**（签到/报名/发布/奖励全部记流水 + 积分页流水列表 + 商城兑换真实扣分）
4. **活动收尾**：取消预约、活动评价入库（reviews）、活动状态流转（报名中→进行中→已完成）
5. **图片上传**（uniCloud 云存储 + 资料头像/发帖配图/发布封面）
6. **发布系统**：6 类发布独立表单（或统一表单带类型切换）+ 精确时间/地点选择接 pick-time/pick-place
7. **关注/用户主页真实化**（follows 集合）
8. **搜索页**（首页/发现/消息三处入口）
9. **设置/隐私/反馈页**（提审合规必需：设置里要有注销账号入口）
10. 提审前：删除 index 残留页、CLOUD_MODE.debug 改 false、隐私协议与权限声明、分包复核

## 六、组件库对照（文档 23 → 实际 4+）

已有：`unida-tabbar`、`unida-card`、`unida-category`、`unida-search` + 各页内复用样式（空态/统计块/筛选胶囊等以页内 class 形式复用，未抽公共组件）。
文档要求的 15 组件清单（UBrand/UMascot/UEmptyState 等）多数以"页内实现"替代——功能都在，组件抽象未做。**不影响功能验收，影响后续维护效率，建议提审后再做组件化重构。**
