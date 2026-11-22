<template>
	<view class="ck unida-page">
		<view class="ck__hero">
			<view class="ck__spark ck__spark--a"></view>
			<view class="ck__spark ck__spark--b"></view>
			<view class="ck__spark ck__spark--c"></view>
			<image class="ck__badge" src="/static/unida/bubbles/check-cap.webp" mode="aspectFit" />
		<text class="ck__title">打卡成功！</text>
		<text class="ck__sub">已连续签到 {{ streak }} 天，玩得开心</text>
	</view>
	<view class="ck__reward">
		<view class="ck__reward-ico"><image class="ck__reward-img" src="/static/icons-dark/flame.png" mode="aspectFit" /></view>
		<view class="ck__reward-info">
			<text class="ck__reward-t">签到奖励</text>
			<text class="ck__reward-s">积分已到账</text>
		</view>
		<text class="ck__reward-num">+{{ gained }}</text>
	</view>
	<view class="ck__btn" @click="goBack">完成</view>
	</view>
</template>

<script>
	export default {
		data() {
			return { statusBar: 0, gained: 5, streak: 1 };
		},
		onLoad(q) {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
			this.gained = Number(q && q.gained) || 5;
			this.streak = Number(q && q.streak) || 1;
		},
		methods: { goBack() { uni.navigateBack(); } }
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.ck { min-height: 100vh; padding: 0 40rpx 60rpx; box-sizing: border-box; }
	.ck__hero { position: relative; display: flex; flex-direction: column; align-items: center; padding-top: 140rpx; }
	.ck__spark { position: absolute; border-radius: 4rpx; transform: rotate(45deg); }
	.ck__spark--a { left: 130rpx; top: 150rpx; width: 20rpx; height: 20rpx; background: $c-sun; }
	.ck__spark--b { right: 140rpx; top: 210rpx; width: 14rpx; height: 14rpx; background: $c-primary; opacity: 0.7; }
	.ck__spark--c { right: 120rpx; top: 130rpx; width: 10rpx; height: 10rpx; background: $c-peach; opacity: 0.8; }
	.ck__badge { width: 260rpx; height: 260rpx; }
	.ck__title { margin-top: 36rpx; font-size: 44rpx; font-weight: 800; color: $c-ink; letter-spacing: 2rpx; }
	.ck__sub { margin-top: 14rpx; font-size: 26rpx; color: $t-sub; }

	.ck__reward {
		display: flex; align-items: center;
		margin-top: 70rpx;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 28rpx;
	}
	.ck__reward-ico {
		width: 84rpx; height: 84rpx;
		border-radius: 26rpx;
		background: rgba(255, 201, 79, 0.2);
		display: flex; align-items: center; justify-content: center;
	}
	.ck__reward-img { width: 44rpx; height: 44rpx; }
	.ck__reward-info { flex: 1; margin-left: 20rpx; display: flex; flex-direction: column; }
	.ck__reward-t { font-size: 28rpx; font-weight: 700; color: $t-main; }
	.ck__reward-s { margin-top: 8rpx; font-size: 23rpx; color: $t-sub; }
	.ck__reward-num { font-family: $ff-num; font-size: 44rpx; font-weight: 800; color: $c-peach; }

	.ck__btn {
		margin-top: 60rpx;
		height: 96rpx;
		border-radius: $r-pill;
		background: $g-cta;
		color: $c-white;
		font-size: 30rpx;
		font-weight: 700;
		letter-spacing: 2rpx;
		display: flex; align-items: center; justify-content: center;
		box-shadow: $sh-float;
	}
</style>
