<template>
	<view class="mo unida-page">
		<!-- ══════════ 自绘顶栏 ══════════ -->
		<view class="mo__nav" :style="{ paddingTop: statusBar + 'px' }">
			<view class="mo__nav-btn" @click="goBack">
				<image class="mo__nav-ico" src="/static/icons-dark/back.png" mode="aspectFit" />
			</view>
			<text class="mo__nav-title">我的报名</text>
			<view class="mo__nav-btn"></view>
		</view>

		<!-- ══════════ 品牌头部：日历星球 + DIN 统计 ══════════ -->
		<view class="mo__hero">
			<image class="mo__hero-img" src="/static/unida/planet/planet-cal.png" mode="aspectFit" />
			<view class="mo__hero-info">
				<text class="mo__hero-title">我的报名</text>
				<view class="mo__hero-stats">
					<view class="mo__stat">
						<text class="mo__stat-n">{{ total }}</text>
						<text class="mo__stat-k">全部</text>
					</view>
					<view class="mo__stat-divider"></view>
					<view class="mo__stat">
						<text class="mo__stat-n">{{ countOngoing }}</text>
						<text class="mo__stat-k">进行中</text>
					</view>
					<view class="mo__stat-divider"></view>
					<view class="mo__stat">
						<text class="mo__stat-n">{{ countDone }}</text>
						<text class="mo__stat-k">已完成</text>
					</view>
				</view>
			</view>
		</view>

		<!-- ══════════ 状态筛选胶囊 ══════════ -->
		<view class="mo__tabs">
			<view
				v-for="(t, i) in tabs"
				:key="i"
				class="mo__tab"
				:class="{ 'mo__tab--on': active === i }"
				@click="onTab(i)"
			>
				<text class="mo__tab-t">{{ t.label }}</text>
			</view>
		</view>

		<!-- ══════════ 报名列表 ══════════ -->
		<view class="mo__list">
			<view class="mo__order" v-for="(o, i) in ordersShow" :key="o.id">
				<view class="mo__order-head">
					<view class="mo__order-type">
						<image class="mo__type-ico" :src="o.typeIcon" mode="aspectFit" />
						<text class="mo__type-t">{{ o.type }}</text>
					</view>
					<view class="mo__status" :class="'mo__status--' + o.statusKey">
						<view class="mo__status-dot"></view>
						<text class="mo__status-t">{{ o.status }}</text>
					</view>
				</view>
				<text class="mo__order-title">{{ o.title }}</text>
				<view class="mo__order-meta">
					<image class="mo__meta-ico" src="/static/icons-dark/clock.png" mode="aspectFit" />
					<text class="mo__meta-t">{{ o.time }}</text>
					<image class="mo__meta-ico mo__meta-ico--pin" src="/static/icons-dark/pin.png" mode="aspectFit" />
					<text class="mo__meta-t">{{ o.place }}</text>
				</view>
				<view class="mo__order-foot">
					<text class="mo__order-price" :class="{ 'mo__order-price--free': o.price === '0' }">
						{{ o.price === '0' ? '免费' : '¥' + o.price }}
					</text>
					<view class="mo__order-actions">
						<text v-if="o.statusKey === 'ongoing'" class="mo__order-btn mo__order-btn--ghost" @click="onTrack(o)">查看进度</text>
						<text v-if="o.statusKey === 'done'" class="mo__order-btn" @click="onReview(o)">去评价</text>
						<text v-if="o.statusKey === 'wait'" class="mo__order-btn" @click="onConfirm(o)">确认完成</text>
					</view>
				</view>
			</view>

			<!-- ══════════ 品牌空态：气泡星球 ══════════ -->
			<view class="mo__empty" v-if="ordersShow.length === 0">
				<image class="mo__empty-img" src="/static/unida/planet/planet-bubble.png" mode="aspectFit" />
				<text class="mo__empty-t">这里还空空的</text>
				<text class="mo__empty-sub">去发现页搭个伴吧</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				active: 0,
				ordersShow: [],
				tabs: [
					{ label: '全部', key: 'all' },
					{ label: '待进行', key: 'wait' },
					{ label: '进行中', key: 'ongoing' },
					{ label: '已完成', key: 'done' }
				],
				orders: [
					{ id: 1, typeIcon: '/static/icons-dark/box.png', type: '跑腿服务', title: '帮忙取快递（中通北区驿站）', time: '今天 18:00 前', place: '北区驿站', price: '8', status: '待接单', statusKey: 'wait' },
					{ id: 2, typeIcon: '/static/icons-dark/music.png', type: '校园活动', title: '校园草地音乐会', time: '本周六 19:00', place: '中心草坪广场', price: '0', status: '进行中', statusKey: 'ongoing' },
					{ id: 3, typeIcon: '/static/icons-dark/box.png', type: '跑腿服务', title: '代拿外卖到宿舍楼下', time: '昨天', place: '东门', price: '5', status: '已完成', statusKey: 'done' }
				]
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = (sys && sys.statusBarHeight) || 0;
			this.ordersShow = this.orders.slice();
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onTab(i) {
				this.active = i;
				const key = this.tabs[i].key;
				this.ordersShow = key === 'all' ? this.orders.slice() : this.orders.filter(o => o.statusKey === key);
			},
			onTrack() { uni.navigateTo({ url: '/pages/errand-detail/errand-detail' }); },
			onReview() { uni.navigateTo({ url: '/pages/review/review' }); },
			onConfirm() { uni.showToast({ title: '已确认完成（演示）', icon: 'success' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.mo { padding-bottom: calc(60rpx + env(safe-area-inset-bottom)); }

	/* ══════════ 顶栏 ══════════ */
	.mo__nav {
		display: flex; align-items: center; justify-content: space-between;
		padding-left: $page-x; padding-right: $page-x; padding-bottom: 16rpx;
	}
	.mo__nav-btn { width: 64rpx; height: 64rpx; display: flex; align-items: center; justify-content: center; }
	.mo__nav-ico { width: 40rpx; height: 40rpx; }
	.mo__nav-title { font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink; letter-spacing: 0.5rpx; }

	/* ══════════ 品牌头部 ══════════ */
	.mo__hero {
		display: flex; align-items: center;
		margin: 8rpx $page-x 0; padding: 24rpx 28rpx;
		border-radius: $r-lg; background: #fff; box-shadow: $sh-card;
	}
	.mo__hero-img { width: 150rpx; height: 150rpx; flex-shrink: 0; }
	.mo__hero-info { flex: 1; margin-left: 20rpx; }
	.mo__hero-title {
		display: block;
		font-size: $fs-h2; font-weight: $fw-bold; color: $c-ink; letter-spacing: -0.8rpx;
	}
	.mo__hero-stats { display: flex; align-items: center; margin-top: 18rpx; }
	.mo__stat { display: flex; flex-direction: column; align-items: center; margin-right: 28rpx; }
	.mo__stat-n { font-family: $ff-num; font-size: $fs-h2; font-weight: $fw-bold; color: $c-primary; line-height: 1.1; }
	.mo__stat-k { margin-top: 4rpx; font-size: $fs-micro; color: $t-sub; letter-spacing: 0.3rpx; }
	.mo__stat-divider { width: 2rpx; height: 52rpx; background: $c-line; margin-right: 28rpx; }

	/* ══════════ 状态胶囊 ══════════ */
	.mo__tabs { display: flex; margin: 24rpx $page-x 0; }
	.mo__tab {
		padding: 12rpx 28rpx; border-radius: $r-pill; margin-right: 14rpx;
		background: #fff; box-shadow: $sh-card;
		transition: background 0.2s ease;
	}
	.mo__tab--on { background: $g-brand; }
	.mo__tab--on .mo__tab-t { color: #fff; font-weight: $fw-bold; }
	.mo__tab-t { font-size: $fs-caption; color: $t-sub; letter-spacing: 0.3rpx; }

	/* ══════════ 报名卡 ══════════ */
	.mo__order {
		margin: 24rpx $page-x 0; padding: 26rpx 28rpx;
		border-radius: $r-lg; background: #fff; box-shadow: $sh-card;
	}
	.mo__order-head { display: flex; align-items: center; justify-content: space-between; }
	.mo__order-type { display: flex; align-items: center; }
	.mo__type-ico {
		width: 44rpx; height: 44rpx; border-radius: 14rpx;
		background: rgba(128,92,250,0.10);
		display: flex; align-items: center; justify-content: center;
	}
	.mo__type-t { margin-left: 12rpx; font-size: $fs-micro; color: $t-sub; letter-spacing: 0.3rpx; }
	.mo__status { display: flex; align-items: center; padding: 6rpx 16rpx; border-radius: $r-pill; }
	.mo__status-dot { width: 10rpx; height: 10rpx; border-radius: 50%; margin-right: 8rpx; }
	.mo__status-t { font-size: $fs-micro; font-weight: $fw-semibold; letter-spacing: 0.3rpx; }
	.mo__status--wait { background: rgba(255,155,119,0.14); }
	.mo__status--wait .mo__status-dot { background: $c-peach; }
	.mo__status--wait .mo__status-t { color: $c-peach; }
	.mo__status--ongoing { background: rgba(128,92,250,0.10); }
	.mo__status--ongoing .mo__status-dot { background: $c-primary; }
	.mo__status--ongoing .mo__status-t { color: $c-primary; }
	.mo__status--done { background: rgba(41,202,131,0.12); }
	.mo__status--done .mo__status-dot { background: $c-mint; }
	.mo__status--done .mo__status-t { color: $c-mint; }
	.mo__order-title {
		display: block; margin-top: 18rpx;
		font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink;
		letter-spacing: -0.3rpx; line-height: 1.4;
	}
	.mo__order-meta { display: flex; align-items: center; margin-top: 14rpx; }
	.mo__meta-ico { width: 24rpx; height: 24rpx; opacity: 0.45; flex-shrink: 0; }
	.mo__meta-ico--pin { margin-left: 24rpx; }
	.mo__meta-t { margin-left: 8rpx; font-size: $fs-micro; color: $t-sub; letter-spacing: 0.2rpx; }
	.mo__order-foot {
		display: flex; align-items: center; justify-content: space-between;
		margin-top: 22rpx; padding-top: 20rpx; border-top: 2rpx solid $c-line;
	}
	.mo__order-price { font-family: $ff-num; font-size: $fs-h3; font-weight: $fw-bold; color: $c-peach; }
	.mo__order-price--free { color: $c-mint; font-size: $fs-body; letter-spacing: 0.5rpx; }
	.mo__order-actions { display: flex; }
	.mo__order-btn {
		font-size: $fs-caption; font-weight: $fw-semibold;
		color: #fff; background: $g-cta;
		padding: 12rpx 30rpx; border-radius: $r-pill;
		box-shadow: 0 6rpx 16rpx rgba(123,97,255,0.22);
	}
	.mo__order-btn--ghost { background: rgba(128,92,250,0.08); color: $c-primary; box-shadow: none; }

	/* ══════════ 品牌空态 ══════════ */
	.mo__empty { display: flex; flex-direction: column; align-items: center; padding: 80rpx 0 40rpx; }
	.mo__empty-img { width: 300rpx; height: 300rpx; }
	.mo__empty-t { margin-top: 12rpx; font-size: $fs-body; font-weight: $fw-semibold; color: $t-sub; letter-spacing: 0.5rpx; }
	.mo__empty-sub { margin-top: 10rpx; font-size: $fs-caption; color: $t-tertiary; letter-spacing: 0.3rpx; }
</style>
