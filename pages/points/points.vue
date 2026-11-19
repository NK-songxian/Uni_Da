<template>
	<view class="pc unida-page">
		<view class="pc__nav"><text class="pc__back" @click="goBack">‹</text><text class="pc__title">积分中心</text><text class="pc__ph"></text></view>

		<!-- 积分卡 -->
		<view class="pc__hero">
			<view class="pc__hero-deco">✦</view>
			<text class="pc__hero-label">我的积分</text>
			<text class="pc__hero-num">1,280</text>
			<view class="pc__hero-row">
				<view class="pc__hero-badge">🥇 Lv.5 活力星人</view>
				<view class="pc__hero-sign" @click="onSign">每日签到 +5</view>
			</view>
		</view>

		<!-- 每日任务 -->
		<view class="unida-section" style="margin-top:28rpx">
			<view class="unida-section__head"><text class="unida-section__title">每日任务</text><text class="unida-section__more">今日已完成 1/4</text></view>
			<view class="pc__task unida-card" v-for="(t, i) in tasks" :key="i">
				<view class="pc__task-icon" :style="{ background: t.bg }">{{ t.icon }}</view>
				<view class="pc__task-info">
					<text class="pc__task-title">{{ t.title }}</text>
					<text class="pc__task-sub">{{ t.sub }}</text>
				</view>
				<view class="pc__task-btn" :class="{ 'pc__task-btn--done': t.done }" @click="onTask(t, i)">{{ t.done ? '已完成' : '+' + t.point }}</view>
			</view>
		</view>

		<!-- 兑换入口 -->
		<view class="pc__mall" @click="goMall">
			<view class="pc__mall-icon">🎁</view>
			<view class="pc__mall-info"><text class="pc__mall-title">积分兑换好礼</text><text class="pc__mall-sub">精美礼品、专属特权等你来换</text></view>
			<text class="pc__mall-arrow">›</text>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				tasks: [
					{ icon: '📅', title: '每日签到', sub: '每天一次', point: 5, done: true, bg: 'linear-gradient(135deg,#7B61FF,#B59BFF)' },
					{ icon: '📝', title: '完善个人资料', sub: '填写头像和兴趣', point: 10, done: false, bg: 'linear-gradient(135deg,#34D399,#86EFAC)' },
					{ icon: '🎪', title: '参加 1 个活动', sub: '线下活动签到', point: 20, done: false, bg: 'linear-gradient(135deg,#FF8A3D,#FFD76A)' },
					{ icon: '⭐', title: '评价一次活动', sub: '给出你的体验', point: 15, done: false, bg: 'linear-gradient(135deg,#F472B6,#FBCFE8)' }
				]
			};
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onSign() { uni.showToast({ title: '今日已签到', icon: 'none' }); },
			onTask(t, i) {
				if (t.done) return;
				this.tasks[i].done = true;
				uni.showToast({ title: '任务完成 +' + t.point + ' 积分', icon: 'success' });
			},
			goMall() { uni.navigateTo({ url: '/pages/points-mall/points-mall' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.pc { padding: 0 24rpx 60rpx; }
	.pc__nav { height: 120rpx; padding-top: 60rpx; display: flex; align-items: center; justify-content: space-between; }
	.pc__back { font-size: 48rpx; width: 60rpx; }
	.pc__title { font-size: 32rpx; font-weight: 700; }
	.pc__ph { width: 60rpx; }
	.pc__hero { position: relative; margin-top: 20rpx; border-radius: 28rpx; padding: 44rpx 40rpx; background: linear-gradient(135deg,#7B61FF,#9B7BFF,#B59BFF); overflow: hidden; display: flex; flex-direction: column; }
	.pc__hero-deco { position: absolute; right: 60rpx; top: 40rpx; font-size: 56rpx; color: rgba(255,255,255,0.5); }
	.pc__hero-label { font-size: 26rpx; color: rgba(255,255,255,0.9); }
	.pc__hero-num { font-size: 84rpx; font-weight: 800; color: #fff; line-height: 1.2; }
	.pc__hero-row { display: flex; align-items: center; justify-content: space-between; margin-top: 20rpx; }
	.pc__hero-badge { font-size: 24rpx; color: #a97b12; background: rgba(255,215,106,0.9); padding: 10rpx 22rpx; border-radius: 999rpx; }
	.pc__hero-sign { font-size: 24rpx; color: $unida-primary; background: #fff; padding: 12rpx 26rpx; border-radius: 999rpx; font-weight: 600; }
	.pc__task { display: flex; align-items: center; margin-bottom: 16rpx; }
	.pc__task-icon { width: 80rpx; height: 80rpx; border-radius: 22rpx; display: flex; align-items: center; justify-content: center; font-size: 40rpx; margin-right: 18rpx; }
	.pc__task-info { flex: 1; display: flex; flex-direction: column; }
	.pc__task-title { font-size: 28rpx; font-weight: 600; color: $unida-text; }
	.pc__task-sub { margin-top: 6rpx; font-size: 22rpx; color: $unida-text-sub; }
	.pc__task-btn { font-size: 24rpx; color: #fff; background: linear-gradient(135deg,#7B61FF,#B59BFF); padding: 12rpx 24rpx; border-radius: 999rpx; font-weight: 600; }
	.pc__task-btn--done { background: #e8e2f5; color: $unida-text-sub; }
	.pc__mall { display: flex; align-items: center; margin-top: 28rpx; padding: 28rpx; background: rgba(255,215,106,0.2); border-radius: 24rpx; }
	.pc__mall-icon { font-size: 60rpx; margin-right: 20rpx; }
	.pc__mall-info { flex: 1; display: flex; flex-direction: column; }
	.pc__mall-title { font-size: 28rpx; font-weight: 700; color: $unida-text; }
	.pc__mall-sub { margin-top: 8rpx; font-size: 22rpx; color: $unida-text-sub; }
	.pc__mall-arrow { font-size: 40rpx; color: $unida-text-sub; }
</style>
