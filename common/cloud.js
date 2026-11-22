/**
 * UNIDA 云服务适配层  common/cloud.js
 * ------------------------------------------------------------------
 * 统一封装 uniCloud.callFunction，页面和 api 层都通过这里访问云端。
 *
 * 模式开关（USE_CLOUD）：
 *   - true  → 走真实云函数（需上传云函数 + 关联服务空间）
 *   - false → 走本地 mock（current api 文件内部实现，开箱即用）
 *
 * 这样你可以先在 mock 模式下继续开发，后端部署好之后把开关改成 true，
 * 页面代码一行都不用动。
 */

export const CLOUD_MODE = {
	// 全局总开关：后端部署完成后改为 true
	enabled: true,
	// 调试期打开，能在控制台看到每次 callCloud 的请求和返回；上线前改回 false
	debug: true
};

/** 调用云函数的统一入口（async 保证所有错误都变成可 catch 的 Promise rejection） */
export async function callCloud(name, data = {}) {
	if (!CLOUD_MODE.enabled) {
		throw new Error('CLOUD_DISABLED');
	}
	if (CLOUD_MODE.debug) {
		console.log('[cloud] →', name, data);
	}
	// 服务空间未关联 / 云函数未上传时给出明确提示，避免卡死
	if (typeof uniCloud === 'undefined') {
		throw new Error('云服务未就绪：请在 HBuilderX 关联服务空间并上传云函数');
	}
	try {
		const res = await uniCloud.callFunction({
			name,
			data
		});
		const out = res && res.result;
		if (CLOUD_MODE.debug) console.log('[cloud] ←', name, out);
		if (!out || out.errCode) {
			throw new Error((out && out.errMsg) || '云函数调用失败');
		}
		return out;
	} catch (e) {
		const msg = String((e && e.message) || e);
		// 支付宝云本地调试读数据库会报 request has expired（官方已知问题，云函数线上不受影响）
		if (msg.indexOf('request has expired') >= 0) {
			throw new Error('本地调试数据库鉴权过期：请在 HBuilderX 前端控制台右上角切到「连接云端云函数」后重试');
		}
		console.error('[cloud] error', name, e);
		throw e;
	}
}

/** 本地登录态缓存 */
const TOKEN_KEY = 'unida_token';
const USER_KEY = 'unida_user';

export function saveSession(token, user) {
	try {
		uni.setStorageSync(TOKEN_KEY, token || '');
		uni.setStorageSync(USER_KEY, user || null);
	} catch (e) {}
}
export function getToken() {
	try { return uni.getStorageSync(TOKEN_KEY) || ''; } catch (e) { return ''; }
}
export function getUser() {
	try { return uni.getStorageSync(USER_KEY) || null; } catch (e) { return null; }
}
export function clearSession() {
	try {
		uni.removeStorageSync(TOKEN_KEY);
		uni.removeStorageSync(USER_KEY);
	} catch (e) {}
}
