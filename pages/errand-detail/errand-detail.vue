<template>
	<view class="ed unida-page">
		<view class="ed__nav"><text class="ed__back" @click="goBack">‹</text><text class="ed__title">跑腿订单详情</text><text class="ed__ph"></text></view>

		<!-- 状态卡 -->
		<view class="ed__status unida-card">
			<view class="ed__status-icon">🛵</view>
			<view class="ed__status-info">
				<text class="ed__status-title">待接单</text>
				<text class="ed__status-sub">赏金 ¥8.00 · 快递代取</text>
			</view>
			<text class="ed__status-badge">进行中</text>
		</view>

		<!-- 进度条 -->
		<view class="ed__progress unida-card">
			<view class="ed__step" v-for="(s, i) in steps" :key="i">
				<view class="ed__step-dot" :class="{ 'ed__step-dot--on': i <= activeStep }">{{ i <= activeStep ? '✓' : i + 1 }}</view>
				<text class="ed__step-label" :class="{ 'ed__step-label--on': i <= activeStep }">{{ s }}</text>
				<view v-if="i < steps.length - 1" class="ed__step-line" :class="{ 'ed__step-line--on': i < activeStep }"></view>
			</view>
		</view>

		<!-- 需求信息 -->
		<view class="ed__section unida-card">
			<view class="ed__head"><text class="ed__head-title">需求详情</text></view>
			<view class="ed__row"><text>需求描述</text><text>帮忙取个快递，中通北区驿站，取件码已私聊</text></view>
			<view class="ed__row"><text>取件地点</text><text>北区快递驿站</text></view>
			<view class="ed__row"><text>送达地点</text><text>东园3栋宿舍楼下</text></view>
			<view class="ed__row"><text>期望时间</text><text>今天 18:00 前</text></view>
			<view class="ed__row"><text>订单编号</text><text>RT20261118001</text></view>
		</view>

		<!-- 发布者 -->
		<view class="ed__user unida-card" @click="goUser">
			<text class="ed__user-avatar">😄</text>
			<view class="ed__user-info"><text class="ed__user-name">阿星</text><text class="ed__user-sub">🎓 已认证 · ⭐ 4.9</text></view>
			<text class="ed__user-arrow">›</text>
		</view>

		<!-- 底部操作 -->
		<view class="ed__bottom">
			<view class="ed__btn ed__btn--ghost" @click="onChat">💬 联系TA</view>
			<view class="ed__btn ed__btn--primary" @click="onAccept">立即接单</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return { steps: ['发布需求', '接单', '执行中', '已交付', '评价'], activeStep: 1 };
		},
		methods: {
			goBack() { uni.navigateBack(); },
			goUser() { uni.navigateTo({ url: '/pages/user-home/user-home' }); },
			onChat() { uni.navigateTo({ url: '/pages/chat/chat' }); },
			onAccept() { uni.showToast({ title: '接单成功（演示）', icon: 'success' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.ed { padding: 0 24rpx 180rpx; }
	.ed__nav { height: 120rpx; padding-top: 60rpx; display: flex; align-items: center; justify-content: space-between; }
	.ed__back { font-size: 48rpx; width: 60rpx; }
	.ed__title { font-size: 32rpx; font-weight: 700; }
	.ed__ph { width: 60rpx; }
	.ed__status { display: flex; align-items: center; }
	.ed__status-icon { width: 96rpx; height: 96rpx; border-radius: 24rpx; background: linear-gradient(135deg,#FF8A3D,#FFD76A); display: flex; align-items: center; justify-content: center; font-size: 52rpx; margin-right: 20rpx; }
	.ed__status-info { flex: 1; display: flex; flex-direction: column; }
	.ed__status-title { font-size: 30rpx; font-weight: 800; color: $unida-text; }
	.ed__status-sub { margin-top: 8rpx; font-size: 24rpx; color: $unida-orange; font-weight: 600; }
	.ed__status-badge { font-size: 22rpx; color: $unida-primary; background: rgba(123,97,255,0.08); padding: 8rpx 18rpx; border-radius: 999rpx; }
	.ed__progress { display: flex; justify-content: space-between; margin-top: 20rpx; padding: 32rpx 20rpx; }
	.ed__step { flex: 1; display: flex; flex-direction: column; align-items: center; position: relative; }
	.ed__step-dot { width: 48rpx; height: 48rpx; border-radius: 50%; background: #e8e2f5; color: #fff; font-size: 24rpx; display: flex; align-items: center; justify-content: center; z-index: 2; }
	.ed__step-dot--on { background: linear-gradient(135deg,#7B61FF,#B59BFF); }
	.ed__step-label { margin-top: 12rpx; font-size: 20rpx; color: $unida-text-sub; }
	.ed__step-label--on { color: $unida-primary; }
	.ed__step-line { position: absolute; top: 24rpx; left: 50%; width: 100%; height: 4rpx; background: #e8e2f5; }
	.ed__step-line--on { background: $unida-primary; }
	.ed__section { margin-top: 20rpx; }
	.ed__head { margin-bottom: 16rpx; }
	.ed__head-title { font-size: 30rpx; font-weight: 700; color: $unida-text; }
	.ed__row { display: flex; justify-content: space-between; padding: 18rpx 0; border-bottom: 2rpx solid $unida-divider; font-size: 24rpx; color: $unida-text-sub; }
	.ed__row:last-child { border-bottom: none; }
	.ed__row text:last-child { color: $unida-text; font-weight: 600; text-align: right; max-width: 60%; }
	.ed__user { display: flex; align-items: center; margin-top: 20rpx; }
	.ed__user-avatar { font-size: 56rpx; margin-right: 18rpx; }
	.ed__user-info { flex: 1; display: flex; flex-direction: column; }
	.ed__user-name { font-size: 28rpx; font-weight: 700; color: $unida-text; }
	.ed__user-sub { margin-top: 8rpx; font-size: 22rpx; color: $unida-text-sub; }
	.ed__user-arrow { font-size: 40rpx; color: $unida-text-sub; }
	.ed__bottom { position: fixed; left: 0; right: 0; bottom: 0; background: #fff; padding: 20rpx 24rpx calc(20rpx + env(safe-area-inset-bottom)); display: flex; gap: 20rpx; box-shadow: 0 -6rpx 24rpx rgba(123,97,255,0.08); z-index: 20; }
	.ed__btn { flex: 1; height: 88rpx; border-radius: 999rpx; display: flex; align-items: center; justify-content: center; font-size: 28rpx; font-weight: 700; }
	.ed__btn--ghost { background: rgba(123,97,255,0.08); color: $unida-primary; }
	.ed__btn--primary { background: linear-gradient(135deg,#7B61FF,#B59BFF); color: #fff; }
</style>
