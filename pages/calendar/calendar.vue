<template>
	<view class="cal unida-page">
		<view class="cal__nav"><text class="cal__back" @click="goBack">‹</text><text class="cal__title">我的日程</text><text class="cal__add" @click="onAdd">＋</text></view>
		<view class="cal__tabs"><text class="cal__tab cal__tab--on">日程</text><text class="cal__tab">日程列表</text></view>
		<!-- 日历 -->
		<view class="cal__calendar unida-card">
			<view class="cal__month">‹ &nbsp; 2024 年 10 月 &nbsp; ›</view>
			<view class="cal__week"><text v-for="w in weeks" :key="w">{{ w }}</text></view>
			<view class="cal__days">
				<view v-for="(d, i) in days" :key="i" class="cal__day" :class="{ 'cal__day--today': d === 17, 'cal__day--empty': d === '' }" @click="d && (selected = d)">
					<text>{{ d }}</text>
					<view v-if="d === 17 || d === 20" class="cal__dot"></view>
				</view>
			</view>
		</view>
		<!-- 当日日程 -->
		<view class="unida-section">
			<view class="unida-section__head"><text class="unida-section__title">{{ selected }} 日（今天）</text><text class="unida-section__more">共 {{ schedules.length }} 项</text></view>
			<view class="cal__item unida-card" v-for="(s, i) in schedules" :key="i">
				<view class="cal__item-line" :style="{ background: s.color }"></view>
				<view class="cal__item-body">
					<text class="cal__item-title">{{ s.title }}</text>
					<text class="cal__item-time">🕒 {{ s.time }}</text>
					<text class="cal__item-place">📍 {{ s.place }}</text>
				</view>
				<text class="cal__item-status" :class="{ 'cal__item-status--done': s.done }">{{ s.done ? '已完成' : '待进行' }}</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				weeks: ['日', '一', '二', '三', '四', '五', '六'],
				days: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
				selected: 17,
				schedules: [
					{ title: '摄影分享会 · 校园风景速成', time: '15:00-16:30', place: '图书馆报告厅', color: '#7B61FF', done: true },
					{ title: '预约了羽毛球场地', time: '18:30-20:00', place: '体育馆 3 号场', color: '#34D399', done: false },
					{ title: '小组作业讨论', time: '20:00-21:00', place: '3 教 405', color: '#FF8A3D', done: false }
				]
			};
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onAdd() { uni.showToast({ title: '添加日程待接入', icon: 'none' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.cal { padding: 0 24rpx 60rpx; }
	.cal__nav { height: 120rpx; padding-top: 60rpx; display: flex; align-items: center; justify-content: space-between; }
	.cal__back { font-size: 48rpx; width: 60rpx; }
	.cal__title { font-size: 32rpx; font-weight: 700; }
	.cal__add { font-size: 44rpx; width: 60rpx; text-align: right; color: $unida-primary; }
	.cal__tabs { display: flex; gap: 32rpx; margin: 12rpx 0 20rpx; }
	.cal__tab { font-size: 26rpx; color: $unida-text-sub; }
	.cal__tab--on { color: $unida-primary; font-weight: 700; }
	.cal__calendar { padding: 28rpx 20rpx; }
	.cal__month { text-align: center; font-size: 28rpx; font-weight: 700; color: $unida-text; }
	.cal__week { display: flex; margin-top: 24rpx; }
	.cal__week text { flex: 1; text-align: center; font-size: 22rpx; color: $unida-text-sub; }
	.cal__days { display: flex; flex-wrap: wrap; margin-top: 12rpx; }
	.cal__day { width: 14.28%; height: 76rpx; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; font-size: 26rpx; color: $unida-text; }
	.cal__day--empty { color: transparent; }
	.cal__day--today text { width: 56rpx; height: 56rpx; border-radius: 50%; background: linear-gradient(135deg,#7B61FF,#B59BFF); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 700; }
	.cal__dot { position: absolute; bottom: 6rpx; width: 8rpx; height: 8rpx; border-radius: 50%; background: $unida-orange; }
	.cal__item { display: flex; align-items: center; padding: 24rpx; margin-bottom: 16rpx; }
	.cal__item-line { width: 8rpx; height: 80rpx; border-radius: 8rpx; margin-right: 20rpx; }
	.cal__item-body { flex: 1; display: flex; flex-direction: column; }
	.cal__item-title { font-size: 28rpx; font-weight: 700; color: $unida-text; }
	.cal__item-time, .cal__item-place { margin-top: 8rpx; font-size: 22rpx; color: $unida-text-sub; }
	.cal__item-status { font-size: 22rpx; color: $unida-primary; }
	.cal__item-status--done { color: $unida-text-sub; }
</style>
