<template>
	<view class="eh unida-page unida-page--tab">
		<view class="eh__top">
			<text class="eh__title">跑腿大厅</text>
			<unida-search placeholder="搜索跑腿需求（快递、外卖…）" @focus="onSearch" />
		</view>
		<!-- 快捷分类 -->
		<view class="eh__cats">
			<view class="eh__cat" v-for="(c, i) in cats" :key="i" @click="onCat(c)">
				<view class="eh__cat-icon" :style="{ background: c.bg }">{{ c.icon }}</view>
				<text class="eh__cat-label">{{ c.label }}</text>
			</view>
		</view>
		<!-- 发布跑腿 CTA -->
		<view class="eh__cta" @click="onPublish">
			<text class="eh__cta-icon">🛵</text>
			<view class="eh__cta-info"><text class="eh__cta-title">需要帮忙？发布跑腿需求</text><text class="eh__cta-sub">同学接单，快速搞定</text></view>
			<text class="eh__cta-btn">去发布 ›</text>
		</view>
		<!-- 需求列表 -->
		<view class="unida-section">
			<view class="unida-section__head"><text class="unida-section__title">附近需求</text><text class="unida-section__more">{{ orders.length }} 个待接单</text></view>
			<view class="eh__item unida-card" v-for="(o, i) in orders" :key="i" @click="onOrder(o)">
				<view class="eh__item-head">
					<text class="unida-tag unida-tag--purple">{{ o.type }}</text>
					<text class="eh__item-reward">¥{{ o.reward }}</text>
				</view>
				<text class="eh__item-title">{{ o.title }}</text>
				<view class="eh__item-meta">
					<text>📍 {{ o.from }} → {{ o.to }}</text>
					<text>🕒 {{ o.time }}</text>
				</view>
				<view class="eh__item-foot">
					<view class="eh__item-user"><text class="eh__item-avatar">{{ o.avatar }}</text><text>{{ o.user }} · {{ o.dorm }}</text></view>
					<view class="eh__item-btn">立即接单</view>
				</view>
			</view>
		</view>
		<unida-tabbar :current="1" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';
	import unidaSearch from '@/components/unida-search/unida-search.vue';
	export default {
		components: { unidaTabbar, unidaSearch },
		data() {
			return {
				cats: [
					{ label: '快递代取', icon: '📦', bg: 'linear-gradient(135deg,#7B61FF,#B59BFF)' },
					{ label: '外卖代拿', icon: '🍜', bg: 'linear-gradient(135deg,#FF8A3D,#FFD76A)' },
					{ label: '物品代送', icon: '🎁', bg: 'linear-gradient(135deg,#F472B6,#FBCFE8)' },
					{ label: '其他互助', icon: '🙌', bg: 'linear-gradient(135deg,#34D399,#86EFAC)' }
				],
				orders: [
					{ type: '快递代取', reward: '8', title: '帮忙取个快递（中通北区驿站）', from: '北区驿站', to: '东园3栋', time: '今天 18:00 前', avatar: '😄', user: '阿星', dorm: '东园3栋' },
					{ type: '外卖代拿', reward: '5', title: '一楼拿外卖送到宿舍楼下', from: '东门', to: '西园1栋', time: '现在', avatar: '🤩', user: '小林', dorm: '西园1栋' },
					{ type: '物品代送', reward: '12', title: '帮忙送一份资料到教学楼', from: '图书馆', to: '3教201', time: '明天 8:00', avatar: '😎', user: 'Leo', dorm: '南园5栋' }
				]
			};
		},
		methods: {
			onSearch() { uni.showToast({ title: '搜索待接入', icon: 'none' }); },
			onCat(c) { uni.showToast({ title: c.label + ' 分类', icon: 'none' }); },
			onPublish() { uni.showToast({ title: '发布跑腿待接入', icon: 'none' }); },
			onOrder(o) { uni.navigateTo({ url: '/pages/errand-detail/errand-detail' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.eh__top { padding: 60rpx 24rpx 0; }
	.eh__title { display: block; font-size: 44rpx; font-weight: 800; color: $unida-text; margin-bottom: 24rpx; }
	.eh__cats { display: flex; padding: 32rpx 24rpx 8rpx; }
	.eh__cat { flex: 1; display: flex; flex-direction: column; align-items: center; }
	.eh__cat-icon { width: 100rpx; height: 100rpx; border-radius: 30rpx; display: flex; align-items: center; justify-content: center; font-size: 48rpx; box-shadow: 0 8rpx 20rpx rgba(123,97,255,0.14); }
	.eh__cat-label { margin-top: 14rpx; font-size: 24rpx; color: $unida-text; }
	.eh__cta { display: flex; align-items: center; margin: 28rpx 24rpx 0; padding: 24rpx; background: linear-gradient(135deg,#7B61FF,#B59BFF); border-radius: 24rpx; box-shadow: 0 10rpx 24rpx rgba(123,97,255,0.24); }
	.eh__cta-icon { font-size: 56rpx; margin-right: 18rpx; }
	.eh__cta-info { flex: 1; display: flex; flex-direction: column; }
	.eh__cta-title { font-size: 28rpx; font-weight: 700; color: #fff; }
	.eh__cta-sub { margin-top: 6rpx; font-size: 22rpx; color: rgba(255,255,255,0.85); }
	.eh__cta-btn { font-size: 24rpx; color: #fff; background: rgba(255,255,255,0.25); padding: 12rpx 22rpx; border-radius: 999rpx; }
	.eh__item { padding: 24rpx; }
	.eh__item-head { display: flex; align-items: center; justify-content: space-between; }
	.eh__item-reward { font-size: 36rpx; font-weight: 800; color: $unida-orange; }
	.eh__item-title { display: block; margin-top: 16rpx; font-size: 30rpx; font-weight: 700; color: $unida-text; }
	.eh__item-meta { display: flex; flex-direction: column; gap: 10rpx; margin-top: 16rpx; }
	.eh__item-meta text { font-size: 24rpx; color: $unida-text-sub; }
	.eh__item-foot { display: flex; align-items: center; justify-content: space-between; margin-top: 20rpx; padding-top: 18rpx; border-top: 2rpx solid $unida-divider; }
	.eh__item-user { display: flex; align-items: center; font-size: 24rpx; color: $unida-text-sub; }
	.eh__item-avatar { font-size: 32rpx; margin-right: 10rpx; }
	.eh__item-btn { font-size: 24rpx; color: #fff; background: linear-gradient(135deg,#7B61FF,#B59BFF); padding: 12rpx 28rpx; border-radius: 999rpx; }
</style>
