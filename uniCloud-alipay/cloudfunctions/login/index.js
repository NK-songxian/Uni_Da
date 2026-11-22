/**
 * 云函数 login —— 微信登录
 * ------------------------------------------------------------------
 * 流程：
 *   1. 前端 wx.login() 拿 code → 调本云函数
 *   2. 本函数用 code 换 openid（真实模式走微信 code2Session）
 *   3. 查 users 集合：有则更新登录时间，无则新建用户
 *   4. 返回 { openid, token, isNew, user }
 *
 * 双模式：
 *   - useRealLogin=false（默认）：用 code 派生稳定临时 openid，先跑通链路
 *   - useRealLogin=true 且填好 AppSecret：真实微信登录
 *
 * token 为轻量签名串（openid + 时间戳 + 简单签名），存 users 表 token 字段。
 * 生产环境建议改用 uni-id 或 JWT，本实现适合校园项目起步。
 */
'use strict';

const crypto = require('crypto');

// 公共模块：uni-config-center（需在 HBuilderX 里上传此公共模块）
// 注意：本项目用的是自写简单公共模块（module.exports = {...}），
// 不是官方 uni-config-center 的 .config() 用法，直接解构即可。
let cfg = {
	weixin: { appid: 'wx7bb5cba400820f1b', appsecret: '', useRealLogin: false }
};
try {
	const uc = require('uni-config-center');
	// 兼容两种形态：官方 .config() 与自写对象
	if (uc && typeof uc.config === 'function') {
		cfg = uc.config();
	} else if (uc && uc.weixin) {
		cfg = uc;
	}
} catch (e) {
	console.warn('uni-config-center 未上传，使用内置默认配置:', e.message);
}

const WX = cfg.weixin || {};

/** 真实微信登录：code2Session 换 openid */
async function code2Session(code) {
	const url = 'https://api.weixin.qq.com/sns/jscode2session'
		+ '?appid=' + encodeURIComponent(WX.appid)
		+ '&secret=' + encodeURIComponent(WX.appsecret)
		+ '&js_code=' + encodeURIComponent(code)
		+ '&grant_type=authorization_code';

	// uniCloud 云函数内置 universal-fetch（无需 axios）
	const res = await uniCloud.httpclient.request(url, {
		method: 'GET',
		dataType: 'json',
		timeout: 8000
	});
	const data = res && res.data;
	if (!data || data.errcode) {
		throw new Error('微信登录失败：' + ((data && data.errmsg) || '未知错误'));
	}
	if (!data.openid) throw new Error('微信未返回 openid');
	return {
		openid: data.openid,
		unionid: data.unionid || ''
	};
}

/** 降级模式：用 code 派生稳定 openid（同一微信号每次登录 code 不同，故此模式仅供调试） */
function fakeOpenid(code) {
	return 'tmp_' + crypto.createHash('md5').update(String(code || 'guest')).digest('hex').slice(0, 24);
}

/** 生成登录 token */
function makeToken(openid) {
	const ts = Date.now();
	const sig = crypto.createHash('md5')
		.update(openid + '|' + ts + '|unida')
		.digest('hex').slice(0, 16);
	return openid + '.' + ts + '.' + sig;
}

exports.main = async (event) => {
	const code = event.code || '';
	const phoneCode = event.phoneCode || '';

	if (!code) {
		return { errCode: 1, errMsg: '缺少登录 code' };
	}

	try {
		let openid, unionid = '';

		if (WX.useRealLogin && WX.appsecret && WX.appsecret.indexOf('请替换') < 0) {
			const s = await code2Session(code);
			openid = s.openid;
			unionid = s.unionid;
		} else {
			openid = fakeOpenid(code);
		}

		const db = uniCloud.database();
		const users = db.collection('users');
		const token = makeToken(openid);

		const q = await users.where({ openid }).limit(1).get();
		const existing = q.data && q.data[0];

		let user;
		if (existing) {
			await users.doc(existing._id).update({
				lastLoginAt: Date.now(),
				token,
				...(unionid ? { unionid } : {})
			});
			user = { ...existing, token, lastLoginAt: Date.now() };
		} else {
			const newUser = {
				openid,
				unionid,
				token,
				nickname: '',
				avatar: '',
				phone: '',
				points: 0,
				school: '',
				createdAt: Date.now(),
				lastLoginAt: Date.now()
			};
			const add = await users.add(newUser);
			user = { ...newUser, _id: add.id };
		}

		return {
			errCode: 0,
			errMsg: 'ok',
			openid,
			token,
			isNew: !existing,
			// 不返回 openid 以外的敏感字段给前端日志；user 仅含前端展示所需
			user: {
				id: user._id,
				nickname: user.nickname,
				avatar: user.avatar,
				points: user.points,
				school: user.school
			},
			mode: (WX.useRealLogin && WX.appsecret && WX.appsecret.indexOf('请替换') < 0) ? 'real' : 'demo'
		};
	} catch (e) {
		console.error('login error:', e);
		return { errCode: 2, errMsg: e.message || '登录失败' };
	}
};
