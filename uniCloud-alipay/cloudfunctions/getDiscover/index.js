/**
 * 云函数 getDiscover —— 发现页列表（分页/筛选/排序）
 * ------------------------------------------------------------------
 * 集合：discover_items（字段见 database/README.md）
 * 集合为空时用内嵌种子数据兜底。
 *
 * 统一分类体系（全站唯一口径）：
 *   tab 0 找搭子   chips: 全部 / 学习 / 运动 / 娱乐
 *   tab 1 校园活动 chips: 全部 / 文体赛事 / 社团招新 / 讲座展览
 *   tab 2 互帮互助 chips: 全部 / 跑腿代办 / 二手闲置 / 拼车同行 / 其他求助
 *   （即时跑腿单在跑腿大厅 errand-hall，互帮互助 tab 是泛求助与长尾需求）
 *
 * 筛选入参：cat = chip 文案（推荐）；兼容旧 filter 下标。
 * 旧数据 category 自动映射：跑腿→跑腿代办 / 社团→社团招新 / 活动→文体赛事 / 生活→其他求助。
 */
'use strict';

const PURPLE = { bar: '#805CFA', barSoft: 'rgba(128,92,250,.10)', bg: 'linear-gradient(135deg,#805CFA,#A98BFF)' };
const GREEN = { bar: '#29CA83', barSoft: 'rgba(41,202,131,.10)', bg: 'linear-gradient(135deg,#29CA83,#93EDCF)' };
const SUN = { bar: '#FFB020', barSoft: 'rgba(255,176,32,.14)', bg: 'linear-gradient(135deg,#FFC94F,#FFE39B)' };
const SKY = { bar: '#69B9F5', barSoft: 'rgba(105,185,245,.12)', bg: 'linear-gradient(135deg,#69B9F5,#B9E2FB)' };

const ARTDIR = '/static/art/';

const SEED = [
	// ═══ tab 0 找搭子：学习 / 运动 / 娱乐 ═══
	{ id: 'd1', tab: 0, category: '学习', hot: true, title: '一起准备英语四级 · 每日打卡互相监督', cover: ARTDIR + 'art-campus.jpg', time: '每天 20:00', place: '图书馆 4F', joined: 12, total: 20, price: '免费', members: [{ ch: '星', bg: PURPLE.bg }, { ch: '林', bg: GREEN.bg }, { ch: 'Y', bg: SKY.bg }], ...PURPLE },
	{ id: 'd2', tab: 0, category: '运动', hot: true, title: '周末爬山 · 登顶看日出，缺 4 人', cover: ARTDIR + 'art-cheer.jpg', time: '周日 05:30', place: '南山公园', joined: 6, total: 10, price: 'AA', members: [{ ch: '陈', bg: SKY.bg }, { ch: '周', bg: PURPLE.bg }], ...GREEN },
	{ id: 'd3', tab: 0, category: '运动', hot: false, title: '羽毛球双打 · 缺 1 人，水平不限', cover: ARTDIR + 'art-tennis.jpg', time: '今晚 20:00', place: '体育馆 3 号场', joined: 3, total: 4, price: '免费', members: [{ ch: '林', bg: GREEN.bg }, { ch: '苏', bg: PURPLE.bg }, { ch: 'Q', bg: SUN.bg }], ...SKY },
	{ id: 'd5', tab: 0, category: '娱乐', hot: false, title: '找周末探店搭子 · 新开的烤肉店', cover: ARTDIR + 'art-guitar.jpg', time: '周六 18:00', place: '大学城', joined: 2, total: 6, price: 'AA', members: [{ ch: '安', bg: SUN.bg }], ...PURPLE },
	{ id: 'd6', tab: 0, category: '学习', hot: false, title: 'PS 技能速成 · 1v1 教学，包教会', cover: ARTDIR + 'art-campus.jpg', time: '预约时间', place: '线上 / 面授', joined: 3, total: 5, price: '¥50', members: [{ ch: '苏', bg: PURPLE.bg }, { ch: 'Y', bg: SKY.bg }], ...GREEN },
	// ═══ tab 1 校园活动：文体赛事 / 社团招新 / 讲座展览 ═══
	{ id: 'd7', tab: 1, category: '文体赛事', hot: true, title: '校园音乐节 · 夏夜草坪摇滚专场', cover: ARTDIR + 'art-guitar.jpg', time: '周六 19:00', place: '中心草坪', joined: 128, total: 300, price: '免费', members: [{ ch: '音', bg: PURPLE.bg }, { ch: '乐', bg: SUN.bg }], ...SUN },
	{ id: 'd8', tab: 1, category: '文体赛事', hot: false, title: '三人篮球赛 · 院系对抗报名中', cover: ARTDIR + 'art-balls.jpg', time: '周日 15:00', place: '东区篮球场', joined: 24, total: 48, price: '免费', members: [{ ch: '篮', bg: GREEN.bg }, { ch: '陈', bg: SKY.bg }], ...GREEN },
	{ id: 'd9', tab: 1, category: '讲座展览', hot: false, title: '秋日校园摄影大赛 · 线上投稿', cover: ARTDIR + 'art-campus.jpg', time: '10.28 截止', place: '线上', joined: 213, total: 500, price: '免费', members: [{ ch: '摄', bg: PURPLE.bg }], ...PURPLE },
	{ id: 'd10', tab: 1, category: '社团招新', hot: true, title: '街舞社招新 · 零基础也能加入', cover: ARTDIR + 'art-cheer.jpg', time: '周四 12:00', place: '中心广场', joined: 56, total: 100, price: '免费', members: [{ ch: '舞', bg: PURPLE.bg }, { ch: '林', bg: SUN.bg }], ...PURPLE },
	{ id: 'd11', tab: 1, category: '社团招新', hot: false, title: '志愿者协会招新 · 一起做有意义的事', cover: ARTDIR + 'art-campus.jpg', time: '本周摆摊', place: '中心广场', joined: 34, total: 80, price: '免费', members: [{ ch: '志', bg: GREEN.bg }], ...GREEN },
	{ id: 'd12', tab: 1, category: '社团招新', hot: false, title: '动漫社同人展 · 招新 + 作品征集', cover: ARTDIR + 'art-guitar.jpg', time: '11.02 全天', place: '艺术楼', joined: 88, total: 150, price: '免费', members: [{ ch: '漫', bg: SKY.bg }, { ch: 'Q', bg: SUN.bg }], ...SKY },
	// ═══ tab 2 互帮互助：跑腿代办 / 二手闲置 / 拼车同行 / 其他求助 ═══
	{ id: 'd4', tab: 2, category: '跑腿代办', hot: false, title: '代取外卖到宿舍楼下 · 东门出发', cover: ARTDIR + 'art-balls.jpg', time: '即时', place: '东门驿站', joined: 0, total: 1, price: '¥4', members: [], ...SUN },
	{ id: 'd13', tab: 2, category: '二手闲置', hot: false, title: '出一辆九成新自行车 · 宿舍自提', cover: ARTDIR + 'art-cheer.jpg', time: '随时', place: '东园 3 栋', joined: 1, total: 1, price: '¥180', members: [], ...GREEN },
	{ id: 'd14', tab: 2, category: '拼车同行', hot: true, title: '周五下午拼车去高铁站 · 缺 2 人', cover: ARTDIR + 'art-campus.jpg', time: '周五 14:00', place: '校门口集合', joined: 2, total: 4, price: 'AA', members: [{ ch: '舟', bg: SKY.bg }], ...SKY },
	{ id: 'd15', tab: 2, category: '其他求助', hot: false, title: '找同学帮忙搬书去新宿舍 · 一小时', cover: ARTDIR + 'art-tennis.jpg', time: '明天上午', place: '南园 5 栋', joined: 0, total: 2, price: '请奶茶', members: [], ...PURPLE }
];

// 每个 tab 的 chip 下标 → 分类名（兼容旧入参 filter）
const FILTERS = {
	0: { 1: '学习', 2: '运动', 3: '娱乐' },
	1: { 1: '文体赛事', 2: '社团招新', 3: '讲座展览' },
	2: { 1: '跑腿代办', 2: '二手闲置', 3: '拼车同行', 4: '其他求助' }
};

// 旧分类名 → 新分类名（用户已发布数据兼容）
const LEGACY = { '跑腿': '跑腿代办', '社团': '社团招新', '活动': '文体赛事', '生活': '其他求助', '互助': '其他求助' };

function normCat(c) {
	if (!c) return '';
	return LEGACY[c] || c;
}

exports.main = async (event) => {
	const tab = Number(event.tab) || 0;
	const sort = Number(event.sort) || 0;
	const page = Number(event.page) || 1;
	const size = Number(event.size) || 6;

	// 筛选分类：优先 cat 文案；兼容旧 filter 下标
	let cat = String(event.cat || '').trim();
	if (!cat && Number(event.filter) > 0) {
		cat = (FILTERS[tab] || {})[Number(event.filter)] || '';
	}

	try {
		const db = uniCloud.database();
		let all = null;
		let fromDB = false;
		try {
			const res = await db.collection('discover_items').limit(200).get();
			if (res.data && res.data.length) {
				all = res.data.map((x) => { const o = { ...x }; delete o._id; return o; });
				fromDB = true;
			}
		} catch (e) {
			console.warn('discover_items 读取失败:', e.message);
		}
		if (!all) all = SEED;

		// 旧数据分类名归一化
		all = all.map((d) => ({ ...d, category: normCat(d.category) }));

		let list = all.filter((d) => Number(d.tab) === tab);
		if (cat) list = list.filter((d) => d.category === cat);

		if (sort === 1) {
			list = list.slice().sort((a, b) => Number(String(b.id).slice(1)) - Number(String(a.id).slice(1)));
		} else if (sort === 2) {
			list = list.slice().sort((a, b) => {
				const ra = a.joined / a.total, rb = b.joined / b.total;
				return rb - ra || b.joined - a.joined;
			});
		}

		const start = (page - 1) * size;
		const pageList = list.slice(start, start + size);
		return {
			errCode: 0,
			list: pageList,
			hasMore: start + pageList.length < list.length,
			total: list.length,
			_source: { fromDB }
		};
	} catch (e) {
		console.error('getDiscover error:', e);
		return { errCode: 2, errMsg: e.message || '获取发现列表失败' };
	}
};
