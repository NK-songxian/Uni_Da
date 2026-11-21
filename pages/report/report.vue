<template>
	<view class="rp unida-page">
		<view class="rp-safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 顶栏 -->
		<view class="rp__nav">
			<view class="rp__back" @click="goBack"><image class="rp__back-img" src="/static/icons-dark/back.png" mode="aspectFit" /></view>
			<text class="rp__title">举报</text>
			<view class="rp__ph"></view>
		</view>

		<!-- 提示 -->
		<view class="rp__tip">
			<image class="rp__tip-img" src="/static/unida/bubbles/shield-check.webp" mode="heightFix" />
			<text class="rp__tip-text">请选择举报原因，我们会尽快核实处理。恶意举报将被处罚。</text>
		</view>

		<!-- 原因单选 -->
		<view class="rp__card">
			<view class="rp__label-row">
				<text class="rp__label">举报原因</text>
				<text class="rp__req">*</text>
			</view>
			<view class="rp__reason" v-for="(r, i) in reasons" :key="i" :class="{ 'rp__reason--on': selected === i }" @click="onSelect(i)">
				<view class="rp__radio" :class="{ 'rp__radio--on': selected === i }">
					<view class="rp__radio-dot" v-if="selected === i"></view>
				</view>
				<text class="rp__reason-t">{{ r }}</text>
				<image class="rp__reason-check" v-if="selected === i" src="/static/unida/bubbles/check-purple.webp" mode="heightFix" />
			</view>
		</view>

		<!-- 补充说明 -->
		<view class="rp__card">
			<text class="rp__label">补充说明 <text class="rp__label-sub">（选填）</text></text>
			<textarea class="rp__textarea" :value="detail" placeholder="请描述具体情况，帮助我们更快处理…" maxlength="200" @input="onDetail" />
			<text class="rp__count">{{ detail.length }}/200</text>
		</view>

		<!-- 提交 -->
		<view class="rp__submit" @click="onSubmit"><text class="rp__submit-t">提交举报</text></view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				selected: -1,
				detail: '',
				reasons: ['色情低俗', '虚假信息 / 诈骗', '人身攻击', '广告骚扰', '侵权内容', '其他原因']
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onSelect(i) { this.selected = i; },
			onDetail(e) { this.detail = e.detail.value; },
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
	@import '@/common/unida-tokens.scss';

	.rp { padding: 0 $page-x 60rpx; box-sizing: border-box; }

	.rp__nav { height: 110rpx; display: flex; align-items: center; justify-content: space-between; }
	.rp__back {
		width: 68rpx; height: 68rpx;
		background: $c-white;
		border-radius: 50%;
		box-shadow: $sh-card;
		display: flex; align-items: center; justify-content: center;
	}
	.rp__back-img { width: 32rpx; height: 32rpx; }
	.rp__title { font-size: 34rpx; font-weight: 800; color: $c-ink; letter-spacing: 1rpx; }
	.rp__ph { width: 68rpx; }

	.rp__tip {
		display: flex; align-items: center;
		background: rgba(255, 201, 79, 0.18);
		border-radius: $r-sm;
		padding: 20rpx 24rpx;
	}
	.rp__tip-img { height: 60rpx; width: 72rpx; margin-right: 16rpx; flex-shrink: 0; }
	.rp__tip-text { flex: 1; font-size: 23rpx; color: #8A6D1F; line-height: 1.6; }

	.rp__card {
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 28rpx;
		margin-top: 20rpx;
	}
	.rp__label-row { display: flex; align-items: center; }
	.rp__label { font-size: 30rpx; font-weight: 800; color: $c-ink; }
	.rp__label-sub { font-size: 22rpx; color: $t-tertiary; font-weight: 400; }
	.rp__req { margin-left: 8rpx; font-size: 26rpx; color: $c-peach; }

	.rp__reason {
		display: flex; align-items: center;
		padding: 22rpx 0;
		border-bottom: 2rpx solid $c-line;
	}
	.rp__reason:last-child { border-bottom: none; }
	.rp__radio {
		width: 40rpx; height: 40rpx;
		border-radius: 50%;
		border: 3rpx solid $c-ice;
		display: flex; align-items: center; justify-content: center;
		margin-right: 18rpx;
		flex-shrink: 0;
		box-sizing: border-box;
	}
	.rp__radio--on { border-color: $c-primary; }
	.rp__radio-dot { width: 20rpx; height: 20rpx; border-radius: 50%; background: $c-primary; }
	.rp__reason-t { flex: 1; font-size: 27rpx; color: $t-main; }
	.rp__reason--on .rp__reason-t { color: $c-primary; font-weight: 600; }
	.rp__reason-check { height: 40rpx; width: 52rpx; }

	.rp__textarea {
		width: 100%; height: 180rpx;
		margin-top: 20rpx;
		font-size: 26rpx;
		line-height: 1.6;
		color: $t-main;
		box-sizing: border-box;
	}
	.rp__count { display: block; text-align: right; font-size: 22rpx; color: $t-tertiary; font-family: $ff-num; }

	.rp__submit {
		margin-top: 40rpx;
		height: 92rpx;
		border-radius: $r-pill;
		background: linear-gradient(145deg, #FF8A7A, #F2564D);
		box-shadow: 0 12rpx 24rpx rgba(242, 86, 77, 0.24);
		display: flex; align-items: center; justify-content: center;
	}
	.rp__submit-t { font-size: 30rpx; color: $c-white; font-weight: 700; letter-spacing: 2rpx; }
</style>
