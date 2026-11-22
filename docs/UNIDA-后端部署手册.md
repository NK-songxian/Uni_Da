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

## 第 3 步：上传公共模块和云函数

1. HBuilderX 左侧右键 **`uniCloud-alipay/cloudfunctions/common`** → 「上传公共模块」
2. 再右键 **`uniCloud-alipay/cloudfunctions`** → 「上传所有云函数」（或逐个右键每个云函数 → 上传）
3. 等待控制台显示上传成功

---

## 第 4 步：创建数据库集合（可选，不建也能跑）

云函数已内置种子数据，**不建集合也能显示内容**。想用真实数据库管理时：

1. 打开 `uniCloud-alipay/database/README.md` 看集合清单
2. HBuilderX 里右键 `database` → 新建集合，按清单创建（如 `users`、`feed`、`discover_items` 等）
3. 需要初始数据时，把 `database/seed/` 下的 JSON 导入对应集合
4. 建议把集合权限设为「仅云函数可读写」

`users` 集合**无需手动创建**——登录时云函数会自动写入（首次登录自动生成）。

---

## 第 5 步：配置微信小程序合法域名

支付宝云调用需要在微信小程序后台加白名单：

1. 登录 https://mp.weixin.qq.com → 开发管理 → 开发设置 → 服务器域名
2. 在 **request 合法域名** 中添加：
   ```
   https://你的空间ID.api-hz.cloudbasefunction.cn
   ```
   （空间 ID 在 HBuilderX 关联后的云服务空间详情里能看到）
3. 保存

> 开发阶段可在微信开发者工具勾选「不校验合法域名」先跳过。

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

## 第 7 步：验证

1. 微信开发者工具打开 `unpackage/dist/dev/mp-weixin/`
2. 打开登录页 → 点微信登录 → 观察：
   - 控制台 `[cloud] → login` / `[cloud] ← login` 日志（debug=true 时）
   - uniCloud 控制台 `users` 集合出现新用户记录
3. 进入首页 → 数据正常显示（若集合为空，显示的是种子数据）
4. 进入发现页 → 列表/筛选/排序正常

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
