<template>
	<!-- 分类入口：彩色渐变圆角块 + 线性图标，无 emoji -->
	<view class="cats">
		<view
			class="cats__item"
			v-for="(item, index) in list"
			:key="index"
			@click="onTap(item, index)"
		>
			<view class="cats__icon" :style="{ background: item.bg }">
				<view class="cats__gloss"></view>
				<image class="cats__img" :src="item.icon" mode="aspectFit" />
			</view>
			<text class="cats__label">{{ item.label }}</text>
		</view>
	</view>
</template>

<script>
	export default {
		name: 'unida-category',
		props: {
			list: { type: Array, default: () => [] }
		},
		methods: {
			onTap(item, index) {
				this.$emit('tap', { item, index });
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.cats { display: flex; flex-wrap: wrap; }
	.cats__item {
		width: 25%;
		display: flex; flex-direction: column; align-items: center;
		margin-bottom: 26rpx;
	}
	.cats__icon {
		position: relative;
		width: 100rpx; height: 100rpx;
		border-radius: 32rpx;
		display: flex; align-items: center; justify-content: center;
		border: 2rpx solid rgba(255, 255, 255, 0.75);
		box-shadow:
			0 12rpx 24rpx rgba(123, 97, 255, 0.18),
			inset 0 4rpx 0 rgba(255, 255, 255, 0.55),
			inset 0 -6rpx 12rpx rgba(0, 0, 0, 0.06);
		transition: transform 0.15s;
		overflow: hidden;
	}
	/* 顶部斜向高光，水晶玻璃质感 */
	.cats__gloss {
		position: absolute;
		top: 0; left: -20%; right: -20%;
		height: 46%;
		background: linear-gradient(180deg, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0) 100%);
		transform: rotate(-8deg);
		pointer-events: none;
	}
	.cats__img { position: relative; width: 52rpx; height: 52rpx; z-index: 2; }
	.cats__label { margin-top: 14rpx; font-size: 24rpx; color: $unida-text; }
	.cats__item:active .cats__icon { transform: scale(0.92); }
</style>
