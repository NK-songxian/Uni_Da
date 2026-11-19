<template>
	<view class="rv unida-page">
		<view class="rv__nav"><text class="rv__back" @click="goBack">‹</text><text class="rv__title">活动评价</text><text class="rv__ph"></text></view>
		<view class="rv__event unida-card">
			<view class="rv__event-icon">🎪</view>
			<view><text class="rv__event-title">校园草地音乐会</text><text class="rv__event-sub">本周六 · 中心草坪广场</text></view>
		</view>
		<view class="rv__rate unida-card">
			<text class="rv__rate-label">整体体验</text>
			<view class="rv__stars">
				<text v-for="n in 5" :key="n" class="rv__star" :class="{ 'rv__star--on': n <= rating }" @click="rating = n">⭐</text>
			</view>
			<text class="rv__rate-hint">{{ ratingText }}</text>
		</view>
		<view class="rv__tags unida-card">
			<text class="rv__rate-label">快速评价（可多选）</text>
			<view class="rv__tag-list">
				<text v-for="(t, i) in tags" :key="i" class="rv__tag" :class="{ 'rv__tag--on': chosen.includes(t) }" @click="toggleTag(t)">{{ t }}</text>
			</view>
		</view>
		<view class="rv__content unida-card">
			<text class="rv__rate-label">说说你的感受</text>
			<textarea class="rv__textarea" v-model="content" placeholder="活动怎么样？有什么想说的～" maxlength="200"></textarea>
			<text class="rv__count">{{ content.length }}/200</text>
		</view>
		<view class="rv__submit" @click="onSubmit">提交评价</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				rating: 5,
				tags: ['组织有序', '氛围超好', '认识新朋友', '场地不错', '值得一来', '下次还来'],
				chosen: [],
				content: ''
			};
		},
		computed: {
			ratingText() { return ['', '很差', '一般', '还行', '不错', '超棒！'][this.rating]; }
		},
		methods: {
			goBack() { uni.navigateBack(); },
			toggleTag(t) {
				const i = this.chosen.indexOf(t);
				if (i >= 0) this.chosen.splice(i, 1); else this.chosen.push(t);
			},
			onSubmit() {
				if (!this.rating) { uni.showToast({ title: '请给活动评分', icon: 'none' }); return; }
				uni.showToast({ title: '评价已提交（演示）', icon: 'success' });
				setTimeout(() => uni.navigateBack(), 1200);
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.rv { padding: 0 24rpx 60rpx; }
	.rv__nav { height: 120rpx; padding-top: 60rpx; display: flex; align-items: center; justify-content: space-between; }
	.rv__back { font-size: 48rpx; width: 60rpx; }
	.rv__title { font-size: 32rpx; font-weight: 700; }
	.rv__ph { width: 60rpx; }
	.rv__event { display: flex; align-items: center; }
	.rv__event-icon { width: 90rpx; height: 90rpx; border-radius: 20rpx; background: linear-gradient(135deg,#7B61FF,#FFD76A); display: flex; align-items: center; justify-content: center; font-size: 48rpx; margin-right: 20rpx; }
	.rv__event view { display: flex; flex-direction: column; }
	.rv__event-title { font-size: 28rpx; font-weight: 700; color: $unida-text; }
	.rv__event-sub { margin-top: 8rpx; font-size: 22rpx; color: $unida-text-sub; }
	.rv__rate, .rv__tags, .rv__content { margin-top: 20rpx; }
	.rv__rate { display: flex; flex-direction: column; align-items: center; }
	.rv__rate-label { display: block; font-size: 28rpx; font-weight: 700; color: $unida-text; align-self: flex-start; }
	.rv__stars { display: flex; gap: 16rpx; margin-top: 24rpx; }
	.rv__star { font-size: 56rpx; filter: grayscale(1) opacity(0.3); }
	.rv__star--on { filter: none; }
	.rv__rate-hint { margin-top: 16rpx; font-size: 26rpx; color: $unida-orange; font-weight: 700; }
	.rv__tag-list { display: flex; flex-wrap: wrap; gap: 16rpx; margin-top: 20rpx; }
	.rv__tag { font-size: 24rpx; color: $unida-text-sub; background: $unida-bg; padding: 14rpx 24rpx; border-radius: 999rpx; border: 2rpx solid transparent; }
	.rv__tag--on { color: $unida-primary; background: rgba(123,97,255,0.08); border-color: $unida-primary; }
	.rv__textarea { width: 100%; height: 180rpx; margin-top: 20rpx; font-size: 26rpx; line-height: 1.6; }
	.rv__count { display: block; text-align: right; font-size: 22rpx; color: $unida-text-sub; }
	.rv__submit { margin-top: 40rpx; height: 92rpx; border-radius: 999rpx; background: linear-gradient(135deg,#7B61FF,#B59BFF); color: #fff; font-size: 30rpx; font-weight: 700; display: flex; align-items: center; justify-content: center; }
</style>
