/**
 * 微信登录配置模板（可提交到仓库）
 * ------------------------------------------------------------------
 * 真实配置在同级 index.js，已加入 .gitignore，不会进仓库。
 *
 * 换电脑 / 换测试号时：
 *   1. 复制本文件为 index.js
 *   2. 填入该测试号配套的 AppSecret（微信公众平台 → 开发管理 → 开发设置）
 *   3. useRealLogin 改为 true
 *   4. HBuilderX 里重新上传 common 公共模块 + login 云函数
 *
 * ⚠️ AppSecret 必须与 appid（wx7bb5cba400820f1b）属于同一个小程序，
 *    否则 code2Session 会返回 invalid appsecret。
 */
module.exports = {
	weixin: {
		appid: 'wx7bb5cba400820f1b',
		appsecret: '在这里填AppSecret',
		useRealLogin: false
	}
};
