/**
 * 云存储上传工具（支付宝云空间）
 * ------------------------------------------------------------------
 * 支付宝云 uploadFile 返回 cloud:// 格式 fileID，image 组件无法直接显示，
 * 统一走 getTempFileURL 转 https 公网链接（公共权限下永久有效，可直接入库）。
 */

function randName(ext) {
	return Date.now() + '_' + Math.floor(Math.random() * 9000 + 1000) + '.' + (ext || 'jpg');
}

function guessExt(path) {
	const m = /\.([a-zA-Z0-9]+)$/.exec(String(path || ''));
	const e = m && m[1].toLowerCase();
	if (e && e.length <= 5 && e !== 'temp') return e;
	return 'jpg';
}

/** 上传单张 → 返回 https 链接（失败抛错） */
export async function uploadImage(filePath, folder) {
	if (!filePath) throw new Error('缺少文件路径');
	const cloudPath = (folder || 'upload') + '/' + randName(guessExt(filePath));
	const up = await uniCloud.uploadFile({
		filePath,
		cloudPath,
		fileType: 'image'
	});
	if (!up || !up.fileID) throw new Error('上传失败，请重试');
	const t = await uniCloud.getTempFileURL({ fileList: [up.fileID] });
	const item = t && t.fileList && t.fileList[0];
	const url = item && item.tempFileURL;
	if (!url) throw new Error('获取图片链接失败');
	return url;
}

/** 批量上传（串行，逐张回报进度），返回 https 链接数组 */
export async function uploadImages(paths, folder, onProgress) {
	const urls = [];
	for (let i = 0; i < (paths || []).length; i++) {
		if (onProgress) onProgress(i, paths.length);
		urls.push(await uploadImage(paths[i], folder));
	}
	return urls;
}
