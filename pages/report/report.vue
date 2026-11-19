<template>
	<view class="rp unida-page">
		<view class="rp__nav"><text class="rp__back" @click="goBack">‹</text><text class="rp__title">举报</text><text class="rp__ph"></text></view>
		<view class="rp__tip">
			<text class="rp__tip-icon">🛡️</text>
			<text class="rp__tip-text">请选择举报原因，我们会尽快核实处理。恶意举报将被处罚。</text>
		</view>
		<view class="rp__section unida-card">
			<text class="rp__label">举报原因 <text class="rp__req">*</text></text>
			<view class="rp__reasons">
				<view class="rp__reason" v-for="(r, i) in reasons" :key="i" :class="{ 'rp__reason--on': selected === i }" @click="selected = i">
					<text class="rp__radio">{{ selected === i ? '●' : '○' }}</text>
					<text class="rp__reason-text">{{ r }}</text>
				</view>
			</view>
		</view>
		<view class="rp__section unida-card">
			<text class="rp__label">补充说明（选填）</text>
			<textarea class="rp__textarea" v-model="detail" placeholder="请描述具体情况，帮助我们更快处理…" maxlength="200"></textarea>
			<text class="rp__count">{{ detail.length }}/200</text>
		</view>
		<view class="rp__submit" @click="onSubmit">提交举报</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				selected: -1,
				detail: '',
				reasons: ['色情低俗', '虚假信息/诈骗', '人身攻击', '广告骚扰', '侵权内容', '其他原因']
			};
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onSubmit() {
				if (this.selected < 0) { uni.showToast({ title: '请选择举报原因', icon: 'none' }); return; }
				uni.showModal({
					title: '确认举报',
					content: '确定提交举报吗？我们会尽快核实。',
					success: (res) => { if (res.confirm) { uni.showToast({ title: '举报已提交', icon: 'success' }); setTimeout(() => uni.navigateBack(), 1200); } }
				});
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.rp { padding: 0 24rpx 60rpx; }
	.rp__nav { height: 120rpx; padding-top: 60rpx; display: flex; align-items: center; justify-content: space-between; }
	.rp__back { font-size: 48rpx; width: 60rpx; }
	.rp__title { font-size: 32rpx; font-weight: 700; }
	.rp__ph { width: 60rpx; }
	.rp__tip { display: flex; padding: 24rpx; background: rgba(255,215,106,0.2); border-radius: 20rpx; }
	.rp__tip-icon { font-size: 40rpx; margin-right: 16rpx; }
	.rp__tip-text { flex: 1; font-size: 24rpx; color: #8a6d1f; line-height: 1.6; }
	.rp__section { margin-top: 20rpx; }
	.rp__label { display: block; font-size: 28rpx; font-weight: 700; color: $unida-text; margin-bottom: 20rpx; }
	.rp__req { color: $unida-orange; }
	.rp__reasons { display: flex; flex-direction: column; }
	.rp__reason { display: flex; align-items: center; padding: 20rpx 0; border-bottom: 2rpx solid $unida-divider; }
	.rp__reason:last-child { border-bottom: none; }
	.rp__radio { font-size: 32rpx; color: $unida-primary; margin-right: 16rpx; }
	.rp__reason-text { font-size: 26rpx; color: $unida-text; }
	.rp__textarea { width: 100%; height: 180rpx; font-size: 26rpx; line-height: 1.6; }
	.rp__count { display: block; text-align: right; font-size: 22rpx; color: $unida-text-sub; }
	.rp__submit { margin-top: 40rpx; height: 92rpx; border-radius: 999rpx; background: linear-gradient(135deg,#FF6B6B,#FF8A3D); color: #fff; font-size: 30rpx; font-weight: 700; display: flex; align-items: center; justify-content: center; }
</style>
