<template>
	<view class="pc unida-page">
		<view class="pf-safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<view class="pc__nav">
			<view class="pc__back" @click="goBack"><image class="pc__back-img" src="/static/icons-dark/back.png" mode="aspectFit" /></view>
			<text class="pc__title">积分中心</text>
			<view class="pc__ph"></view>
		</view>

		<!-- 积分卡 -->
		<view class="pc__hero">
			<text class="pc__hero-label">我的积分</text>
			<text class="pc__hero-num">{{ pointsText }}</text>
			<view class="pc__hero-row">
				<view class="pc__hero-badge">
					<image class="pc__hero-badge-img" src="/static/unida/bubbles/label-pop.webp" mode="heightFix" />
					<text class="pc__hero-badge-t">Lv.{{ level }} {{ levelName }}</text>
				</view>
				<view class="pc__hero-sign" :class="{ 'pc__hero-sign--done': signedToday }" @click="onSign">
					<text class="pc__hero-sign-t">{{ signedToday ? '今日已签' : '每日签到 +5' }}</text>
				</view>
			</view>
			<view class="pc__streak" v-if="streak > 0">
				<text class="pc__streak-t">已连续签到 {{ streak }} 天</text>
			</view>
		</view>

		<!-- 每日任务 -->
		<view class="pc__sect">
			<text class="pc__sect-t">每日任务</text>
			<text class="pc__sect-s">今日已完成 {{ doneCount }}/{{ tasks.length }}</text>
		</view>
		<view class="pc__task" v-for="(t, i) in tasks" :key="i" @click="onTask(i)">
			<view class="pc__task-icon" :class="'pc__task-icon--' + t.tone">
				<image class="pc__task-img" :src="t.icon" mode="aspectFit" />
			</view>
			<view class="pc__task-info">
				<text class="pc__task-title">{{ t.title }}</text>
				<text class="pc__task-sub">{{ t.sub }}</text>
			</view>
			<view class="pc__task-btn" :class="{ 'pc__task-btn--done': t.done }">
				<text class="pc__task-btn-t">{{ t.done ? '已完成' : '+' + t.point }}</text>
			</view>
		</view>

		<!-- 兑换入口 -->
		<view class="pc__mall" @click="goMall">
			<view class="pc__mall-info">
				<text class="pc__mall-title">积分兑换好礼</text>
				<text class="pc__mall-sub">精美礼品、专属特权等你来换</text>
			</view>
			<image class="pc__mall-img" src="/static/unida/bubbles/corner-sticker-y.webp" mode="aspectFit" />
			<image class="pc__chev" src="/static/icons-dark/chevron.png" mode="aspectFit" />
		</view>

		<!-- 积分明细 -->
		<view class="pc__sect">
			<text class="pc__sect-t">积分明细</text>
			<text class="pc__sect-s">收支流水，服务端记账</text>
		</view>
		<view class="pc__ledger">
			<view class="pc__ledger-row" v-for="(l, i) in ledgers" :key="l.id">
				<view class="pc__ledger-main">
					<text class="pc__ledger-title">{{ l.title }}</text>
					<text class="pc__ledger-time">{{ l.time }} · 余额 {{ l.balance }}</text>
				</view>
				<text class="pc__ledger-delta" :class="{ 'pc__ledger-delta--minus': l.delta < 0 }">{{ l.delta > 0 ? '+' + l.delta : l.delta }}</text>
			</view>
			<text class="pc__ledger-empty" v-if="ledgers.length === 0">还没有积分记录，去签到赚第一笔吧</text>
		</view>
	</view>
</template>

<script>
	import { callCloud, getToken } from '@/common/cloud.js';
	import { timeAgo } from '@/common/fmt.js';

	export default {
		data() {
			return {
				statusBar: 0,
				points: 0,
				streak: 0,
				signedToday: false,
				profileDone: false,
				hasOrders: false,
				loading: false,
				signBusy: false,
				level: 2,
				levelName: '初来乍到',
				tasks: [],
				ledgers: []
			};
		},
		computed: {
			pointsText() {
				return String(this.points).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
			},
			doneCount() {
				return this.tasks.filter((t) => t.done).length;
			}
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		onShow() {
			this.loadHome();
		},
		methods: {
			goBack() { uni.navigateBack(); },
			buildTasks() {
				this.tasks = [
					{ title: '每日签到', sub: '每天一次，+5 积分', point: 5, done: this.signedToday, icon: '/static/icons-dark/calendar.png', tone: 'purple', act: 'sign' },
					{ title: '完善个人资料', sub: '填写昵称和学校', point: 10, done: this.profileDone, icon: '/static/icons-dark/buddy.png', tone: 'green', act: 'profile' },
					{ title: '参加 1 个活动', sub: '报名任意校园活动', point: 20, done: this.hasOrders, icon: '/static/icons-dark/heart.png', tone: 'orange', act: 'act' },
					{ title: '发布 1 条动态', sub: '去社区分享校园生活', point: 15, done: false, icon: '/static/icons-dark/bulb.png', tone: 'pink', act: 'post' }
				];
			},
			async loadHome() {
				if (this.loading) return;
				this.loading = true;
				try {
					const r = await callCloud('points', { action: 'home', token: getToken() });
					this.points = Number(r.points) || 0;
					this.streak = Number(r.streak) || 0;
					this.signedToday = !!r.signedToday;
					this.profileDone = !!r.profileDone;
					this.hasOrders = !!r.hasOrders;
					const p = this.points;
					this.level = p >= 2000 ? 6 : p >= 1000 ? 5 : p >= 500 ? 4 : p >= 200 ? 3 : 2;
					this.levelName = p >= 2000 ? '校园明星' : p >= 1000 ? '活力星人' : p >= 500 ? '活跃成长者' : p >= 200 ? '热心搭友' : '初来乍到';
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '加载积分失败', icon: 'none' });
				} finally {
					this.buildTasks();
					this.loading = false;
				}
				this.loadLedger();
			},
			async loadLedger() {
				try {
					const r = await callCloud('points', { action: 'ledger', token: getToken() });
					this.ledgers = (r.list || []).map((x) => ({ ...x, time: timeAgo(x.ts) }));
				} catch (e) {}
			},
			async onSign() {
				if (this.signBusy) return;
				if (this.signedToday) {
					uni.showToast({ title: '今日已签到，明天再来吧～', icon: 'none' });
					return;
				}
				this.signBusy = true;
				try {
					const r = await callCloud('points', { action: 'checkin', token: getToken() });
					uni.navigateTo({
						url: '/pages/checkin/checkin?gained=' + (r.gained || 5) + '&streak=' + (r.streak || 1)
					});
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '签到失败', icon: 'none' });
				} finally {
					this.signBusy = false;
				}
			},
			onTask(i) {
				const t = this.tasks[i];
				if (!t || t.done) return;
				if (t.act === 'sign') { this.onSign(); return; }
				if (t.act === 'profile') { uni.navigateTo({ url: '/pages/profile-setup/profile-setup' }); return; }
				if (t.act === 'act') { uni.navigateTo({ url: '/pages/discover/discover' }); return; }
				if (t.act === 'post') { uni.navigateTo({ url: '/pages/community/community' }); return; }
			},
			goMall() { uni.navigateTo({ url: '/pages/points-mall/points-mall' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.pc { padding: 0 $page-x 60rpx; box-sizing: border-box; }

	.pc__nav { height: 110rpx; display: flex; align-items: center; justify-content: space-between; }
	.pc__back {
		width: 68rpx; height: 68rpx;
		background: $c-white;
		border-radius: 50%;
		box-shadow: $sh-card;
		display: flex; align-items: center; justify-content: center;
	}
	.pc__back-img { width: 32rpx; height: 32rpx; }
	.pc__title { font-size: 34rpx; font-weight: 800; color: $c-ink; letter-spacing: 1rpx; }
	.pc__ph { width: 68rpx; }

	.pc__hero {
		background: $g-brand;
		border-radius: $r-lg;
		padding: 44rpx 40rpx;
		display: flex; flex-direction: column;
		box-shadow: $sh-float;
	}
	.pc__hero-label { font-size: 25rpx; color: rgba(255, 255, 255, 0.9); }
	.pc__hero-num { margin-top: 8rpx; font-family: $ff-num; font-size: 88rpx; font-weight: 800; color: $c-white; line-height: 1.15; }
	.pc__hero-row { display: flex; align-items: center; justify-content: space-between; margin-top: 24rpx; }
	.pc__hero-badge { display: flex; align-items: center; background: rgba(255, 255, 255, 0.2); padding: 8rpx 18rpx 8rpx 8rpx; border-radius: $r-pill; }
	.pc__hero-badge-img { height: 48rpx; width: 84rpx; }
	.pc__hero-badge-t { margin-left: 10rpx; font-size: 23rpx; color: $c-white; font-weight: 600; }
	.pc__hero-sign { background: $c-white; border-radius: $r-pill; padding: 14rpx 28rpx; }
	.pc__hero-sign--done { opacity: 0.75; }
	.pc__hero-sign-t { font-size: 24rpx; color: $c-primary; font-weight: 700; }
	.pc__streak { margin-top: 20rpx; }
	.pc__streak-t { font-size: 22rpx; color: rgba(255, 255, 255, 0.85); font-family: $ff-num; letter-spacing: 1rpx; }

	.pc__sect { display: flex; align-items: baseline; margin: 36rpx 0 0; }
	.pc__sect-t { font-size: 32rpx; font-weight: 800; color: $c-ink; }
	.pc__sect-s { margin-left: auto; font-size: 22rpx; color: $t-tertiary; font-family: $ff-num; }

	.pc__task {
		display: flex; align-items: center;
		margin-top: 16rpx;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 24rpx;
	}
	.pc__task-icon { width: 80rpx; height: 80rpx; border-radius: 24rpx; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
	.pc__task-icon--purple { background: rgba(128, 92, 250, 0.13); }
	.pc__task-icon--green { background: rgba(41, 202, 131, 0.14); }
	.pc__task-icon--orange { background: rgba(255, 155, 119, 0.16); }
	.pc__task-icon--pink { background: rgba(244, 114, 182, 0.14); }
	.pc__task-img { width: 40rpx; height: 40rpx; }
	.pc__task-info { flex: 1; margin: 0 18rpx; display: flex; flex-direction: column; min-width: 0; }
	.pc__task-title { font-size: 27rpx; font-weight: 600; color: $t-main; }
	.pc__task-sub { margin-top: 6rpx; font-size: 21rpx; color: $t-sub; }
	.pc__task-btn {
		background: $g-cta;
		border-radius: $r-pill;
		padding: 13rpx 26rpx;
		flex-shrink: 0;
	}
	.pc__task-btn-t { font-size: 23rpx; color: $c-white; font-weight: 700; font-family: $ff-num; }
	.pc__task-btn--done { background: $c-ice; }
	.pc__task-btn--done .pc__task-btn-t { color: $t-sub; }

	.pc__mall {
		display: flex; align-items: center;
		margin-top: 28rpx;
		background: rgba(255, 201, 79, 0.18);
		border-radius: $r-md;
		padding: 26rpx 28rpx;
	}
	.pc__mall-info { flex: 1; display: flex; flex-direction: column; }
	.pc__mall-title { font-size: 28rpx; font-weight: 700; color: $t-main; }
	.pc__mall-sub { margin-top: 8rpx; font-size: 21rpx; color: $t-sub; }
	.pc__mall-img { width: 88rpx; height: 88rpx; margin-right: 12rpx; }
	.pc__chev { width: 26rpx; height: 26rpx; opacity: 0.4; }

	/* ---------- 积分明细 ---------- */
	.pc__ledger {
		margin-top: 16rpx;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 8rpx 28rpx;
	}
	.pc__ledger-row {
		display: flex; align-items: center;
		padding: 24rpx 0;
		border-bottom: 2rpx solid $c-line;
	}
	.pc__ledger-row:last-child { border-bottom: none; }
	.pc__ledger-main { flex: 1; min-width: 0; display: flex; flex-direction: column; }
	.pc__ledger-title { font-size: 26rpx; font-weight: 600; color: $t-main; }
	.pc__ledger-time { margin-top: 6rpx; font-size: 20rpx; color: $t-tertiary; font-family: $ff-num; }
	.pc__ledger-delta { font-family: $ff-num; font-size: 30rpx; font-weight: 800; color: $c-mint; flex-shrink: 0; }
	.pc__ledger-delta--minus { color: #E86154; }
	.pc__ledger-empty { display: block; padding: 40rpx 0; font-size: 24rpx; color: $t-tertiary; text-align: center; }
</style>
