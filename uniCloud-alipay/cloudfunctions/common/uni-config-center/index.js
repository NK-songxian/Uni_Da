/**
 * uni-config-center 公共模块配置
 * ------------------------------------------------------------------
 * 微信登录凭证集中在这里配置。AppSecret 属于敏感信息，只在云端保存，
 * 绝不下发到小程序前端，也不要提交到公开仓库。
 *
 * 部署前：把 WX_APPID / WX_APPSECRET 换成你自己的（小程序后台 → 开发管理 → 开发设置）。
 */
module.exports = {
	weixin: {
		// 微信小程序 AppID（manifest.json 里的 appid，可明文）
		appid: 'wx7bb5cba400820f1b',
		// 微信小程序 AppSecret —— 请替换为真实值，切勿提交到 GitHub
		appsecret: '请替换为你的微信AppSecret',

		// 是否启用真实 code2Session。未填 secret 时为 false，
		// 登录函数会退化为「用 code 派生的临时 openid」，方便你先跑通链路。
		// 填好真实 secret 后改为 true 即可启用真实微信登录。
		useRealLogin: false
	}
};
