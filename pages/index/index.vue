<template>
	<view class="ix unida-page">
		<view class="ix-safe" :style="{ paddingTop: statusBar + 'px' }"></view>
		<view class="ix__glow"></view>

		<!-- 品牌 hero -->
		<view class="ix__hero">
			<view class="ix__frame">
				<image class="ix__frame-img" src="/static/unida/bubbles/frame-unida-cloud.webp" mode="aspectFit" />
				<image class="ix__badge" src="/static/unida/bubbles/brand-badge-u.webp" mode="aspectFit" />
			</view>
			<text class="ix__brand">UNIDA</text>
			<text class="ix__slogan">有你搭 · 在校园，找到同频的伙伴</text>
		</view>

		<!-- 卖点 -->
		<view class="ix__features">
			<view class="ix__feature" v-for="(f, i) in features" :key="i">
				<view class="ix__feature-icon" :class="'ix__feature-icon--' + f.tone">
					<image class="ix__feature-img" :src="f.icon" mode="aspectFit" />
				</view>
				<view class="ix__feature-info">
					<text class="ix__feature-t">{{ f.title }}</text>
					<text class="ix__feature-s">{{ f.sub }}</text>
				</view>
			</view>
		</view>

		<!-- 操作 -->
		<view class="ix__actions">
			<view class="ix__btn" @click="onStart"><text class="ix__btn-t">开启校园之旅</text></view>
			<view class="ix__sub-btn" @click="onLogin"><text class="ix__sub-btn-t">已有账号？登录</text></view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				features: [
					{ icon: '/static/icons-dark/buddy.png', title: '找搭子', sub: '自习 · 吃饭 · 运动，同频同行', tone: 'purple' },
					{ icon: '/static/icons-dark/calendar.png', title: '校园活动', sub: '讲座 · 比赛 · 舞台，不错过精彩', tone: 'orange' },
					{ icon: '/static/icons-dark/box.png', title: '生活互助', sub: '跑腿 · 代取 · 借还，同学来帮忙', tone: 'green' }
				]
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			onStart() { uni.navigateTo({ url: '/pages/login-wechat/login-wechat' }); },
			onLogin() { uni.navigateTo({ url: '/pages/phone-login/phone-login' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.ix { min-height: 100vh; padding: 0 $page-x 60rpx; box-sizing: border-box; position: relative; overflow: hidden; }
	.ix__glow {
		position: absolute;
		top: -120rpx; right: -120rpx;
		width: 480rpx; height: 480rpx;
		border-radius: 50%;
		background: radial-gradient(circle, rgba(169, 139, 255, 0.35), rgba(169, 139, 255, 0));
	}

	.ix__hero { position: relative; display: flex; flex-direction: column; align-items: center; margin-top: 80rpx; }
	.ix__frame { position: relative; width: 380rpx; height: 300rpx; display: flex; align-items: center; justify-content: center; }
	.ix__frame-img { position: absolute; width: 380rpx; height: 300rpx; }
	.ix__badge { position: relative; width: 180rpx; height: 180rpx; }
	.ix__brand { margin-top: 8rpx; font-size: 72rpx; font-weight: 800; color: $c-ink; letter-spacing: 8rpx; font-family: $ff-base; }
	.ix__slogan { margin-top: 16rpx; font-size: 26rpx; color: $t-sub; letter-spacing: 1rpx; }

	.ix__features { margin-top: 60rpx; }
	.ix__feature {
		display: flex; align-items: center;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 22rpx 24rpx;
		margin-bottom: 16rpx;
	}
	.ix__feature-icon { width: 80rpx; height: 80rpx; border-radius: 22rpx; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
	.ix__feature-icon--purple { background: rgba(128, 92, 250, 0.13); }
	.ix__feature-icon--orange { background: rgba(255, 155, 119, 0.16); }
	.ix__feature-icon--green { background: rgba(41, 202, 131, 0.14); }
	.ix__feature-img { width: 40rpx; height: 40rpx; }
	.ix__feature-info { flex: 1; margin-left: 20rpx; display: flex; flex-direction: column; min-width: 0; }
	.ix__feature-t { font-size: 28rpx; font-weight: 700; color: $t-main; }
	.ix__feature-s { margin-top: 6rpx; font-size: 22rpx; color: $t-sub; }

	.ix__actions { margin-top: 56rpx; position: relative; z-index: 2; }
	.ix__btn {
		height: 96rpx;
		border-radius: $r-pill;
		background: $g-cta;
		box-shadow: $sh-float;
		display: flex; align-items: center; justify-content: center;
	}
	.ix__btn-t { font-size: 32rpx; color: $c-white; font-weight: 700; letter-spacing: 2rpx; }
	.ix__sub-btn { margin-top: 28rpx; text-align: center; }
	.ix__sub-btn-t { font-size: 26rpx; color: $c-primary; font-weight: 600; }
</style>
