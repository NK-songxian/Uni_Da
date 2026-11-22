# UNIDA 后端部署操作手册（uniCloud 支付宝云）

> 目标：打通 **用户登录 + 首页/发现真实数据**。
> 你已开通支付宝云服务空间（首月免费），下面按步骤做即可。
> 全程在 **HBuilderX** 里操作，我写的代码已经就位。

---

## 第 0 步之前：微信开发者工具要打开哪个目录（最容易踩的坑）

**必须打开编译产物目录，不是源码根目录：**

```
✅ 正确：H:\UniDA\unida\unpackage\dist\dev\mp-weixin
❌ 错误：H:\UniDA\unida   ← 这里只有 pages.json，没有 app.json
```

如果打开错目录，会报：`app.json: 在项目根目录未找到 app.json`。

原因：uni-app 源码用 `pages.json`，编译后才生成微信原生的 `app.json`。源码根目录还有个历史遗留的 `project.config.json`，会让微信开发者工具误以为它是原生小程序项目，实际打开发现没有 app.json 就报错。

> 每次 HBuilderX 重新编译后，产物目录会被刷新，但路径不变，仍是上面那个正确路径。

---

## 第 0 步：确认工程结构（已完成 ✅）

我已在工程里生成：

```
uniCloud-alipay/
├── cloudfunctions/
│   ├── common/
│   │   └── uni-config-center/   ← 微信配置公共模块
│   ├── login/                    ← 登录云函数
│   ├── getHomeData/              ← 首页数据云函数
│   └── getDiscover/              ← 发现页云函数
└── database/
    ├── README.md                 ← 集合设计说明
    └── seed/                     ← 可导入的初始数据 JSON
common/
└── cloud.js                      ← 前端云服务适配层（开关在这里）
```

---

## 第 1 步：关联服务空间（HBuilderX）

1. 打开 HBuilderX，加载 `H:/UniDA/unida` 工程
2. 在左侧文件树找到 **`uniCloud-alipay`** 目录
3. **右键点击 `uniCloud-alipay`** → 「关联服务空间」/「关联云服务空间或项目」
4. 登录 DCloud 账号 → 选择你已开通的**支付宝云**服务空间 → 确认
5. 关联成功后目录会显示空间名

> ⚠️ 如果右键没有这个菜单，说明项目未启用 uniCloud：打开 `manifest.json` → 「uniCloud」页签 → 勾选启用，保存后重试。

---

## 第 2 步：配置微信登录凭证（本次已填好 ✅）

已把 AppSecret 填入 `uniCloud-alipay/cloudfunctions/common/uni-config-center/index.js`，`useRealLogin: true`。

- 🔒 该文件已加入 `.gitignore` 并从 git 仓库移除，**密钥只在本机和云端，不会进 GitHub**
- 📋 仓库里留了 `index.example.js` 模板，换测试号时复制成 `index.js` 再填

> ⚠️ **必须重新上传才生效**（代码改过了）：见下方「重新上传」提示。

> 🔑 **凭证匹配**：AppSecret 必须和 AppID `wx7bb5cba400820f1b` 属于**同一个小程序**。如果登录报 `invalid appsecret`，说明这串 secret 是另一个测试号的，需要去对应小程序后台取配套的（或把项目 AppID 改成那个测试号）。

### 换测试号/换电脑的操作

1. 复制 `index.example.js` 为 `index.js`
2. 填新测试号的 AppSecret，`useRealLogin: true`
3. HBuilderX 重新上传公共模块 + login 云函数

---

## ⚠️ 代码改动后必须重新上传（重要）

只要改了 `cloudfunctions/` 下的任何文件（云函数或公共模块），云端不会自动更新，必须：

1. 右键 `uniCloud-alipay/cloudfunctions/common` → 「上传公共模块」
2. 右键 `uniCloud-alipay/cloudfunctions/login` → 「上传部署」
3. 等控制台显示上传成功，再测试登录

本次修复了公共模块读取 bug + 填入凭证，**这两步一定要重做**。

---

## 第 3 步：上传公共模块、云函数、数据库集合（已脚本化）

不用再逐个右键上传。项目里已加一键部署脚本：

```bash
E:/anaco/envs/sam_gpu/python.exe H:/UniDA/unida/scripts/deploy_cloud.py
```

它会自动：
1. 逐个上传 `cloudfunctions/common/` 下**非空**公共模块（跳过空模块，避免 `all` 模式中断）
2. 逐个上传全部云函数（`login` / `getHomeData` / `getDiscover` / `publishItem`）
3. 上传 `database/*.schema.json`，自动创建全部集合（含 `discover_items`、`users` 等）

核对云端现状：

```bash
E:/anaco/envs/sam_gpu/python.exe H:/UniDA/unida/scripts/deploy_cloud.py --check
```

> 脚本使用 HBuilderX CLI，需要 HBuilderX 已登录 DCloud 且已关联服务空间。本机 CLI 路径 `H:/HBuilderX/cli.exe`，服务空间 `env-00jy72vf1i57`。

手动右键上传仍可用作兜底，但改完代码后建议直接跑脚本，不用再记哪些没传。

---

## 第 4 步：数据库集合（已由脚本自动创建 ✅）

本地 `uniCloud-alipay/database/*.schema.json` 已覆盖全部集合，跑一次 `deploy_cloud.py` 就会自动建好 `users` / `app_config` / `discover_items` / `feed` 等 9 个集合，权限均为「仅云函数可读写」。

需要初始数据时，再把 `database/seed/` 下的 JSON 导入对应集合即可（不导入也能跑，云函数有种子兜底）。

---

## 第 5 步：配置微信小程序合法域名

支付宝云调用需要在微信小程序后台加白名单：

1. 登录 https://mp.weixin.qq.com → 开发管理 → 开发设置 → 服务器域名
2. 在 **request 合法域名** 中添加（本项目实际值）：
   ```
   https://env-00jy72vf1i57.api-hz.cloudbasefunction.cn
   ```
3. 保存后，微信开发者工具里点「详情 → 域名信息 → 刷新项目配置」，或直接重新编译项目

开发阶段可临时跳过校验：

- 微信开发者工具 → 详情 → 本地设置 → 勾选「不校验合法域名…」
- 本项目产物 `project.config.json` 已补 `"urlCheck": false`，但部分版本仍会在页面顶部提示，勾选一次最稳

---

## 第 6 步：打开云端模式（关键开关）

一切就绪后，打开 `common/cloud.js`：

```js
export const CLOUD_MODE = {
	enabled: true,   // ← 把 false 改成 true
	debug: true      // 调试期可开，上线关掉
};
```

然后：
- 如果产物是 HBuilderX 真编译的：重新「运行到微信开发者工具」即可
- 如果是 sync 脚本产物：我已在产物里同步好 cloud.js，改 `unpackage/dist/dev/mp-weixin/common/cloud.js` 里的 `enabled: true`

---

## 第 7 步：5 分钟真实验证（按这个顺序做）

> 我已把 `common/cloud.js` 的 `enabled: true`、`debug: true` 同步到源码和产物。
> `debug: true` 会在微信开发者工具控制台打印 `[cloud] → 云函数名` 和 `[cloud] ← 返回结果`，验证完成后再改回 `false`。

### 7.1 先确认三件事（错了后面全白测）

1. **云函数已上传**：HBuilderX 控制台显示 `common` 公共模块 + `login` / `getHomeData` / `getDiscover` 上传成功。改过配置后必须**重新上传**，不是只保存本地文件。
2. **切到云端云函数**：HBuilderX 底部「前端控制台」右上角有一个连接切换，默认是 **`连接本地云函数`**。真实验证必须切成 **`连接云端云函数`**，否则跑的是本机模拟环境，数据库不会出现记录。
3. **打开正确项目目录**：微信开发者工具打开 `unpackage/dist/dev/mp-weixin/`；`urlCheck:false` 已配好，开发阶段不用管合法域名。

### 7.2 验证登录 + users 集合

1. 微信开发者工具 → 清掉本地缓存里的 `unida_token` / `unida_user`（或直接清 Storage），重新进登录页走一次微信登录。
2. 控制台应看到：
   ```text
   [cloud] → login {code: "..."}
   [cloud] ← login {errCode: 0, mode: "real", isNew: true, ...}
   ```
   - `mode: "real"` 说明微信 code2Session 成功；
   - 若 `mode: "demo"`，说明公共模块没上传或配置没读到。
3. HBuilderX 右键 `uniCloud-alipay` → 「打开 uniCloud Web 控制台」→ 数据库 → `users` 集合，应多出一条记录，带 `openid`、`token`、`createdAt`。
   > 集合不存在时，第一次登录会自动创建并写入。

### 7.3 验证首页 / 发现页真实数据

1. 进首页，控制台应看到 `[cloud] → getHomeData` / `[cloud] ← getHomeData`。
2. 进发现页，控制台应看到 `[cloud] → getDiscover` / `[cloud] ← getDiscover`。
3. **最硬的证据：改数据库，看界面变。**
   - 首页：在 Web 控制台把 `app_config` 里那条记录的 `school` 改成 `云端已连通测试大学`，下拉刷新首页，顶部学校名应跟着变。
   - 发现页：在 `discover_items` 集合新增一条记录（tab=0 才会出现在默认「找搭子」）：
     ```json
     {
       "id": "d999",
       "tab": 0,
       "category": "学习",
       "hot": true,
       "title": "【云端真实数据】验证成功",
       "cover": "/static/art/art-campus.jpg",
       "time": "现在",
       "place": "云端数据库",
       "joined": 1,
       "total": 2,
       "price": "免费",
       "members": [],
       "bar": "#805CFA",
       "barSoft": "rgba(128,92,250,.10)"
     }
     ```
     回到发现页下拉刷新，列表应出现这条标题。
4. 云函数返回里有 `_source.fromDB: true`（在 `[cloud] ←` 的日志里能看到），表示数据确实来自数据库而不是内置种子。

### 7.4 如果还是老数据

| 现象 | 先查这里 |
|------|----------|
| 控制台没有 `[cloud]` 日志 | `CLOUD_MODE.enabled` 被编译回 false；重跑 `scripts/sync_cloud.py` 或重新编译 |
| 有 `[cloud] error` | 看 errMsg：服务空间未关联 / 云函数未上传 / 未切到云端云函数 |
| `mode: "demo"` | 公共模块没重新上传，`uni-config-center` 没读到 AppSecret |
| 页面数据没变但日志正常 | 云函数读集合失败会回退种子数据；去数据库确认集合名拼写（`discover_items`、`app_config`） |
| `request has expired`（登录/读集合都报） | 支付宝云 **HBuilderX 本地调试读数据库的已知问题**，DCloud 已确认不影响线上 | 前端控制台右上角切到「连接云端云函数」后重试；`common/cloud.js` 已把这句翻译成明确提示 |
| `socket 合法域名校验出错 ws://10.68...:8090` / `Cannot send network request to localhost` | 这是 HBuilderX 开发模式日志通道，不是业务云请求 | 微信开发者工具「详情 → 本地设置」勾选「不校验合法域名…」，然后关闭项目重新打开；不用把 ws 域名加进后台 |
| 真机正常、模拟器不正常 | 微信开发者工具勾选「不校验合法域名」后重试 |

验证通过后，把 `common/cloud.js` 的 `debug` 改回 `false` 并重跑 `scripts/sync_cloud.py`，避免生产环境打印用户数据。

---

## 第 8 步：发布功能真实入库（已接入 publishItem）

前端 `publish-form` 已不再“演示成功”，改为调 `publishItem` 云函数写入 `discover_items`。

1. `discover_items` 集合已由 `deploy_cloud.py` 自动创建，不用手动建。
2. 云函数也已由脚本上传，确认过 `[cloud] → publishItem` 能调用即可。
3. 确认已登录（本地 Storage 有 `unida_token`），进入发布页填标题/时间/地点，点「发布活动」。
4. 控制台应看到：
   ```text
   [cloud] → publishItem {...}
   [cloud] ← publishItem { errCode:0, id:"d..." }
   ```
5. 自动跳回发现页，列表第一条应出现你刚发的标题；Web 控制台 `discover_items` 集合同步多一条记录。

> 云函数会校验 `unida_token` 签名，未登录或登录态伪造会返回 401，不会写入数据库。

---

## 第 9 步：资料完善真实入库（已接入 saveProfile）

`profile-setup` 页面现在会把「学校 / 昵称 / 兴趣」写入 `users` 集合，并把云端返回的 `user` 覆盖本地缓存。

1. 清掉本地 `unida_user` 后重新登录，或直接进 `profile-setup`
2. 填学校 + 昵称 + 选兴趣 → 点「完成」
3. 控制台应看到：
   ```text
   [cloud] → saveProfile {...}
   [cloud] ← saveProfile { errCode:0, user:{...} }
   ```
4. Web 控制台 `users` 集合中，对应 openid 那条记录应新增 `school` / `nickname` / `interests` 字段
5. 再次进入 `profile-setup`，已保存的学校/昵称/兴趣会自动回显

---

## 第 10 步：报名 / 加入活动真实入库（已接入 joinActivity + getMyOrders）

1. 首页 / 发现页点进活动详情 → 立即报名 → 报名确认页
2. 填人数 / 备注 → 提交报名
3. 控制台应看到：
   ```text
   [cloud] → joinActivity {...}
   [cloud] ← joinActivity { errCode:0, orderId:"UNI..." }
   ```
4. 自动跳到报名成功页；Web 控制台 `activity_members` 集合应多一条记录
5. 如果活动在 `discover_items` / `activities` 里有对应 `id`，对应条目的 `joined` 人数会同步 +人数
6. 进入「我的报名」，控制台应看到 `[cloud] ← getMyOrders`，列表显示刚才那条报名

---

## 故障排查

| 现象 | 原因 | 解决 |
|------|------|------|
| `uniCloud 未启用` | 未关联服务空间 | 回到第 1 步 |
| `request:fail 域名不在白名单` | 合法域名未配 | 第 5 步，或勾选不校验域名 |
| `service not found` | 云函数未上传 | 第 3 步重新上传 |
| 登录返回 demo 模式 | useRealLogin=false 或 secret 未填 | 第 2 步 |
| 首页数据不变 | CLOUD_MODE.enabled 还是 false | 第 6 步 |

---

## 回退方案

任何时候把 `common/cloud.js` 的 `enabled` 改回 `false`，整个 App 立即回到 mock 模式，界面和数据恢复原样，不影响开发。
