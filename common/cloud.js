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
	enabled: false,
	// 是否打印云函数返回（调试用，生产建议关）
	debug: false
};

/** 调用云函数的统一入口 */
export function callCloud(name, data = {}) {
	if (!CLOUD_MODE.enabled) {
		return Promise.reject(new Error('CLOUD_DISABLED'));
	}
	if (CLOUD_MODE.debug) {
		console.log('[cloud] →', name, data);
	}
	// #ifdef MP-WEIXIN
	// 支付宝云 / 阿里云 / 腾讯云均为 uniCloud 标准 provider，跨端调用一致
	// #endif
	return uniCloud.callFunction({
		name,
		data
	}).then((res) => {
		const out = res && res.result;
		if (CLOUD_MODE.debug) console.log('[cloud] ←', name, out);
		if (!out || out.errCode) {
			throw new Error((out && out.errMsg) || '云函数调用失败');
		}
		return out;
	}).catch((e) => {
		if (e && e.message === 'CLOUD_DISABLED') throw e;
		console.error('[cloud] error', name, e);
		throw e;
	});
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
