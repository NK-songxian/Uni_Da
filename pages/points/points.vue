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
			<text class="pc__hero-num">1,280</text>
			<view class="pc__hero-row">
				<view class="pc__hero-badge">
					<image class="pc__hero-badge-img" src="/static/unida/bubbles/label-pop.webp" mode="heightFix" />
					<text class="pc__hero-badge-t">Lv.5 活力星人</text>
				</view>
				<view class="pc__hero-sign" @click="onSign"><text class="pc__hero-sign-t">每日签到 +5</text></view>
			</view>
		</view>

		<!-- 每日任务 -->
		<view class="pc__sect">
			<text class="pc__sect-t">每日任务</text>
			<text class="pc__sect-s">今日已完成 1/4</text>
		</view>
		<view class="pc__task" v-for="(t, i) in tasks" :key="i">
			<view class="pc__task-icon" :class="'pc__task-icon--' + t.tone">
				<image class="pc__task-img" :src="t.icon" mode="aspectFit" />
			</view>
			<view class="pc__task-info">
				<text class="pc__task-title">{{ t.title }}</text>
				<text class="pc__task-sub">{{ t.sub }}</text>
			</view>
			<view class="pc__task-btn" :class="{ 'pc__task-btn--done': t.done }" @click="onTask(i)">
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
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				tasks: [
					{ title: '每日签到', sub: '每天一次', point: 5, done: true, icon: '/static/icons-dark/calendar.png', tone: 'purple' },
					{ title: '完善个人资料', sub: '填写头像和兴趣', point: 10, done: false, icon: '/static/icons-dark/buddy.png', tone: 'green' },
					{ title: '参加 1 个活动', sub: '线下活动签到', point: 20, done: false, icon: '/static/icons-dark/heart.png', tone: 'orange' },
					{ title: '评价一次活动', sub: '给出你的体验', point: 15, done: false, icon: '/static/icons-dark/bulb.png', tone: 'pink' }
				]
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onSign() { uni.showToast({ title: '今日已签到', icon: 'none' }); },
			onTask(i) {
				if (this.tasks[i].done) return;
				this.tasks = this.tasks.map((x, j) => j === i ? { icon: x.icon, title: x.title, sub: x.sub, point: x.point, tone: x.tone, done: true } : x);
				uni.showToast({ title: '任务完成 +' + this.tasks[i].point + ' 积分', icon: 'success' });
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
	.pc__hero-sign-t { font-size: 24rpx; color: $c-primary; font-weight: 700; }

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
</style>
