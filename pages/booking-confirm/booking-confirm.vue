<template>
	<view class="bc unida-page">
		<view class="bc__nav">
			<text class="bc__back" @click="goBack">‹</text>
			<text class="bc__title">预约确认</text>
			<text class="bc__ph"></text>
		</view>

		<!-- 活动卡片 -->
		<view class="bc__activity unida-card">
			<view class="bc__cover">🎪</view>
			<view class="bc__activity-info">
				<text class="bc__activity-title">校园草地音乐会 · 一起嗨翻周末</text>
				<view class="bc__activity-tags">
					<text class="unida-tag unida-tag--purple">校园活动</text>
					<text class="unida-tag unida-tag--green">免费</text>
				</view>
				<text class="bc__activity-meta">🕒 本周六 19:00-21:00</text>
				<text class="bc__activity-meta">📍 中心草坪广场</text>
			</view>
		</view>

		<!-- 预约与确认 -->
		<view class="bc__section unida-card">
			<view class="bc__head"><text class="bc__head-title">预约与确认</text></view>
			<view class="bc__row"><text>预约时间</text><text class="bc__row-val">本周六 19:00</text></view>
			<view class="bc__row"><text>参与人数</text><text class="bc__row-val">1 人</text></view>
			<view class="bc__row"><text>联系电话</text><text class="bc__row-val">138****8888</text></view>
		</view>

		<!-- 参与备注 -->
		<view class="bc__section unida-card">
			<view class="bc__head"><text class="bc__head-title">参与备注 <text class="bc__optional">（选填）</text></text></view>
			<textarea class="bc__textarea" v-model="remark" placeholder="想对发起人说什么？例如：我会弹吉他～" maxlength="100"></textarea>
			<text class="bc__count">{{ remark.length }}/100</text>
		</view>

		<!-- 费用提示 -->
		<view class="bc__notice">
			<text class="bc__notice-icon">💰</text>
			<text class="bc__notice-text">本活动免费，现场零食饮料 AA 自愿参与。请准时到场，如需取消请提前 2 小时操作。</text>
		</view>

		<!-- 底部提交 -->
		<view class="bc__bottom">
			<view class="bc__agree" @click="agreed = !agreed">
				<view class="bc__checkbox" :class="{ 'bc__checkbox--on': agreed }"><text v-if="agreed">✓</text></view>
				<text>我已阅读并同意活动参与须知</text>
			</view>
			<view class="bc__submit" @click="onSubmit">提交预约</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return { remark: '', agreed: true };
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onSubmit() {
				if (!this.agreed) { uni.showToast({ title: '请先同意活动须知', icon: 'none' }); return; }
				uni.navigateTo({ url: '/pages/booking-success/booking-success' });
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.bc { padding: 0 24rpx 200rpx; }
	.bc__nav { height: 120rpx; padding-top: 60rpx; display: flex; align-items: center; justify-content: space-between; margin: 0 -24rpx; padding-left: 32rpx; padding-right: 32rpx; }
	.bc__back { font-size: 48rpx; width: 60rpx; }
	.bc__title { font-size: 32rpx; font-weight: 700; }
	.bc__ph { width: 60rpx; }
	.bc__activity { display: flex; padding: 20rpx; }
	.bc__cover { width: 160rpx; height: 160rpx; border-radius: 20rpx; background: linear-gradient(135deg,#7B61FF,#FFD76A); display: flex; align-items: center; justify-content: center; font-size: 72rpx; margin-right: 20rpx; flex-shrink: 0; }
	.bc__activity-info { flex: 1; display: flex; flex-direction: column; }
	.bc__activity-title { font-size: 28rpx; font-weight: 700; color: $unida-text; line-height: 1.4; }
	.bc__activity-tags { display: flex; gap: 10rpx; margin: 12rpx 0; }
	.bc__activity-meta { font-size: 22rpx; color: $unida-text-sub; margin-top: 4rpx; }
	.bc__section { margin-top: 20rpx; }
	.bc__head { margin-bottom: 20rpx; }
	.bc__head-title { font-size: 30rpx; font-weight: 700; color: $unida-text; }
	.bc__optional { font-size: 22rpx; color: $unida-text-sub; font-weight: 400; }
	.bc__row { display: flex; align-items: center; justify-content: space-between; padding: 18rpx 0; border-bottom: 2rpx solid $unida-divider; font-size: 26rpx; color: $unida-text-sub; }
	.bc__row:last-child { border-bottom: none; }
	.bc__row-val { color: $unida-text; font-weight: 600; }
	.bc__textarea { width: 100%; height: 160rpx; font-size: 26rpx; color: $unida-text; line-height: 1.6; }
	.bc__count { display: block; text-align: right; font-size: 22rpx; color: $unida-text-sub; }
	.bc__notice { display: flex; margin-top: 24rpx; padding: 24rpx; background: rgba(255,215,106,0.18); border-radius: 20rpx; }
	.bc__notice-icon { font-size: 36rpx; margin-right: 16rpx; }
	.bc__notice-text { flex: 1; font-size: 24rpx; color: #8a6d1f; line-height: 1.6; }
	.bc__bottom { position: fixed; left: 0; right: 0; bottom: 0; background: #fff; padding: 20rpx 24rpx calc(20rpx + env(safe-area-inset-bottom)); box-shadow: 0 -6rpx 24rpx rgba(123,97,255,0.08); z-index: 20; }
	.bc__agree { display: flex; align-items: center; justify-content: center; font-size: 22rpx; color: $unida-text-sub; margin-bottom: 16rpx; }
	.bc__checkbox { width: 32rpx; height: 32rpx; border-radius: 50%; border: 2rpx solid #c9c2dd; margin-right: 10rpx; display: flex; align-items: center; justify-content: center; font-size: 20rpx; color: #fff; }
	.bc__checkbox--on { background: $unida-primary; border-color: $unida-primary; }
	.bc__submit { height: 88rpx; border-radius: 999rpx; background: linear-gradient(135deg,#7B61FF,#B59BFF); color: #fff; font-size: 30rpx; font-weight: 700; display: flex; align-items: center; justify-content: center; box-shadow: 0 10rpx 24rpx rgba(123,97,255,0.28); }
</style>
