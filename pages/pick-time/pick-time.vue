<template>
	<view class="pt unida-page">
		<view class="pt__nav"><text class="pt__back" @click="goBack">‹</text><text class="pt__title">选择活动时间</text><text class="pt__ph"></text></view>
		<view class="pt__quick">
			<text class="pt__label">快捷选择</text>
			<view class="pt__quick-list">
				<text v-for="(q, i) in quicks" :key="i" class="pt__quick-item" :class="{ 'pt__quick-item--on': active === q }" @click="active = q">{{ q }}</text>
			</view>
		</view>
		<view class="pt__picker unida-card">
			<text class="pt__label">自定义日期时间</text>
			<picker mode="date" :value="date" @change="onDate">
				<view class="pt__row"><text>日期</text><text class="pt__row-val">{{ date }} ›</text></view>
			</picker>
			<picker mode="time" :value="time" @change="onTime">
				<view class="pt__row"><text>时间</text><text class="pt__row-val">{{ time }} ›</text></view>
			</picker>
		</view>
		<view class="pt__submit" @click="onConfirm">确定</view>
	</view>
</template>

<script>
	export default {
		data() {
			const now = new Date();
			return {
				quicks: ['今天', '明天', '本周末', '下周'],
				active: '明天',
				date: now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate() + 1).padStart(2, '0'),
				time: '19:00'
			};
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onDate(e) { this.date = e.detail.value; this.active = ''; },
			onTime(e) { this.time = e.detail.value; },
			onConfirm() {
				const val = this.active ? this.active + ' ' + this.time : this.date + ' ' + this.time;
				uni.$emit('pickTime', val);
				uni.navigateBack();
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.pt { padding: 0 24rpx 60rpx; }
	.pt__nav { height: 120rpx; padding-top: 60rpx; display: flex; align-items: center; justify-content: space-between; }
	.pt__back { font-size: 48rpx; width: 60rpx; }
	.pt__title { font-size: 32rpx; font-weight: 700; }
	.pt__ph { width: 60rpx; }
	.pt__label { display: block; font-size: 28rpx; font-weight: 700; color: $unida-text; margin-bottom: 20rpx; }
	.pt__quick { margin-top: 40rpx; }
	.pt__quick-list { display: flex; flex-wrap: wrap; gap: 16rpx; }
	.pt__quick-item { font-size: 26rpx; padding: 16rpx 32rpx; border-radius: 999rpx; background: #fff; color: $unida-text-sub; box-shadow: 0 6rpx 18rpx rgba(123,97,255,0.06); }
	.pt__quick-item--on { background: linear-gradient(135deg,#7B61FF,#B59BFF); color: #fff; }
	.pt__picker { margin-top: 40rpx; }
	.pt__row { display: flex; justify-content: space-between; padding: 24rpx 0; border-bottom: 2rpx solid $unida-divider; font-size: 28rpx; color: $unida-text-sub; }
	.pt__row-val { color: $unida-text; font-weight: 600; }
	.pt__submit { margin-top: 60rpx; height: 92rpx; border-radius: 999rpx; background: linear-gradient(135deg,#7B61FF,#B59BFF); color: #fff; font-size: 30rpx; font-weight: 700; display: flex; align-items: center; justify-content: center; }
</style>
