<template>
	<view class="pm unida-page">
		<view class="pm__nav"><text class="pm__back" @click="goBack">‹</text><text class="pm__title">积分商城</text><text class="pm__ph"></text></view>
		<!-- 我的积分条 -->
		<view class="pm__bar" @click="goPoints">
			<text class="pm__bar-icon">🪙</text>
			<text class="pm__bar-label">我的积分</text>
			<text class="pm__bar-num">1,280</text>
			<text class="pm__bar-arrow">›</text>
		</view>
		<!-- 分类 -->
		<view class="pm__cats">
			<text v-for="(c, i) in cats" :key="i" class="pm__cat" :class="{ 'pm__cat--on': active === i }" @click="active = i">{{ c }}</text>
		</view>
		<!-- Banner -->
		<view class="pm__banner">
			<text class="pm__banner-title">积分兑换好礼 🎁</text>
			<text class="pm__banner-sub">精美礼品 · 专属特权 · 校园周边</text>
		</view>
		<!-- 商品网格 -->
		<view class="pm__grid">
			<view class="pm__goods" v-for="(g, i) in goods" :key="i">
				<view class="pm__goods-cover" :style="{ background: g.bg }"><text class="pm__goods-emoji">{{ g.icon }}</text></view>
				<view class="pm__goods-body">
					<text class="pm__goods-name">{{ g.name }}</text>
					<view class="pm__goods-foot"><text class="pm__goods-point">{{ g.point }} 积分</text><text class="pm__goods-btn" @click="onExchange(g)">兑换</text></view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				cats: ['全部', '实物礼品', '生活用品', '专属特权'],
				active: 0,
				goods: [
					{ name: '定制帆布袋', icon: '🛍️', point: 500, bg: 'linear-gradient(135deg,#7B61FF,#B59BFF)' },
					{ name: '咖啡兑换券', icon: '☕', point: 800, bg: 'linear-gradient(135deg,#FF8A3D,#FFD76A)' },
					{ name: '校园笔记本', icon: '📔', point: 300, bg: 'linear-gradient(135deg,#34D399,#86EFAC)' },
					{ name: '电影票抵扣', icon: '🎬', point: 1500, bg: 'linear-gradient(135deg,#F472B6,#FBCFE8)' },
					{ name: '专属头像框', icon: '🖼️', point: 200, bg: 'linear-gradient(135deg,#5B8DEF,#93C5FD)' },
					{ name: '免跑腿券', icon: '🛵', point: 600, bg: 'linear-gradient(135deg,#A78BFA,#DDD6FE)' }
				]
			};
		},
		methods: {
			goBack() { uni.navigateBack(); },
			goPoints() { uni.navigateTo({ url: '/pages/points/points' }); },
			onExchange(g) {
				uni.showModal({
					title: '确认兑换',
					content: '用 ' + g.point + ' 积分兑换「' + g.name + '」？',
					success: (res) => { if (res.confirm) uni.showToast({ title: '兑换成功（演示）', icon: 'success' }); }
				});
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.pm { padding: 0 24rpx 60rpx; }
	.pm__nav { height: 120rpx; padding-top: 60rpx; display: flex; align-items: center; justify-content: space-between; }
	.pm__back { font-size: 48rpx; width: 60rpx; }
	.pm__title { font-size: 32rpx; font-weight: 700; }
	.pm__ph { width: 60rpx; }
	.pm__bar { display: flex; align-items: center; padding: 24rpx; background: #fff; border-radius: 20rpx; box-shadow: 0 6rpx 20rpx rgba(123,97,255,0.06); }
	.pm__bar-icon { font-size: 40rpx; margin-right: 14rpx; }
	.pm__bar-label { font-size: 26rpx; color: $unida-text-sub; flex: 1; }
	.pm__bar-num { font-size: 32rpx; font-weight: 800; color: $unida-orange; }
	.pm__bar-arrow { font-size: 36rpx; color: $unida-text-sub; margin-left: 10rpx; }
	.pm__cats { display: flex; gap: 24rpx; margin: 28rpx 0 20rpx; }
	.pm__cat { font-size: 26rpx; color: $unida-text-sub; }
	.pm__cat--on { color: $unida-primary; font-weight: 700; }
	.pm__banner { border-radius: 24rpx; padding: 32rpx; background: linear-gradient(135deg,#FF8A3D,#FFD76A); display: flex; flex-direction: column; }
	.pm__banner-title { font-size: 34rpx; font-weight: 800; color: #fff; }
	.pm__banner-sub { margin-top: 8rpx; font-size: 24rpx; color: rgba(255,255,255,0.9); }
	.pm__grid { display: flex; flex-wrap: wrap; justify-content: space-between; margin-top: 24rpx; }
	.pm__goods { width: 48%; background: #fff; border-radius: 24rpx; overflow: hidden; margin-bottom: 20rpx; box-shadow: 0 8rpx 24rpx rgba(123,97,255,0.08); }
	.pm__goods-cover { height: 200rpx; display: flex; align-items: center; justify-content: center; }
	.pm__goods-emoji { font-size: 96rpx; filter: drop-shadow(0 8rpx 12rpx rgba(0,0,0,0.12)); }
	.pm__goods-body { padding: 16rpx 18rpx 20rpx; }
	.pm__goods-name { font-size: 26rpx; font-weight: 700; color: $unida-text; }
	.pm__goods-foot { display: flex; align-items: center; justify-content: space-between; margin-top: 14rpx; }
	.pm__goods-point { font-size: 24rpx; font-weight: 700; color: $unida-orange; }
	.pm__goods-btn { font-size: 22rpx; color: #fff; background: linear-gradient(135deg,#7B61FF,#B59BFF); padding: 10rpx 22rpx; border-radius: 999rpx; }
</style>
