<template>
	<view class="pm unida-page">
		<view class="pf-safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<view class="pm__nav">
			<view class="pm__back" @click="goBack"><image class="pm__back-img" src="/static/icons-dark/back.png" mode="aspectFit" /></view>
			<text class="pm__title">积分商城</text>
			<view class="pm__ph"></view>
		</view>

		<!-- 我的积分条 -->
		<view class="pm__bar" @click="goPoints">
			<view class="pm__coin"><text class="pm__coin-t">P</text></view>
			<text class="pm__bar-label">我的积分</text>
			<text class="pm__bar-num">{{ pointsText }}</text>
			<image class="pm__chev" src="/static/icons-dark/chevron.png" mode="aspectFit" />
		</view>

		<!-- 分类 -->
		<view class="pm__cats">
			<text v-for="(c, i) in cats" :key="i" class="pm__cat" :class="{ 'pm__cat--on': active === i }" @click="onCat(i)">{{ c }}</text>
		</view>

		<!-- Banner -->
		<view class="pm__banner">
			<view class="pm__banner-txt">
				<text class="pm__banner-title">积分兑换好礼</text>
				<text class="pm__banner-sub">精美礼品 · 专属特权 · 校园周边</text>
			</view>
			<image class="pm__banner-img" src="/static/unida/bubbles/board-cap.webp" mode="aspectFit" />
		</view>

		<!-- 商品网格 -->
		<view class="pm__grid">
			<view class="pm__goods" v-for="(g, i) in goods" :key="i">
				<view class="pm__goods-cover" :class="'pm__goods-cover--' + g.tone">
					<image class="pm__goods-ico" :src="g.icon" mode="aspectFit" />
				</view>
				<view class="pm__goods-body">
					<text class="pm__goods-name">{{ g.name }}</text>
					<view class="pm__goods-foot">
						<text class="pm__goods-point">{{ g.point }} 积分</text>
						<view class="pm__goods-btn" @click="onExchange(i)"><text class="pm__goods-btn-t">兑换</text></view>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import { callCloud, getToken } from '@/common/cloud.js';

	export default {
		data() {
			return {
				statusBar: 0,
				points: 0,
				exBusy: false,
				cats: ['全部', '实物礼品', '生活用品', '专属特权'],
				active: 0,
				goods: [
					{ name: '专属头像框', icon: '/static/icons-dark/bulb.png', tone: 'sky', point: 200 },
					{ name: '校园纪念徽章', icon: '/static/unida/bubbles/brand-badge-u.webp', tone: 'green', point: 400 },
					{ name: '定制帆布袋', icon: '/static/icons-dark/box.png', tone: 'purple', point: 500 },
					{ name: '免跑腿券', icon: '/static/icons-dark/heart.png', tone: 'purple', point: 600 },
					{ name: '咖啡兑换券', icon: '/static/icons-dark/clock.png', tone: 'orange', point: 800 },
					{ name: '电影票抵扣券', icon: '/static/icons-dark/music.png', tone: 'pink', point: 1500 }
				]
			};
		},
		computed: {
			pointsText() {
				return String(this.points).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
			}
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		onShow() {
			this.loadPoints();
		},
		methods: {
			goBack() { uni.navigateBack(); },
			goPoints() { uni.navigateTo({ url: '/pages/points/points' }); },
			onCat(i) { this.active = i; },
			async loadPoints() {
				try {
					const r = await callCloud('points', { action: 'home', token: getToken() });
					this.points = Number(r.points) || 0;
				} catch (e) {}
			},
			onExchange(i) {
				const g = this.goods[i];
				if (!g || this.exBusy) return;
				if (this.points < g.point) {
					uni.showToast({ title: '积分不够，还差 ' + (g.point - this.points) + ' 分', icon: 'none' });
					return;
				}
				uni.showModal({
					title: '确认兑换',
					content: '用 ' + g.point + ' 积分兑换「' + g.name + '」？',
					success: async (res) => {
						if (!res.confirm) return;
						this.exBusy = true;
						try {
							const r = await callCloud('points', {
								action: 'redeem',
								token: getToken(),
								name: g.name,
								cost: g.point
							});
							this.points = Number(r.points);
							uni.showToast({ title: '兑换成功，请到服务点领取', icon: 'success' });
						} catch (e) {
							uni.showToast({ title: (e && e.message) || '兑换失败', icon: 'none' });
						} finally {
							this.exBusy = false;
						}
					}
				});
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.pm { padding: 0 $page-x 60rpx; box-sizing: border-box; }

	.pm__nav { height: 110rpx; display: flex; align-items: center; justify-content: space-between; }
	.pm__back {
		width: 68rpx; height: 68rpx;
		background: $c-white;
		border-radius: 50%;
		box-shadow: $sh-card;
		display: flex; align-items: center; justify-content: center;
	}
	.pm__back-img { width: 32rpx; height: 32rpx; }
	.pm__title { font-size: 34rpx; font-weight: 800; color: $c-ink; letter-spacing: 1rpx; }
	.pm__ph { width: 68rpx; }

	.pm__bar {
		display: flex; align-items: center;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 24rpx 26rpx;
	}
	.pm__coin {
		width: 56rpx; height: 56rpx;
		border-radius: 50%;
		background: $g-cta;
		display: flex; align-items: center; justify-content: center;
	}
	.pm__coin-t { font-family: $ff-num; font-size: 26rpx; font-weight: 800; color: $c-white; }
	.pm__bar-label { flex: 1; margin-left: 16rpx; font-size: 26rpx; color: $t-sub; }
	.pm__bar-num { font-family: $ff-num; font-size: 34rpx; font-weight: 800; color: $c-peach; }
	.pm__chev { width: 26rpx; height: 26rpx; opacity: 0.4; margin-left: 12rpx; }

	.pm__cats { display: flex; margin: 28rpx 0 20rpx; }
	.pm__cat { font-size: 26rpx; color: $t-sub; margin-right: 36rpx; }
	.pm__cat--on { color: $c-primary; font-weight: 700; }

	.pm__banner {
		display: flex; align-items: center;
		background: $g-cta;
		border-radius: $r-md;
		padding: 30rpx 32rpx;
		box-shadow: $sh-float;
	}
	.pm__banner-txt { flex: 1; display: flex; flex-direction: column; }
	.pm__banner-title { font-size: 32rpx; font-weight: 800; color: $c-white; letter-spacing: 1rpx; }
	.pm__banner-sub { margin-top: 10rpx; font-size: 22rpx; color: rgba(255, 255, 255, 0.85); }
	.pm__banner-img { width: 110rpx; height: 110rpx; }

	.pm__grid { display: flex; flex-wrap: wrap; justify-content: space-between; margin-top: 24rpx; }
	.pm__goods {
		width: 335rpx;
		box-sizing: border-box;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		margin-bottom: 16rpx;
		overflow: hidden;
	}
	.pm__goods-cover { height: 190rpx; display: flex; align-items: center; justify-content: center; }
	.pm__goods-cover--purple { background: rgba(128, 92, 250, 0.13); }
	.pm__goods-cover--orange { background: rgba(255, 155, 119, 0.16); }
	.pm__goods-cover--green { background: rgba(41, 202, 131, 0.14); }
	.pm__goods-cover--pink { background: rgba(244, 114, 182, 0.14); }
	.pm__goods-cover--sky { background: rgba(105, 185, 245, 0.16); }
	.pm__goods-ico { width: 80rpx; height: 80rpx; opacity: 0.85; }
	.pm__goods-body { padding: 18rpx 20rpx 22rpx; }
	.pm__goods-name { font-size: 26rpx; font-weight: 700; color: $t-main; }
	.pm__goods-foot { display: flex; align-items: center; justify-content: space-between; margin-top: 14rpx; }
	.pm__goods-point { font-family: $ff-num; font-size: 24rpx; font-weight: 700; color: $c-peach; }
	.pm__goods-btn { background: $g-cta; border-radius: $r-pill; padding: 10rpx 24rpx; }
	.pm__goods-btn-t { font-size: 22rpx; color: $c-white; font-weight: 600; }
</style>
