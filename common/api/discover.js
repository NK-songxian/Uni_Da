import { CLOUD_MODE, callCloud } from '@/common/cloud.js';

/**
 * 发现页数据接口  common/api/discover.js
 * ------------------------------------------------------------------
 * 双模式：CLOUD_MODE.enabled=true 走云函数，false 走本地 mock。
 * 云函数失败自动回退 mock，页面代码无需改动。
 *
 * 统一分类体系（全站唯一口径，与首页入口/发布页/跑腿大厅对齐）：
 *   tab 0 找搭子   chips: 全部 / 学习 / 运动 / 娱乐
 *   tab 1 校园活动 chips: 全部 / 文体赛事 / 社团招新 / 讲座展览
 *   tab 2 互帮互助 chips: 全部 / 跑腿代办 / 二手闲置 / 拼车同行 / 其他求助
 *   （即时跑腿单在跑腿大厅，互帮互助 tab 是泛求助与长尾需求）
 */

const ART = '/static/art/';

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

let mockFail = false;
export function setDiscoverFail(v) {
	mockFail = v;
}

// 三大主 tab（页面直接引用，避免两处维护）；filters 为每个 tab 自己的筛选 chip
export const DISCOVER_TABS = [
	{ label: '找搭子', icon: '/static/unida/msg/ico-chat.webp', key: 'buddy', filters: ['全部', '学习', '运动', '娱乐'] },
	{ label: '校园活动', icon: '/static/unida/msg/ico-calendar.webp', key: 'act', filters: ['全部', '文体赛事', '社团招新', '讲座展览'] },
	{ label: '互帮互助', icon: '/static/unida/msg/ico-bag.webp', key: 'help', filters: ['全部', '跑腿代办', '二手闲置', '拼车同行', '其他求助'] }
];

// 排序方式
export const DISCOVER_SORTS = ['综合', '最新', '最热'];

const PURPLE = { bar: '#805CFA', barSoft: 'rgba(128,92,250,.10)', bg: 'linear-gradient(135deg,#805CFA,#A98BFF)' };
const GREEN = { bar: '#29CA83', barSoft: 'rgba(41,202,131,.10)', bg: 'linear-gradient(135deg,#29CA83,#93EDCF)' };
const SUN = { bar: '#FFB020', barSoft: 'rgba(255,176,32,.14)', bg: 'linear-gradient(135deg,#FFC94F,#FFE39B)' };
const SKY = { bar: '#69B9F5', barSoft: 'rgba(105,185,245,.12)', bg: 'linear-gradient(135deg,#69B9F5,#B9E2FB)' };

const POOL = [
	// ═══ tab 0 找搭子 ═══
	{
		id: 'd1', tab: 0, hot: true,
		title: '一起准备英语四级 · 每日打卡互相监督',
		cover: ART + 'art-campus.jpg', category: '学习', time: '每天 20:00', place: '图书馆 4F',
		joined: 12, total: 20, price: '免费',
		members: [{ ch: '星', bg: PURPLE.bg }, { ch: '林', bg: GREEN.bg }, { ch: 'Y', bg: SKY.bg }],
		...PURPLE
	},
	{
		id: 'd2', tab: 0, hot: true,
		title: '周末爬山 · 登顶看日出，缺 4 人',
		cover: ART + 'art-cheer.jpg', category: '运动', time: '周日 05:30', place: '南山公园',
		joined: 6, total: 10, price: 'AA',
		members: [{ ch: '陈', bg: SKY.bg }, { ch: '周', bg: PURPLE.bg }],
		...GREEN
	},
	{
		id: 'd3', tab: 0, hot: false,
		title: '羽毛球双打 · 缺 1 人，水平不限',
		cover: ART + 'art-tennis.jpg', category: '运动', time: '今晚 20:00', place: '体育馆 3 号场',
		joined: 3, total: 4, price: '免费',
		members: [{ ch: '林', bg: GREEN.bg }, { ch: '苏', bg: PURPLE.bg }, { ch: 'Q', bg: SUN.bg }],
		...SKY
	},
	{
		id: 'd5', tab: 0, hot: false,
		title: '找周末探店搭子 · 新开的烤肉店',
		cover: ART + 'art-guitar.jpg', category: '娱乐', time: '周六 18:00', place: '大学城',
		joined: 2, total: 6, price: 'AA',
		members: [{ ch: '安', bg: SUN.bg }],
		...PURPLE
	},
	{
		id: 'd6', tab: 0, hot: false,
		title: 'PS 技能速成 · 1v1 教学，包教会',
		cover: ART + 'art-campus.jpg', category: '学习', time: '预约时间', place: '线上 / 面授',
		joined: 3, total: 5, price: '¥50',
		members: [{ ch: '苏', bg: PURPLE.bg }, { ch: 'Y', bg: SKY.bg }],
		...GREEN
	},
	// ═══ tab 1 校园活动 ═══
	{
		id: 'd7', tab: 1, hot: true,
		title: '校园音乐节 · 夏夜草坪摇滚专场',
		cover: ART + 'art-guitar.jpg', category: '文体赛事', time: '周六 19:00', place: '中心草坪',
		joined: 128, total: 300, price: '免费',
		members: [{ ch: '音', bg: PURPLE.bg }, { ch: '乐', bg: SUN.bg }],
		...SUN
	},
	{
		id: 'd8', tab: 1, hot: false,
		title: '三人篮球赛 · 院系对抗报名中',
		cover: ART + 'art-balls.jpg', category: '文体赛事', time: '周日 15:00', place: '东区篮球场',
		joined: 24, total: 48, price: '免费',
		members: [{ ch: '篮', bg: GREEN.bg }, { ch: '陈', bg: SKY.bg }],
		...GREEN
	},
	{
		id: 'd9', tab: 1, hot: false,
		title: '秋日校园摄影大赛 · 线上投稿',
		cover: ART + 'art-campus.jpg', category: '讲座展览', time: '10.28 截止', place: '线上',
		joined: 213, total: 500, price: '免费',
		members: [{ ch: '摄', bg: PURPLE.bg }],
		...PURPLE
	},
	{
		id: 'd10', tab: 1, hot: true,
		title: '街舞社招新 · 零基础也能加入',
		cover: ART + 'art-cheer.jpg', category: '社团招新', time: '周四 12:00', place: '中心广场',
		joined: 56, total: 100, price: '免费',
		members: [{ ch: '舞', bg: PURPLE.bg }, { ch: '林', bg: SUN.bg }],
		...PURPLE
	},
	{
		id: 'd11', tab: 1, hot: false,
		title: '志愿者协会招新 · 一起做有意义的事',
		cover: ART + 'art-campus.jpg', category: '社团招新', time: '本周摆摊', place: '中心广场',
		joined: 34, total: 80, price: '免费',
		members: [{ ch: '志', bg: GREEN.bg }],
		...GREEN
	},
	{
		id: 'd12', tab: 1, hot: false,
		title: '动漫社同人展 · 招新 + 作品征集',
		cover: ART + 'art-guitar.jpg', category: '社团招新', time: '11.02 全天', place: '艺术楼',
		joined: 88, total: 150, price: '免费',
		members: [{ ch: '漫', bg: SKY.bg }, { ch: 'Q', bg: SUN.bg }],
		...SKY
	},
	// ═══ tab 2 互帮互助 ═══
	{
		id: 'd4', tab: 2, hot: false,
		title: '代取外卖到宿舍楼下 · 东门出发',
		cover: ART + 'art-balls.jpg', category: '跑腿代办', time: '即时', place: '东门驿站',
		joined: 0, total: 1, price: '¥4',
		members: [],
		...SUN
	},
	{
		id: 'd13', tab: 2, hot: false,
		title: '出一辆九成新自行车 · 宿舍自提',
		cover: ART + 'art-cheer.jpg', category: '二手闲置', time: '随时', place: '东园 3 栋',
		joined: 1, total: 1, price: '¥180',
		members: [],
		...GREEN
	},
	{
		id: 'd14', tab: 2, hot: true,
		title: '周五下午拼车去高铁站 · 缺 2 人',
		cover: ART + 'art-campus.jpg', category: '拼车同行', time: '周五 14:00', place: '校门口集合',
		joined: 2, total: 4, price: 'AA',
		members: [{ ch: '舟', bg: SKY.bg }],
		...SKY
	},
	{
		id: 'd15', tab: 2, hot: false,
		title: '找同学帮忙搬书去新宿舍 · 一小时',
		cover: ART + 'art-tennis.jpg', category: '其他求助', time: '明天上午', place: '南园 5 栋',
		joined: 0, total: 2, price: '请奶茶',
		members: [],
		...PURPLE
	}
];

/**
 * @param {Object} opt { tab, chip, sort, page, size }
 *   tab    0 找搭子 / 1 校园活动 / 2 互帮互助
 *   chip   筛选分类文案（'全部' 或具体分类名），按 category 精确匹配
 *   sort   DISCOVER_SORTS 下标，0 综合 / 1 最新 / 2 最热
 * @returns {{ list, hasMore, total }}
 */
export async function fetchDiscover(opt = {}) {
	const tab = opt.tab || 0;
	const chip = opt.chip || '全部';
	const sort = opt.sort || 0;
	const page = opt.page || 1;
	const size = opt.size || 6;

	if (CLOUD_MODE.enabled) {
		try {
			const r = await callCloud('getDiscover', { tab, cat: chip === '全部' ? '' : chip, sort, page, size });
			return { list: r.list, hasMore: r.hasMore, total: r.total };
		} catch (e) {
			console.warn('[discover] 云函数失败，回退 mock：', e.message);
		}
	}

	await delay(420);
	if (mockFail) throw new Error('NETWORK');

	let list = POOL.filter((d) => d.tab === tab);
	if (chip !== '全部') list = list.filter((d) => d.category === chip);

	// 排序：发现页独有的深度检索能力
	if (sort === 1) {
		list = list.slice().sort((a, b) => Number(b.id.slice(1)) - Number(a.id.slice(1)));
	} else if (sort === 2) {
		list = list.slice().sort((a, b) => {
			const ra = a.joined / a.total, rb = b.joined / b.total;
			return rb - ra || b.joined - a.joined;
		});
	}

	const start = (page - 1) * size;
	const pageList = list.slice(start, start + size);
	return {
		list: JSON.parse(JSON.stringify(pageList)),
		hasMore: start + pageList.length < list.length,
		total: list.length
	};
}
