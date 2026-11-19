<template>
	<view class="search" @click="onTap">
		<image class="search__icon" src="/static/icons/search.png" mode="aspectFit" />
		<text class="search__ph">{{ placeholder }}</text>
		<view class="search__btn">搜索</view>
	</view>
</template>

<script>
	export default {
		name: 'unida-search',
		props: {
			placeholder: { type: String, default: '搜搭子、活动、话题…' }
		},
		methods: {
			onTap() {
				this.$emit('focus');
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.search {
		height: 80rpx;
		border-radius: 999rpx;
		background: #fff;
		display: flex;
		align-items: center;
		padding: 0 8rpx 0 24rpx;
		box-shadow: 0 8rpx 26rpx rgba(123, 97, 255, 0.10);
	}
	.search__icon {
		width: 32rpx; height: 32rpx;
		margin-right: 14rpx;
		opacity: 0.55;
	}
	.search__ph {
		flex: 1;
		font-size: 26rpx;
		color: $unida-text-sub;
	}
	.search__btn {
		padding: 14rpx 30rpx;
		border-radius: 999rpx;
		background: linear-gradient(135deg, $unida-primary 0%, $unida-primary-light 100%);
		color: #fff;
		font-size: 26rpx;
		font-weight: 600;
		box-shadow: 0 6rpx 16rpx rgba(123, 97, 255, 0.28);
	}
</style>
