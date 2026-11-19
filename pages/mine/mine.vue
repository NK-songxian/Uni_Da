<template>
	<view class="mine unida-page unida-page--tab">
		<!-- 头部渐变 + 用户信息 -->
		<view class="mine__hero">
			<view class="mine__blob"></view>
			<view class="mine__top">
				<text class="mine__title">我的</text>
				<text class="mine__setting" @click="onSetting">⚙️</text>
			</view>
			<view class="mine__user" @click="onEditProfile">
				<view class="mine__avatar">😄</view>
				<view class="mine__info">
					<text class="mine__name">校园小伙伴</text>
					<text class="mine__school">🎓 阳光大学 · 已认证</text>
				</view>
				<text class="mine__arrow">›</text>
			</view>
		</view>

		<!-- 积分卡 -->
		<view class="mine__points unida-card">
			<view class="mine__points-left">
				<text class="mine__points-label">我的积分</text>
				<text class="mine__points-num">2,480 <text class="mine__points-unit">分</text></text>
			</view>
			<view class="mine__points-badge">🥇 Lv.6 活力达人</view>
			<view class="mine__points-btn" @click="onPoints">去签到 +5 →</view>
		</view>

		<!-- 数据概览 -->
		<view class="mine__stats unida-card">
			<view class="mine__stat" v-for="(s, i) in stats" :key="i" @click="onStat(s)">
				<text class="mine__stat-num">{{ s.num }}</text>
				<text class="mine__stat-label">{{ s.label }}</text>
			</view>
		</view>

		<!-- 功能列表 -->
		<view class="mine__group unida-card">
			<view class="mine__row" v-for="(r, i) in rows" :key="i" @click="onRow(r)">
				<text class="mine__row-icon">{{ r.icon }}</text>
				<text class="mine__row-label">{{ r.label }}</text>
				<text v-if="r.tip" class="mine__row-tip">{{ r.tip }}</text>
				<text class="mine__row-arrow">›</text>
			</view>
		</view>

		<unida-tabbar :current="4" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';

	export default {
		components: { unidaTabbar },
		data() {
			return {
				stats: [
					{ num: 6, label: '我的发布' },
					{ num: 12, label: '我的搭子' },
					{ num: 8, label: '我的预约' },
					{ num: 3, label: '收藏' }
				],
				rows: [
					{ icon: '🎓', label: '校园认证', tip: '已认证' },
					{ icon: '📋', label: '我的订单' },
					{ icon: '⭐', label: '我的评价' },
					{ icon: '🏅', label: '我的勋章' },
					{ icon: '👥', label: '我的关注' },
					{ icon: '🛡️', label: '隐私管理' },
					{ icon: '❓', label: '举报与反馈' }
				]
			};
		},
		methods: {
			onSetting() { uni.showToast({ title: '设置待开发', icon: 'none' }); },
			onEditProfile() { uni.showToast({ title: '编辑资料待开发', icon: 'none' }); },
			onPoints() { uni.showToast({ title: '积分中心待开发', icon: 'none' }); },
			onStat(s) { uni.showToast({ title: s.label + ' 待开发', icon: 'none' }); },
			onRow(r) { uni.showToast({ title: r.label + ' 待开发', icon: 'none' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.mine__hero {
		position: relative;
		padding: 60rpx 32rpx 80rpx;
		background: linear-gradient(135deg, #7B61FF, #B59BFF);
		border-radius: 0 0 44rpx 44rpx;
		overflow: hidden;
	}
	.mine__blob {
		position: absolute;
		right: -60rpx;
		top: -40rpx;
		width: 260rpx;
		height: 260rpx;
		border-radius: 50%;
		background: rgba(255,255,255,0.15);
	}
	.mine__top { display: flex; align-items: center; justify-content: space-between; position: relative; }
	.mine__title { font-size: 44rpx; font-weight: 800; color: #fff; }
	.mine__setting { font-size: 40rpx; }
	.mine__user { display: flex; align-items: center; margin-top: 44rpx; position: relative; }
	.mine__avatar {
		width: 120rpx;
		height: 120rpx;
		border-radius: 50%;
		background: #fff;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 64rpx;
		border: 4rpx solid rgba(255,255,255,0.6);
		margin-right: 24rpx;
	}
	.mine__info { flex: 1; display: flex; flex-direction: column; }
	.mine__name { font-size: 36rpx; font-weight: 800; color: #fff; }
	.mine__school { margin-top: 10rpx; font-size: 24rpx; color: rgba(255,255,255,0.9); }
	.mine__arrow { font-size: 48rpx; color: #fff; }

	.mine__points {
		margin: -48rpx 24rpx 0;
		position: relative;
		display: flex;
		align-items: center;
		flex-wrap: wrap;
	}
	.mine__points-left { display: flex; flex-direction: column; }
	.mine__points-label { font-size: 24rpx; color: $unida-text-sub; }
	.mine__points-num { font-size: 44rpx; font-weight: 800; color: $unida-orange; }
	.mine__points-unit { font-size: 24rpx; }
	.mine__points-badge {
		margin-left: auto;
		font-size: 22rpx;
		color: #a97b12;
		background: rgba(255,215,106,0.3);
		padding: 10rpx 18rpx;
		border-radius: 999rpx;
	}
	.mine__points-btn {
		width: 100%;
		margin-top: 20rpx;
		text-align: center;
		padding: 18rpx;
		border-radius: 16rpx;
		background: rgba(123,97,255,0.08);
		color: $unida-primary;
		font-size: 26rpx;
		font-weight: 600;
	}

	.mine__stats { display: flex; margin: 20rpx 24rpx; padding: 28rpx 0; }
	.mine__stat { flex: 1; display: flex; flex-direction: column; align-items: center; }
	.mine__stat-num { font-size: 36rpx; font-weight: 800; color: $unida-primary; }
	.mine__stat-label { margin-top: 8rpx; font-size: 22rpx; color: $unida-text-sub; }

	.mine__group { margin: 20rpx 24rpx; padding: 8rpx 24rpx; }
	.mine__row { display: flex; align-items: center; padding: 24rpx 0; border-bottom: 2rpx solid $unida-divider; }
	.mine__row:last-child { border-bottom: none; }
	.mine__row-icon { font-size: 36rpx; margin-right: 20rpx; }
	.mine__row-label { flex: 1; font-size: 28rpx; color: $unida-text; }
	.mine__row-tip { font-size: 22rpx; color: $unida-green; margin-right: 12rpx; }
	.mine__row-arrow { font-size: 36rpx; color: $unida-text-sub; }
</style>
