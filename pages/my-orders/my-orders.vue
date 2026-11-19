<template>
	<view class="mo unida-page">
		<view class="mo__nav"><text class="mo__back" @click="goBack">‹</text><text class="mo__title">我的订单</text><text class="mo__ph"></text></view>
		<!-- 状态筛选 -->
		<view class="mo__tabs">
			<text v-for="(t, i) in tabs" :key="i" class="mo__tab" :class="{ 'mo__tab--on': active === i }" @click="active = i">{{ t }}</text>
		</view>
		<!-- 订单列表 -->
		<view class="mo__list">
			<view class="mo__order unida-card" v-for="(o, i) in orders" :key="i">
				<view class="mo__order-head">
					<view class="mo__order-type"><text class="mo__order-icon">{{ o.icon }}</text><text>{{ o.type }}</text></view>
					<text class="mo__order-status" :class="'mo__order-status--' + o.statusKey">{{ o.status }}</text>
				</view>
				<text class="mo__order-title">{{ o.title }}</text>
				<view class="mo__order-meta"><text>{{ o.time }}</text><text>{{ o.place }}</text></view>
				<view class="mo__order-foot">
					<text class="mo__order-price">¥{{ o.price }}</text>
					<view class="mo__order-actions">
						<text v-if="o.statusKey === 'ongoing'" class="mo__order-btn mo__order-btn--ghost" @click="onTrack(o)">查看进度</text>
						<text v-if="o.statusKey === 'done'" class="mo__order-btn" @click="onReview(o)">去评价</text>
						<text v-if="o.statusKey === 'wait'" class="mo__order-btn" @click="onConfirm(o)">确认完成</text>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				tabs: ['待进行', '进行中', '已完成', '全部'],
				active: 0,
				orders: [
					{ icon: '🛵', type: '跑腿服务', title: '帮忙取快递（中通北区驿站）', time: '今天 18:00 前', place: '北区驿站→东园3栋', price: '8', status: '待接单', statusKey: 'wait' },
					{ icon: '🎪', type: '活动预约', title: '校园草地音乐会', time: '本周六 19:00', place: '中心草坪广场', price: '0', status: '进行中', statusKey: 'ongoing' },
					{ icon: '📦', type: '跑腿服务', title: '代拿外卖到宿舍楼下', time: '昨天', place: '东门→西园1栋', price: '5', status: '已完成', statusKey: 'done' }
				]
			};
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onTrack() { uni.navigateTo({ url: '/pages/errand-detail/errand-detail' }); },
			onReview() { uni.navigateTo({ url: '/pages/review/review' }); },
			onConfirm() { uni.showToast({ title: '已确认完成（演示）', icon: 'success' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.mo { padding: 0 24rpx 60rpx; }
	.mo__nav { height: 120rpx; padding-top: 60rpx; display: flex; align-items: center; justify-content: space-between; }
	.mo__back { font-size: 48rpx; width: 60rpx; }
	.mo__title { font-size: 32rpx; font-weight: 700; }
	.mo__ph { width: 60rpx; }
	.mo__tabs { display: flex; gap: 40rpx; padding: 12rpx 0 24rpx; }
	.mo__tab { font-size: 28rpx; color: $unida-text-sub; padding-bottom: 12rpx; }
	.mo__tab--on { color: $unida-primary; font-weight: 700; border-bottom: 6rpx solid $unida-primary; border-radius: 6rpx; }
	.mo__order { margin-bottom: 20rpx; }
	.mo__order-head { display: flex; align-items: center; justify-content: space-between; padding-bottom: 16rpx; border-bottom: 2rpx solid $unida-divider; }
	.mo__order-type { display: flex; align-items: center; font-size: 24rpx; color: $unida-text-sub; }
	.mo__order-icon { font-size: 32rpx; margin-right: 10rpx; }
	.mo__order-status { font-size: 24rpx; font-weight: 600; }
	.mo__order-status--wait { color: $unida-orange; }
	.mo__order-status--ongoing { color: $unida-primary; }
	.mo__order-status--done { color: $unida-text-sub; }
	.mo__order-title { display: block; margin-top: 18rpx; font-size: 28rpx; font-weight: 700; color: $unida-text; }
	.mo__order-meta { display: flex; gap: 24rpx; margin-top: 12rpx; font-size: 22rpx; color: $unida-text-sub; }
	.mo__order-foot { display: flex; align-items: center; justify-content: space-between; margin-top: 20rpx; padding-top: 18rpx; border-top: 2rpx solid $unida-divider; }
	.mo__order-price { font-size: 32rpx; font-weight: 800; color: $unida-orange; }
	.mo__order-actions { display: flex; gap: 16rpx; }
	.mo__order-btn { font-size: 24rpx; color: #fff; background: linear-gradient(135deg,#7B61FF,#B59BFF); padding: 12rpx 26rpx; border-radius: 999rpx; }
	.mo__order-btn--ghost { background: rgba(123,97,255,0.08); color: $unida-primary; }
</style>
