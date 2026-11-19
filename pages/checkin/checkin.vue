<template>
	<view class="ck">
		<view class="ck__hero">
			<view class="ck__circle"><text>✓</text></view>
			<text class="ck__title">打卡成功！</text>
			<text class="ck__sub">已完成签到，玩得开心 🎉</text>
		</view>
		<view class="ck__reward unida-card">
			<view class="ck__reward-icon">🎁</view>
			<view class="ck__reward-info">
				<text class="ck__reward-title">签到奖励</text>
				<text class="ck__reward-sub">积分 +20 · 已到账</text>
			</view>
			<text class="ck__reward-num">+20</text>
		</view>
		<view class="ck__btn" @click="goHome">完成</view>
	</view>
</template>

<script>
	export default {
		methods: { goHome() { uni.reLaunch({ url: '/pages/home/home' }); } }
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.ck { min-height: 100vh; padding: 0 40rpx 60rpx; background: $unida-bg; }
	.ck__hero { display: flex; flex-direction: column; align-items: center; padding-top: 160rpx; }
	.ck__circle { width: 180rpx; height: 180rpx; border-radius: 50%; background: linear-gradient(135deg,#34D399,#86EFAC); display: flex; align-items: center; justify-content: center; box-shadow: 0 20rpx 50rpx rgba(52,211,153,0.4); }
	.ck__circle text { font-size: 100rpx; color: #fff; font-weight: 700; }
	.ck__title { margin-top: 44rpx; font-size: 44rpx; font-weight: 800; color: $unida-text; }
	.ck__sub { margin-top: 14rpx; font-size: 26rpx; color: $unida-text-sub; }
	.ck__reward { display: flex; align-items: center; margin-top: 70rpx; }
	.ck__reward-icon { font-size: 64rpx; margin-right: 20rpx; }
	.ck__reward-info { flex: 1; display: flex; flex-direction: column; }
	.ck__reward-title { font-size: 28rpx; font-weight: 700; color: $unida-text; }
	.ck__reward-sub { margin-top: 8rpx; font-size: 24rpx; color: $unida-text-sub; }
	.ck__reward-num { font-size: 40rpx; font-weight: 800; color: $unida-orange; }
	.ck__btn { margin-top: 60rpx; height: 92rpx; border-radius: 999rpx; background: linear-gradient(135deg,#7B61FF,#B59BFF); color: #fff; font-size: 30rpx; font-weight: 700; display: flex; align-items: center; justify-content: center; }
</style>
