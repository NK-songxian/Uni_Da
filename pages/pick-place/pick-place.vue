<template>
	<view class="pp unida-page">
		<view class="pp__nav"><text class="pp__back" @click="goBack">‹</text><text class="pp__title">选择地点</text><text class="pp__ph"></text></view>
		<view class="pp__search unida-card">
			<text class="pp__search-icon">🔍</text>
			<input class="pp__search-input" v-model="keyword" placeholder="搜索校园地点" />
		</view>
		<view class="pp__list unida-card">
			<view class="pp__head">
				<text class="pp__loc" @click="onLocate">📍 当前位置：主校区</text>
				<text class="pp__refresh" @click="onLocate">重新定位 ↻</text>
			</view>
			<view class="pp__item" v-for="(p, i) in filtered" :key="i" @click="onSelect(p.name)">
				<view class="pp__item-icon">{{ p.icon }}</view>
				<view class="pp__item-info">
					<text class="pp__item-name">{{ p.name }}</text>
					<text class="pp__item-addr">{{ p.addr }}</text>
				</view>
				<text class="pp__item-dist">{{ p.dist }}</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				keyword: '',
				places: [
					{ name: '中心草坪广场', addr: '阳光大学主校区中心', icon: '🌿', dist: '300m' },
					{ name: '图书馆南门', addr: '主校区图书馆', icon: '📚', dist: '600m' },
					{ name: '体育馆', addr: '主校区东区', icon: '🏀', dist: '800m' },
					{ name: '第一教学楼', addr: '主校区教学区', icon: '🏫', dist: '1.0km' }
				]
			};
		},
		computed: {
			filtered() {
				if (!this.keyword) return this.places;
				return this.places.filter(p => p.name.includes(this.keyword) || p.addr.includes(this.keyword));
			}
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onLocate() { uni.showToast({ title: '定位成功（演示）', icon: 'success' }); },
			onSelect(name) {
				uni.$emit('pickPlace', name);
				uni.navigateBack();
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.pp { padding: 0 24rpx 60rpx; }
	.pp__nav { height: 120rpx; padding-top: 60rpx; display: flex; align-items: center; justify-content: space-between; }
	.pp__back { font-size: 48rpx; width: 60rpx; }
	.pp__title { font-size: 32rpx; font-weight: 700; }
	.pp__ph { width: 60rpx; }
	.pp__search { display: flex; align-items: center; padding: 16rpx 24rpx; }
	.pp__search-icon { font-size: 32rpx; margin-right: 14rpx; }
	.pp__search-input { flex: 1; font-size: 26rpx; }
	.pp__list { margin-top: 20rpx; padding: 8rpx 24rpx; }
	.pp__head { display: flex; align-items: center; justify-content: space-between; padding: 20rpx 0; border-bottom: 2rpx solid $unida-divider; }
	.pp__loc { font-size: 26rpx; color: $unida-primary; font-weight: 600; }
	.pp__refresh { font-size: 22rpx; color: $unida-text-sub; }
	.pp__item { display: flex; align-items: center; padding: 24rpx 0; border-bottom: 2rpx solid $unida-divider; }
	.pp__item:last-child { border-bottom: none; }
	.pp__item-icon { width: 72rpx; height: 72rpx; border-radius: 20rpx; background: rgba(123,97,255,0.08); display: flex; align-items: center; justify-content: center; font-size: 36rpx; margin-right: 18rpx; }
	.pp__item-info { flex: 1; display: flex; flex-direction: column; }
	.pp__item-name { font-size: 28rpx; font-weight: 600; color: $unida-text; }
	.pp__item-addr { margin-top: 8rpx; font-size: 22rpx; color: $unida-text-sub; }
	.pp__item-dist { font-size: 24rpx; color: $unida-primary; }
</style>
