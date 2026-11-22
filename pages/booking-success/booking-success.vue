<template>
	<view class="bs unida-page">
		<!-- ══════════ 品牌成功区：U 星球 + 星光 ══════════ -->
		<view class="bs__hero" :style="{ paddingTop: (statusBar + 60) + 'px' }">
			<!-- 星光点缀（仅 transform/opacity 动画，不触发重排） -->
			<image class="bs__sp bs__sp--1" src="/static/unida/illustrations/deco-sparkle-1.png" mode="aspectFit" />
			<image class="bs__sp bs__sp--2" src="/static/unida/illustrations/deco-sparkle-2.png" mode="aspectFit" />
			<image class="bs__sp bs__sp--3" src="/static/unida/illustrations/deco-sparkle-1.png" mode="aspectFit" />

			<!-- U 星球：UNIDA 品牌 IP 承载"成功"情绪 -->
			<view class="bs__planet">
				<image class="bs__planet-img" src="/static/unida/mascot/u-planet.png" mode="aspectFit" />
			</view>

			<text class="bs__title">报名成功</text>
			<text class="bs__sub">已加入这场校园活动，期待与你相遇</text>
		</view>

		<!-- ══════════ 报名信息 ══════════ -->
		<view class="bs__card">
			<view class="bs__card-head">
				<text class="bs__card-title">报名信息</text>
				<view class="bs__badge">
					<view class="bs__badge-dot"></view>
					<text class="bs__badge-t">已报名</text>
				</view>
			</view>
			<view class="bs__row"><text class="bs__row-k">活动名称</text><text class="bs__row-v">{{ title }}</text></view>
			<view class="bs__row"><text class="bs__row-k">活动时间</text><text class="bs__row-v">{{ time }}</text></view>
			<view class="bs__row"><text class="bs__row-k">活动地点</text><text class="bs__row-v">{{ place }}</text></view>
			<view class="bs__row"><text class="bs__row-k">报名编号</text><text class="bs__row-code">{{ orderId || 'UNI 2026 1120 193' }}</text></view>
		</view>

		<!-- ══════════ 签到码（UNIDA 现场签到特色） ══════════ -->
		<view class="bs__qr-card">
			<view class="bs__qr-head">
				<view class="bs__qr-title-row">
					<image class="bs__qr-ico" src="/static/icons-dark/calendar.png" mode="aspectFit" />
					<text class="bs__qr-title">现场签到码</text>
				</view>
				<text class="bs__qr-hint">活动开始前 30 分钟生效</text>
			</view>
			<view class="bs__qr-box">
				<image class="bs__qr-img" src="/static/unida/qr/booking-qr.png" mode="aspectFit" />
			</view>
			<text class="bs__qr-tip">到场后向发起人出示此码完成签到</text>
		</view>

		<!-- ══════════ 提示 ══════════ -->
		<view class="bs__notice">
			<image class="bs__notice-ico" src="/static/icons-dark/bell.png" mode="aspectFit" />
			<text class="bs__notice-t">活动开始前会收到提醒。如需取消，请在我的报名中提前操作。</text>
		</view>

		<!-- ══════════ 操作 ══════════ -->
		<view class="bs__actions">
			<view class="bs__btn bs__btn--primary" @click="goMyOrders">
				<text class="bs__btn-t">查看我的报名</text>
			</view>
			<view class="bs__btn bs__btn--ghost" @click="goHome">
				<text class="bs__btn-t2">返回首页</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				orderId: '',
				title: '校园草地音乐会',
				time: '本周六 19:00',
				place: '中心草坪广场'
			};
		},
		onLoad(options) {
			const sys = uni.getSystemInfoSync();
			this.statusBar = (sys && sys.statusBarHeight) || 0;
			this.orderId = (options && options.orderId) || '';
			this.title = (options && options.title && decodeURIComponent(options.title)) || this.title;
			this.time = (options && options.time && decodeURIComponent(options.time)) || this.time;
			this.place = (options && options.place && decodeURIComponent(options.place)) || this.place;
		},
		methods: {
			goMyOrders() { uni.navigateTo({ url: '/pages/my-orders/my-orders' }); },
			goHome() { uni.reLaunch({ url: '/pages/home/home' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.bs { min-height: 100vh; padding-bottom: calc(60rpx + env(safe-area-inset-bottom)); }

	/* ══════════ 成功区 ══════════ */
	.bs__hero {
		position: relative;
		display: flex; flex-direction: column; align-items: center;
		padding-bottom: 56rpx;
		background: linear-gradient(180deg, #EDE4FF 0%, #F5F0FF 100%);
		border-radius: 0 0 56rpx 56rpx;
	}
	.bs__planet {
		width: 260rpx; height: 260rpx;
		display: flex; align-items: center; justify-content: center;
		animation: floaty 3.6s ease-in-out infinite;
	}
	.bs__planet-img { width: 240rpx; height: 232rpx; }
	@keyframes floaty {
		0%, 100% { transform: translateY(0); }
		50% { transform: translateY(-14rpx); }
	}
	/* 星光：仅透明度/缩放，零重排 */
	.bs__sp { position: absolute; }
	.bs__sp--1 { width: 44rpx; height: 44rpx; left: 132rpx; top: 168rpx; animation: twinkle 2.4s ease-in-out infinite; }
	.bs__sp--2 { width: 34rpx; height: 34rpx; right: 128rpx; top: 214rpx; animation: twinkle 2.8s ease-in-out 0.4s infinite; }
	.bs__sp--3 { width: 26rpx; height: 26rpx; right: 168rpx; top: 150rpx; animation: twinkle 3.2s ease-in-out 0.8s infinite; }
	@keyframes twinkle {
		0%, 100% { opacity: 0.45; transform: scale(0.86); }
		50% { opacity: 1; transform: scale(1.06); }
	}
	.bs__title {
		margin-top: 8rpx;
		font-size: $fs-h1; font-weight: $fw-bold; color: $c-ink;
		letter-spacing: 1rpx;
	}
	.bs__sub {
		margin-top: 14rpx;
		font-size: $fs-caption; color: $t-sub; letter-spacing: 0.4rpx;
	}

	/* ══════════ 信息卡 ══════════ */
	.bs__card { margin: 24rpx $page-x 0; padding: 28rpx; border-radius: $r-lg; background: #fff; box-shadow: $sh-card; }
	.bs__card-head { display: flex; align-items: center; justify-content: space-between; padding-bottom: 20rpx; border-bottom: 2rpx solid $c-line; }
	.bs__card-title { font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink; letter-spacing: -0.3rpx; }
	.bs__badge {
		display: flex; align-items: center;
		padding: 6rpx 18rpx; border-radius: $r-pill; background: rgba(41,202,131,0.12);
	}
	.bs__badge-dot { width: 12rpx; height: 12rpx; border-radius: 50%; background: $c-mint; margin-right: 8rpx; }
	.bs__badge-t { font-size: $fs-micro; font-weight: $fw-semibold; color: $c-mint; letter-spacing: 0.3rpx; }
	.bs__row { display: flex; align-items: center; justify-content: space-between; padding: 20rpx 0; border-bottom: 2rpx solid $c-line; }
	.bs__row:last-child { border-bottom: none; padding-bottom: 0; }
	.bs__row-k { font-size: $fs-body; color: $t-sub; letter-spacing: 0.2rpx; }
	.bs__row-v { font-size: $fs-body; font-weight: $fw-semibold; color: $c-ink; letter-spacing: -0.2rpx; }
	.bs__row-code { font-family: $ff-num; font-size: $fs-body; font-weight: $fw-bold; color: $c-primary; letter-spacing: 1rpx; }

	/* ══════════ 签到码卡 ══════════ */
	.bs__qr-card {
		margin: 24rpx $page-x 0; padding: 28rpx; border-radius: $r-lg;
		background: #fff; box-shadow: $sh-card;
		display: flex; flex-direction: column; align-items: center;
	}
	.bs__qr-head { width: 100%; display: flex; align-items: center; justify-content: space-between; }
	.bs__qr-title-row { display: flex; align-items: center; }
	.bs__qr-ico { width: 32rpx; height: 32rpx; }
	.bs__qr-title { margin-left: 10rpx; font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink; letter-spacing: -0.3rpx; }
	.bs__qr-hint { font-size: $fs-micro; color: $t-tertiary; }
	.bs__qr-box {
		margin-top: 26rpx; padding: 20rpx; border-radius: $r-md;
		background: #fff; border: 2rpx solid $c-line;
		box-shadow: 0 6rpx 18rpx rgba(123,97,255,0.10);
	}
	.bs__qr-img { width: 300rpx; height: 300rpx; }
	.bs__qr-tip { margin-top: 20rpx; font-size: $fs-caption; color: $t-sub; letter-spacing: 0.3rpx; }

	/* ══════════ 提示 ══════════ */
	.bs__notice {
		display: flex; align-items: flex-start; margin: 24rpx $page-x 0;
		padding: 22rpx 24rpx; border-radius: $r-md;
		background: rgba(128,92,250,0.07);
	}
	.bs__notice-ico { width: 32rpx; height: 32rpx; flex-shrink: 0; margin-top: 2rpx; opacity: 0.7; }
	.bs__notice-t { flex: 1; margin-left: 14rpx; font-size: $fs-caption; color: $c-deep; line-height: 1.62; letter-spacing: 0.2rpx; }

	/* ══════════ 操作按钮 ══════════ */
	.bs__actions { margin: 36rpx $page-x 0; }
	.bs__btn { height: 92rpx; border-radius: $r-pill; display: flex; align-items: center; justify-content: center; margin-bottom: 20rpx; }
	.bs__btn--primary { background: $g-cta; box-shadow: $sh-float; }
	.bs__btn--ghost { background: rgba(128,92,250,0.08); }
	.bs__btn-t { font-size: $fs-h3; font-weight: $fw-bold; color: #fff; letter-spacing: 2rpx; }
	.bs__btn-t2 { font-size: $fs-h3; font-weight: $fw-bold; color: $c-primary; letter-spacing: 2rpx; }
</style>
