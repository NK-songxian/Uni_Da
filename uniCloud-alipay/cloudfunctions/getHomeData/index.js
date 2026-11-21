/**
 * 云函数 getHomeData —— 首页概览 + 同校动态
 * ------------------------------------------------------------------
 * 数据策略：
 *   1. 若数据库集合有数据 → 从数据库读（真实数据）
 *   2. 若集合为空 → 用内嵌种子数据兜底（未导入数据时也能跑通）
 *
 * 集合：home_categories / home_promos / activities / users(作为 mates) / feed
 */
'use strict';

// ── 种子数据（与源码 mock 一致，导入数据库后可删） ──
const SEED = {
	school: '江南大学',
	todayJoin: '1,284',
	cats: [
		{ label: '学习组队', icon: '/static/unida/msg/ico-book.webp', key: 'study', tint: 'rgba(128,92,250,.10)', order: 1 },
		{ label: '运动搭子', icon: '/static/unida/msg/ico-run.webp', key: 'sport', tint: 'rgba(41,202,131,.10)', order: 2 },
		{ label: '校园活动', icon: '/static/unida/msg/ico-calendar.webp', key: 'activity', tint: 'rgba(255,201,79,.16)', order: 3 },
		{ label: '生活互助', icon: '/static/unida/msg/ico-bag.webp', key: 'help', tint: 'rgba(128,92,250,.09)', order: 4 },
		{ label: '社团招新', icon: '/static/unida/msg/ico-megaphone.webp', key: 'club', tint: 'rgba(105,185,245,.11)', order: 5 },
		{ label: '同校广场', icon: '/static/unida/msg/ico-bubble.webp', key: 'square', tint: 'rgba(169,139,255,.14)', order: 6 }
	],
	promos: [
		{ id: 'promo-1', tag: '校园推广', title: '图书馆自习搭子招募', desc: '发布即得 200 积分 · 今日剩 3 席', point: '200', bg: 'linear-gradient(135deg, #EFE7FF 0%, #F6EEFF 100%)', tagBg: 'linear-gradient(135deg, #9B7BFF, #6C3FF2)', order: 1 },
		{ id: 'promo-2', tag: '优质任务', title: '社团招新 · 校园推广大使', desc: '完成打卡额外奖励 · 长期有效', point: '500', bg: 'linear-gradient(135deg, #E4F8EF 0%, #F0FBF5 100%)', tagBg: 'linear-gradient(135deg, #4FD89A, #29CA83)', order: 2 },
		{ id: 'promo-3', tag: '限时任务', title: '帮取快递 · 顺路互助', desc: '今晚 22:00 前完成 · 先到先得', point: '120', bg: 'linear-gradient(135deg, #FFF3DC 0%, #FFFAEE 100%)', tagBg: 'linear-gradient(135deg, #FFD76A, #FFB020)', order: 3 }
	],
	nowList: [
		{ id: 'n1', title: '周五夜跑 · 环湖 5 公里', cover: '/static/art/art-cheer.jpg', left: '40 分钟后', time: '19:30', place: '中心湖广场', joined: 3, total: 8, members: [{ ch: '星', bg: 'linear-gradient(135deg,#805CFA,#A98BFF)' }, { ch: '林', bg: 'linear-gradient(135deg,#29CA83,#93EDCF)' }, { ch: 'L', bg: 'linear-gradient(135deg,#FFC94F,#FFE39B)' }] },
		{ id: 'n2', title: '羽毛球双打，缺 1 人', cover: '/static/art/art-tennis.jpg', left: '1 小时后', time: '20:00', place: '体育馆 3 号场', joined: 3, total: 4, members: [{ ch: '陈', bg: 'linear-gradient(135deg,#69B9F5,#B9E2FB)' }, { ch: '周', bg: 'linear-gradient(135deg,#805CFA,#A98BFF)' }, { ch: 'Q', bg: 'linear-gradient(135deg,#FF9B77,#FFCDBB)' }] },
		{ id: 'n3', title: '图书馆四楼 · 期末自习', cover: '/static/art/art-balls.jpg', left: '现在', time: '即刻', place: '图书馆 4F', joined: 5, total: 6, members: [{ ch: '苏', bg: 'linear-gradient(135deg,#542DAF,#805CFA)' }, { ch: 'Y', bg: 'linear-gradient(135deg,#29CA83,#93EDCF)' }] },
		{ id: 'n4', title: '吉他速成 30 分钟', cover: '/static/art/art-guitar.jpg', left: '今晚 20:00', time: '20:00', place: '艺术楼 201', joined: 2, total: 5, members: [{ ch: '安', bg: 'linear-gradient(135deg,#FF9B77,#FFC94F)' }] }
	],
	acts: [
		{ id: 'a1', title: '校园音乐节 · 夏夜草坪', cover: '/static/art/art-guitar.jpg', time: '周六 19:00', place: '中心草坪', host: '校学生会', joined: 128, flag: '即将开始', tone: 'sun' },
		{ id: 'a2', title: '三人篮球赛 · 院系对抗', cover: '/static/art/art-cheer.jpg', time: '周日 15:00', place: '东区篮球场', host: '体育部', joined: 64, flag: '报名中', tone: 'mint' },
		{ id: 'a3', title: '秋日校园摄影大赛', cover: '/static/art/art-campus.jpg', time: '10.28 截止', place: '线上投稿', host: '摄影社', joined: 213, flag: '征集中', tone: 'purple' }
	],
	mates: [
		{ id: 'm1', name: '苏叶', ch: '苏', college: '数媒 · 大二', online: true, tags: ['羽毛球', '摄影'], bg: 'linear-gradient(135deg,#805CFA,#A98BFF)' },
		{ id: 'm2', name: '陈一鸣', ch: '陈', college: '机械 · 大三', online: true, tags: ['夜跑', '吉他'], bg: 'linear-gradient(135deg,#29CA83,#93EDCF)' },
		{ id: 'm3', name: '周可以把', ch: '周', college: '新闻 · 大一', online: false, tags: ['探店', '电影'], bg: 'linear-gradient(135deg,#FF9B77,#FFC94F)' },
		{ id: 'm4', name: 'Yuki', ch: 'Y', college: '英语 · 大四', online: true, tags: ['自习', '旅行'], bg: 'linear-gradient(135deg,#69B9F5,#B9E2FB)' },
		{ id: 'm5', name: '安琪', ch: '安', college: '音乐 · 大二', online: false, tags: ['合唱', '咖啡'], bg: 'linear-gradient(135deg,#542DAF,#805CFA)' }
	]
};

const clean = (arr) => (arr || []).map((x) => {
	const o = { ...x };
	delete o._id;
	delete o.createdAt;
	delete o.updatedAt;
	return o;
});

/** 安全读取集合：集合不存在或为空时返回 null */
async function readCol(db, name, orderBy) {
	try {
		let q = db.collection(name);
		if (orderBy) q = q.orderBy(orderBy, 'asc');
		const res = await q.limit(100).get();
		return res.data && res.data.length ? clean(res.data) : null;
	} catch (e) {
		console.warn('read ' + name + ' failed:', e.message);
		return null;
	}
}

exports.main = async (event) => {
	const db = uniCloud.database();
	const type = event.type || 'overview'; // overview | feed
	const source = { fromDB: false };

	try {
		if (type === 'overview') {
			const cats = await readCol(db, 'home_categories', 'order') || SEED.cats;
			const promos = await readCol(db, 'home_promos', 'order') || SEED.promos;
			const nowList = await readCol(db, 'activities', 'order') || SEED.nowList;
			const acts = await readCol(db, 'home_acts', 'order') || SEED.acts;
			const mates = await readCol(db, 'mates', 'order') || SEED.mates;

			const config = await readCol(db, 'app_config');
			const school = (config && config[0] && config[0].school) || SEED.school;
			const todayJoin = (config && config[0] && config[0].todayJoin) || SEED.todayJoin;

			source.fromDB = !!(config || (await readCol(db, 'activities')));
			return {
				errCode: 0,
				school,
				todayJoin,
				cats,
				promos,
				nowList,
				acts,
				mates,
				_source: source
			};
		}

		if (type === 'feed') {
			const tab = Number(event.tab) || 0;
			const page = Number(event.page) || 1;
			const size = Number(event.size) || 3;

			let all = await readCol(db, 'feed', 'order');
			source.fromDB = !!all;
			if (!all) all = SEED.feed || [];

			// 数据库无 feed 集合时用内嵌 feed 种子
			if (!all.length) all = FEED_SEED;

			const filtered = tab === 0 ? all : all.filter((f) => Number(f.tab) === tab);
			const start = (page - 1) * size;
			const list = filtered.slice(start, start + size);
			return {
				errCode: 0,
				list,
				hasMore: start + list.length < filtered.length,
				total: filtered.length,
				_source: source
			};
		}

		return { errCode: 1, errMsg: '未知 type' };
	} catch (e) {
		console.error('getHomeData error:', e);
		return { errCode: 2, errMsg: e.message || '获取数据失败' };
	}
};

// feed 种子（独立常量，避免与主 SEED 混淆）
const FEED_SEED = [
	{ id: 'f1', user: '阿星', ch: '星', college: '计算机学院 · 大二', time: '5 分钟前', cat: '找搭子', topic: '周末探店', tab: 1, text: '有没有人一起去吃新开的烤肉店？AA 制，本周六晚，人多可以拼桌～', like: 42, cmt: 12, cover: '/static/art/art-cheer.jpg', bar: '#805CFA', barSoft: 'rgba(128,92,250,.10)', bg: 'linear-gradient(135deg,#805CFA,#A98BFF)' },
	{ id: 'f2', user: '小林同学', ch: '林', college: '设计学院 · 大一', time: '18 分钟前', cat: '校园活动', topic: '社团招新', tab: 0, text: '街舞社、动漫社、志愿者协会都在招人，周四中午在中心广场摆摊，有兴趣的来看看。', like: 128, cmt: 36, cover: '/static/art/art-guitar.jpg', bar: '#29CA83', barSoft: 'rgba(41,202,131,.10)', bg: 'linear-gradient(135deg,#29CA83,#93EDCF)' },
	{ id: 'f3', user: 'Leo', ch: 'L', college: '外国语学院 · 大三', time: '32 分钟前', cat: '求助', topic: '代取快递', tab: 2, text: '帮忙取个快递，东区驿站，酬劳 5 元，今晚之前都在图书馆，顺路的同学私我。', like: 9, cmt: 4, cover: '/static/art/art-campus.jpg', bar: '#FFC94F', barSoft: 'rgba(255,201,79,.16)', bg: 'linear-gradient(135deg,#FFC94F,#FFE39B)' },
	{ id: 'f4', user: '苏叶', ch: '苏', college: '数媒 · 大二', time: '1 小时前', cat: '找搭子', topic: '羽毛球', tab: 1, text: '周三晚上体育馆还有一块空场地，想找两个人打双打，水平不限，主要图个开心。', like: 27, cmt: 8, cover: '/static/art/art-tennis.jpg', bar: '#805CFA', barSoft: 'rgba(128,92,250,.10)', bg: 'linear-gradient(135deg,#805CFA,#A98BFF)' },
	{ id: 'f5', user: '陈一鸣', ch: '陈', college: '机械 · 大三', time: '1 小时前', cat: '出闲置', topic: '二手教材', tab: 3, text: '出一套《机械原理》和《材料力学》教材，九成新，无笔记，两本 40 带走。', like: 15, cmt: 6, cover: '/static/art/art-balls.jpg', bar: '#69B9F5', barSoft: 'rgba(105,185,245,.12)', bg: 'linear-gradient(135deg,#69B9F5,#B9E2FB)' },
	{ id: 'f6', user: '周可以把', ch: '周', college: '新闻 · 大一', time: '2 小时前', cat: '找搭子', topic: '夜跑', tab: 1, text: '想组个固定的夜跑小队，每周二四晚上八点环湖，配速 6 分半，缺两个队友。', like: 33, cmt: 11, cover: '/static/art/art-cheer.jpg', bar: '#29CA83', barSoft: 'rgba(41,202,131,.10)', bg: 'linear-gradient(135deg,#29CA83,#93EDCF)' },
	{ id: 'f7', user: 'Yuki', ch: 'Y', college: '英语 · 大四', time: '3 小时前', cat: '求助', topic: '找室友', tab: 2, text: '下个月搬去西区公寓，两室一厅，想找个作息规律的女生合租，价格好商量。', like: 21, cmt: 15, cover: '/static/art/art-campus.jpg', bar: '#FFC94F', barSoft: 'rgba(255,201,79,.16)', bg: 'linear-gradient(135deg,#FFC94F,#FFE39B)' },
	{ id: 'f8', user: '安琪', ch: '安', college: '音乐 · 大二', time: '4 小时前', cat: '校园活动', topic: '合唱团', tab: 0, text: '合唱团冬招开始啦，不需要基础，会唱就行，每周三晚排练，期末有专场演出。', like: 76, cmt: 19, cover: '/static/art/art-guitar.jpg', bar: '#805CFA', barSoft: 'rgba(128,92,250,.10)', bg: 'linear-gradient(135deg,#805CFA,#A98BFF)' },
	{ id: 'f9', user: '老赵', ch: '赵', college: '土木 · 研一', time: '5 小时前', cat: '出闲置', topic: '自行车', tab: 3, text: '毕业出一辆捷安特通勤车，骑了两年，车况良好，带锁，200 自提。', like: 18, cmt: 9, cover: '/static/art/art-balls.jpg', bar: '#69B9F5', barSoft: 'rgba(105,185,245,.12)', bg: 'linear-gradient(135deg,#69B9F5,#B9E2FB)' },
	{ id: 'f10', user: '小鹿', ch: '鹿', college: '心理 · 大二', time: '昨天', cat: '找搭子', topic: '自习搭子', tab: 1, text: '找个每天早上八点图书馆的搭子，互相监督打卡，坚持到期末就行。', like: 54, cmt: 22, cover: '/static/art/art-campus.jpg', bar: '#805CFA', barSoft: 'rgba(128,92,250,.10)', bg: 'linear-gradient(135deg,#805CFA,#A98BFF)' },
	{ id: 'f11', user: '阿哲', ch: '哲', college: '电子 · 大三', time: '昨天', cat: '求助', topic: '借设备', tab: 2, text: '想借一台示波器做课设，用两天，可以付租金，有的话评论区喊我。', like: 6, cmt: 3, cover: '/static/art/art-tennis.jpg', bar: '#FFC94F', barSoft: 'rgba(255,201,79,.16)', bg: 'linear-gradient(135deg,#FFC94F,#FFE39B)' },
	{ id: 'f12', user: '小满', ch: '满', college: '食品 · 大一', time: '前天', cat: '出闲置', topic: '宿舍好物', tab: 3, text: '出一个小台灯和一个收纳架，都是今年新买的，宿舍搬家带不走。', like: 12, cmt: 5, cover: '/static/art/art-balls.jpg', bar: '#69B9F5', barSoft: 'rgba(105,185,245,.12)', bg: 'linear-gradient(135deg,#69B9F5,#B9E2FB)' }
];
