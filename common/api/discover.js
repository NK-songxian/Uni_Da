import { CLOUD_MODE, callCloud } from '@/common/cloud.js';

/**
 * 发现页数据接口  common/api/discover.js
 * ------------------------------------------------------------------
 * 双模式：CLOUD_MODE.enabled=true 走云函数，false 走本地 mock。
 * 云函数失败自动回退 mock，页面代码无需改动。
 */

const ART = '/static/art/';
const U = '/static/unida/illustrations/';

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

let mockFail = false;
export function setDiscoverFail(v) {
	mockFail = v;
}

// 筛选 chip（页面直接引用，避免两处维护）
export const DISCOVER_FILTERS = ['全部', '学习', '运动', '娱乐', '生活', '社团', '跑腿'];
// 排序方式（首页没有的深度检索能力，与首页推荐流去重）
export const DISCOVER_SORTS = ['综合', '最新', '最热'];
// chip 下标 → 分类名。按 category 匹配，不再依赖数据里易错的下标字段
const FILTER_CATEGORY = { 1: '学习', 2: '运动', 3: '娱乐', 4: '生活', 5: '社团', 6: '跑腿' };

const PURPLE = { bar: '#805CFA', barSoft: 'rgba(128,92,250,.10)', bg: 'linear-gradient(135deg,#805CFA,#A98BFF)' };
const GREEN = { bar: '#29CA83', barSoft: 'rgba(41,202,131,.10)', bg: 'linear-gradient(135deg,#29CA83,#93EDCF)' };
const SUN = { bar: '#FFB020', barSoft: 'rgba(255,176,32,.14)', bg: 'linear-gradient(135deg,#FFC94F,#FFE39B)' };
const SKY = { bar: '#69B9F5', barSoft: 'rgba(105,185,245,.12)', bg: 'linear-gradient(135deg,#69B9F5,#B9E2FB)' };

/**
 * tab: 0 找搭子 / 1 校园活动 / 2 社团招新
 * filter: DISCOVER_FILTERS 下标
 */
const POOL = [
	{
		id: 'd1', tab: 0, filter: 1, hot: true,
		title: '一起准备英语四级 · 每日打卡互相监督',
		cover: ART + 'art-campus.jpg', category: '学习', time: '每天 20:00', place: '图书馆 4F',
		joined: 12, total: 20, price: '免费',
		members: [{ ch: '星', bg: PURPLE.bg }, { ch: '林', bg: GREEN.bg }, { ch: 'Y', bg: SKY.bg }],
		...PURPLE
	},
	{
		id: 'd2', tab: 0, filter: 2, hot: true,
		title: '周末爬山 · 登顶看日出，缺 4 人',
		cover: ART + 'art-cheer.jpg', category: '运动', time: '周日 05:30', place: '南山公园',
		joined: 6, total: 10, price: 'AA',
		members: [{ ch: '陈', bg: SKY.bg }, { ch: '周', bg: PURPLE.bg }],
		...GREEN
	},
	{
		id: 'd3', tab: 0, filter: 3, hot: false,
		title: '羽毛球双打 · 缺 1 人，水平不限',
		cover: ART + 'art-tennis.jpg', category: '运动', time: '今晚 20:00', place: '体育馆 3 号场',
		joined: 3, total: 4, price: '免费',
		members: [{ ch: '林', bg: GREEN.bg }, { ch: '苏', bg: PURPLE.bg }, { ch: 'Q', bg: SUN.bg }],
		...SKY
	},
	{
		id: 'd4', tab: 0, filter: 4, hot: false,
		title: '代取外卖到宿舍楼下 · 东门出发',
		cover: ART + 'art-balls.jpg', category: '跑腿', time: '即时', place: '东门驿站',
		joined: 0, total: 1, price: '¥4',
		members: [],
		...SUN
	},
	{
		id: 'd5', tab: 0, filter: 5, hot: false,
		title: '找周末探店搭子 · 新开的烤肉店',
		cover: ART + 'art-guitar.jpg', category: '娱乐', time: '周六 18:00', place: '大学城',
		joined: 2, total: 6, price: 'AA',
		members: [{ ch: '安', bg: SUN.bg }],
		...PURPLE
	},
	{
		id: 'd6', tab: 0, filter: 4, hot: false,
		title: 'PS 技能速成 · 1v1 教学，包教会',
		cover: ART + 'art-campus.jpg', category: '学习', time: '预约时间', place: '线上 / 面授',
		joined: 3, total: 5, price: '¥50',
		members: [{ ch: '苏', bg: PURPLE.bg }, { ch: 'Y', bg: SKY.bg }],
		...GREEN
	},
	{
		id: 'd7', tab: 1, filter: 0, hot: true,
		title: '校园音乐节 · 夏夜草坪摇滚专场',
		cover: ART + 'art-guitar.jpg', category: '活动', time: '周六 19:00', place: '中心草坪',
		joined: 128, total: 300, price: '免费',
		members: [{ ch: '音', bg: PURPLE.bg }, { ch: '乐', bg: SUN.bg }],
		...SUN
	},
	{
		id: 'd8', tab: 1, filter: 2, hot: false,
		title: '三人篮球赛 · 院系对抗报名中',
		cover: ART + 'art-balls.jpg', category: '活动', time: '周日 15:00', place: '东区篮球场',
		joined: 24, total: 48, price: '免费',
		members: [{ ch: '篮', bg: GREEN.bg }, { ch: '陈', bg: SKY.bg }],
		...GREEN
	},
	{
		id: 'd9', tab: 1, filter: 3, hot: false,
		title: '秋日校园摄影大赛 · 线上投稿',
		cover: ART + 'art-campus.jpg', category: '活动', time: '10.28 截止', place: '线上',
		joined: 213, total: 500, price: '免费',
		members: [{ ch: '摄', bg: PURPLE.bg }],
		...PURPLE
	},
	{
		id: 'd10', tab: 2, filter: 5, hot: true,
		title: '街舞社招新 · 零基础也能加入',
		cover: ART + 'art-cheer.jpg', category: '社团', time: '周四 12:00', place: '中心广场',
		joined: 56, total: 100, price: '免费',
		members: [{ ch: '舞', bg: PURPLE.bg }, { ch: '林', bg: SUN.bg }],
		...PURPLE
	},
	{
		id: 'd11', tab: 2, filter: 1, hot: false,
		title: '志愿者协会招新 · 一起做有意义的事',
		cover: ART + 'art-campus.jpg', category: '社团', time: '本周摆摊', place: '中心广场',
		joined: 34, total: 80, price: '免费',
		members: [{ ch: '志', bg: GREEN.bg }],
		...GREEN
	},
	{
		id: 'd12', tab: 2, filter: 3, hot: false,
		title: '动漫社同人展 · 招新 + 作品征集',
		cover: ART + 'art-guitar.jpg', category: '社团', time: '11.02 全天', place: '艺术楼',
		joined: 88, total: 150, price: '免费',
		members: [{ ch: '漫', bg: SKY.bg }, { ch: 'Q', bg: SUN.bg }],
		...SKY
	}
];

/**
 * @param {Object} opt { tab, filter, sort, page, size }
 *   tab    0 找搭子 / 1 校园活动 / 2 社团招新
 *   filter DISCOVER_FILTERS 下标，0=全部
 *   sort   DISCOVER_SORTS 下标，0 综合 / 1 最新 / 2 最热
 * @returns {{ list, hasMore, total }}
 */
export async function fetchDiscover(opt = {}) {
	const tab = opt.tab || 0;
	const filter = opt.filter || 0;
	const sort = opt.sort || 0;
	const page = opt.page || 1;
	const size = opt.size || 6;

	if (CLOUD_MODE.enabled) {
		try {
			const r = await callCloud('getDiscover', { tab, filter, sort, page, size });
			return { list: r.list, hasMore: r.hasMore, total: r.total };
		} catch (e) {
			console.warn('[discover] 云函数失败，回退 mock：', e.message);
		}
	}

	await delay(420);
	if (mockFail) throw new Error('NETWORK');

	let list = POOL.filter((d) => d.tab === tab);
	// 按分类名匹配，彻底避免下标错位（原数据 filter 字段与 chip 对不上）
	const cat = FILTER_CATEGORY[filter];
	if (cat) list = list.filter((d) => d.category === cat);

	// 排序：发现页独有的深度检索能力
	if (sort === 1) {
		// 最新：POOL 里 id 越大越新（d12 > d1）
		list = list.slice().sort((a, b) => Number(b.id.slice(1)) - Number(a.id.slice(1)));
	} else if (sort === 2) {
		// 最热：报名比例优先，同比例看报名人数
		list = list.slice().sort((a, b) => {
			const ra = a.joined / a.total, rb = b.joined / b.total;
			return rb - ra || b.joined - a.joined;
		});
	}
	// sort=0 综合：保留 POOL 原始顺序（热门优先已体现在数据排列里）

	const start = (page - 1) * size;
	const pageList = list.slice(start, start + size);
	return {
		list: JSON.parse(JSON.stringify(pageList)),
		hasMore: start + pageList.length < list.length,
		total: list.length
	};
}
