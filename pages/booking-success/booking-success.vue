<template>
	<view class="bs">
		<!-- 成功动画区 -->
		<view class="bs__hero">
			<view class="bs__circle">
				<text class="bs__check">✓</text>
			</view>
			<view class="bs__spark bs__spark--1">✦</view>
			<view class="bs__spark bs__spark--2">✦</view>
			<view class="bs__spark bs__spark--3">✦</view>
			<text class="bs__title">报名成功！</text>
			<text class="bs__sub">已成功加入活动，期待与你见面 🎉</text>
		</view>

		<!-- 预约信息卡 -->
		<view class="bs__card unida-card">
			<view class="bs__card-head">
				<text class="bs__card-title">预约信息</text>
				<text class="bs__card-status">已报名</text>
			</view>
			<view class="bs__row"><text>活动名称</text><text>校园草地音乐会</text></view>
			<view class="bs__row"><text>活动时间</text><text>本周六 19:00</text></view>
			<view class="bs__row"><text>活动地点</text><text>中心草坪广场</text></view>
			<view class="bs__row"><text>报名编号</text><text>UNI20261118</text></view>
			<view class="bs__qr">
				<text class="bs__qr-icon">▦</text>
				<text class="bs__qr-tip">签到二维码 · 现场出示</text>
			</view>
		</view>

		<!-- 提示 -->
		<view class="bs__tip">
			<text>💡 活动开始前会收到提醒，如需取消请在「我的预约」中操作</text>
		</view>

		<!-- 按钮组 -->
		<view class="bs__actions">
			<view class="bs__btn bs__btn--primary" @click="goMyBookings">查看我的预约</view>
			<view class="bs__btn bs__btn--ghost" @click="goHome">返回首页</view>
		</view>
	</view>
</template>

<script>
	export default {
		methods: {
			goMyBookings() { uni.showToast({ title: '我的预约页待接入', icon: 'none' }); },
			goHome() { uni.reLaunch({ url: '/pages/home/home' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.bs { min-height: 100vh; background: $unida-bg; padding: 0 32rpx 60rpx; }
	.bs__hero { display: flex; flex-direction: column; align-items: center; padding-top: 120rpx; position: relative; }
	.bs__circle { width: 180rpx; height: 180rpx; border-radius: 50%; background: linear-gradient(135deg,#34D399,#86EFAC); display: flex; align-items: center; justify-content: center; box-shadow: 0 20rpx 50rpx rgba(52,211,153,0.4); animation: pop 0.5s ease; }
	.bs__check { font-size: 100rpx; color: #fff; font-weight: 700; }
	@keyframes pop { from { transform: scale(0.4); opacity: 0; } to { transform: scale(1); opacity: 1; } }
	.bs__spark { position: absolute; color: $unida-yellow; font-size: 44rpx; top: 130rpx; }
	.bs__spark--1 { left: 140rpx; }
	.bs__spark--2 { right: 140rpx; top: 180rpx; color: $unida-primary; }
	.bs__spark--3 { right: 180rpx; color: $unida-orange; }
	.bs__title { margin-top: 44rpx; font-size: 44rpx; font-weight: 800; color: $unida-text; }
	.bs__sub { margin-top: 14rpx; font-size: 26rpx; color: $unida-text-sub; }
	.bs__card { margin-top: 60rpx; }
	.bs__card-head { display: flex; align-items: center; justify-content: space-between; padding-bottom: 20rpx; border-bottom: 2rpx solid $unida-divider; }
	.bs__card-title { font-size: 30rpx; font-weight: 700; color: $unida-text; }
	.bs__card-status { font-size: 22rpx; color: $unida-green; background: rgba(52,211,153,0.12); padding: 6rpx 18rpx; border-radius: 999rpx; }
	.bs__row { display: flex; justify-content: space-between; padding: 18rpx 0; font-size: 26rpx; color: $unida-text-sub; }
	.bs__row text:last-child { color: $unida-text; font-weight: 600; }
	.bs__qr { display: flex; flex-direction: column; align-items: center; margin-top: 20rpx; padding: 24rpx; background: $unida-bg; border-radius: 20rpx; }
	.bs__qr-icon { font-size: 120rpx; color: $unida-primary; line-height: 1; }
	.bs__qr-tip { margin-top: 12rpx; font-size: 22rpx; color: $unida-text-sub; }
	.bs__tip { margin-top: 28rpx; padding: 24rpx; background: rgba(123,97,255,0.06); border-radius: 20rpx; }
	.bs__tip text { font-size: 24rpx; color: $unida-primary; line-height: 1.6; }
	.bs__actions { margin-top: 48rpx; }
	.bs__btn { height: 92rpx; border-radius: 999rpx; display: flex; align-items: center; justify-content: center; font-size: 30rpx; font-weight: 700; margin-bottom: 20rpx; }
	.bs__btn--primary { background: linear-gradient(135deg,#7B61FF,#B59BFF); color: #fff; box-shadow: 0 10rpx 24rpx rgba(123,97,255,0.28); }
	.bs__btn--ghost { background: rgba(123,97,255,0.08); color: $unida-primary; }
</style>
