<template>
	<view class="cal unida-page">
		<view class="cal-safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 顶栏 -->
		<view class="cal__nav">
			<view class="cal__back" @click="goBack"><image class="cal__back-img" src="/static/icons-dark/back.png" mode="aspectFit" /></view>
			<text class="cal__title">我的日程</text>
			<view class="cal__add" @click="onAdd"><image class="cal__add-img" src="/static/icons-dark/plus.png" mode="aspectFit" /></view>
		</view>

		<!-- 月历卡 -->
		<view class="cal__calendar">
			<view class="cal__month">
				<view class="cal__month-btn" @click="onPrev"><image class="cal__month-img" src="/static/icons-dark/back.png" mode="aspectFit" /></view>
				<text class="cal__month-t">{{ year }} 年 {{ month }} 月</text>
				<view class="cal__month-btn" @click="onNext"><image class="cal__month-img cal__month-img--next" src="/static/icons-dark/back.png" mode="aspectFit" /></view>
			</view>
			<view class="cal__week">
				<text class="cal__week-t" v-for="(w, i) in weeks" :key="i">{{ w }}</text>
			</view>
			<view class="cal__days">
				<view class="cal__day {{d.d === selected ? 'cal__day--on' : ''}}" v-for="(d, i) in days" :key="i" @click="onDay(i)">
					<text class="cal__day-t">{{ d.d !== 0 ? d.d : '' }}</text>
					<view class="cal__dot" v-if="d.has"></view>
				</view>
			</view>
			<view class="cal__legend">
				<view class="cal__legend-item"><view class="cal__dot cal__dot--legend"></view><text class="cal__legend-t">有日程</text></view>
				<view class="cal__legend-item"><image class="cal__legend-img" src="/static/unida/bubbles/cal-check.webp" mode="heightFix" /><text class="cal__legend-t">今日已签</text></view>
			</view>
		</view>

		<!-- 当日日程 -->
		<view class="cal__sect">
			<view class="cal__sect-head">
				<view class="cal__sect-head-l">
					<text class="cal__sect-t">{{ month }}月{{ selected }}日</text>
					<image class="cal__sect-badge" src="/static/unida/bubbles/time-now.webp" mode="heightFix" />
				</view>
				<text class="cal__sect-s">共 {{ schedules.length }} 项</text>
			</view>
			<view class="cal__item" v-for="(s, i) in schedules" :key="i">
				<view class="cal__item-line" :style="{ background: s.color }"></view>
				<view class="cal__item-body">
					<text class="cal__item-title">{{ s.title }}</text>
					<view class="cal__item-meta">
						<image class="cal__item-ico" src="/static/icons-dark/clock.png" mode="aspectFit" />
						<text class="cal__item-meta-t">{{ s.time }}</text>
					</view>
					<view class="cal__item-meta">
						<image class="cal__item-ico" src="/static/icons-dark/pin.png" mode="aspectFit" />
						<text class="cal__item-meta-t">{{ s.place }}</text>
					</view>
				</view>
				<view class="cal__status" :class="{ 'cal__status--done': s.done }"><text class="cal__status-t">{{ s.done ? '已完成' : '待进行' }}</text></view>
			</view>
			<view class="cal__empty" v-if="schedules.length === 0">
				<image class="cal__empty-img" src="/static/unida/bubbles/cal-blank.webp" mode="aspectFit" />
				<text class="cal__empty-t">这天还没有安排，去发现页找点好玩的吧</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				weeks: ['日', '一', '二', '三', '四', '五', '六'],
				year: 2026,
				month: 11,
				selected: 21,
				days: [],
				schedules: [
					{ title: '摄影分享会 · 校园风景速成', time: '15:00-16:30', place: '图书馆报告厅', color: '#805CFA', done: true },
					{ title: '预约了羽毛球场地', time: '18:30-20:00', place: '体育馆 3 号场', color: '#29CA83', done: false },
					{ title: '小组作业讨论', time: '20:00-21:00', place: '3 教 405', color: '#FF9B77', done: false }
				]
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
			this.days = this.makeDays(this.year, this.month);
		},
		methods: {
			makeDays(y, m) {
				const blank = new Date(y, m - 1, 1).getDay();
				const total = new Date(y, m, 0).getDate();
				const marks = [5, 12, 17, 20, 21, 26];
				const out = [];
				for (let k = 0; k < blank; k++) out.push({ d: 0, has: false });
				for (let n = 1; n <= total; n++) out.push({ d: n, has: marks.indexOf(n) >= 0 });
				return out;
			},
			goBack() { uni.navigateBack(); },
			onAdd() { uni.showToast({ title: '添加日程待接入', icon: 'none' }); },
			onPrev() {
				let y = this.year;
				let m = this.month - 1;
				if (m < 1) { m = 12; y = y - 1; }
				this.year = y;
				this.month = m;
				this.selected = -1;
				this.days = this.makeDays(y, m);
				this.schedules = [];
			},
			onNext() {
				let y = this.year;
				let m = this.month + 1;
				if (m > 12) { m = 1; y = y + 1; }
				this.year = y;
				this.month = m;
				this.selected = -1;
				this.days = this.makeDays(y, m);
				this.schedules = [];
			},
			onDay(i) {
				const d = this.days[i].d;
				if (d === 0) return;
				this.selected = d;
				if (d === 21) {
					this.schedules = [
						{ title: '摄影分享会 · 校园风景速成', time: '15:00-16:30', place: '图书馆报告厅', color: '#805CFA', done: true },
						{ title: '预约了羽毛球场地', time: '18:30-20:00', place: '体育馆 3 号场', color: '#29CA83', done: false },
						{ title: '小组作业讨论', time: '20:00-21:00', place: '3 教 405', color: '#FF9B77', done: false }
					];
				} else {
					this.schedules = [];
				}
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.cal { padding: 0 $page-x 60rpx; box-sizing: border-box; }

	.cal__nav { height: 110rpx; display: flex; align-items: center; justify-content: space-between; }
	.cal__back, .cal__add {
		width: 68rpx; height: 68rpx;
		background: $c-white;
		border-radius: 50%;
		box-shadow: $sh-card;
		display: flex; align-items: center; justify-content: center;
	}
	.cal__back-img, .cal__add-img { width: 32rpx; height: 32rpx; }
	.cal__title { font-size: 34rpx; font-weight: 800; color: $c-ink; letter-spacing: 1rpx; }

	.cal__calendar {
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 28rpx 20rpx;
	}
	.cal__month { display: flex; align-items: center; justify-content: space-between; }
	.cal__month-btn { width: 60rpx; height: 60rpx; display: flex; align-items: center; justify-content: center; }
	.cal__month-img { width: 30rpx; height: 30rpx; transform: rotate(180deg); }
	.cal__month-img--next { transform: rotate(0deg); }
	.cal__month-t { font-size: 32rpx; font-weight: 800; color: $c-ink; }
	.cal__week { display: flex; margin-top: 24rpx; }
	.cal__week-t { flex: 1; text-align: center; font-size: 22rpx; color: $t-sub; }
	.cal__days { display: flex; flex-wrap: wrap; margin-top: 12rpx; }
	.cal__day { width: 14.28%; height: 84rpx; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; }
	.cal__day-t { font-size: 26rpx; color: $t-main; width: 56rpx; height: 56rpx; line-height: 56rpx; text-align: center; border-radius: 50%; }
	.cal__day--empty .cal__day-t { color: transparent; }
	.cal__day--on .cal__day-t { background: $g-brand; color: $c-white; font-weight: 700; box-shadow: 0 6rpx 12rpx rgba(128, 92, 250, 0.3); }
	.cal__dot { position: absolute; bottom: 6rpx; width: 8rpx; height: 8rpx; border-radius: 50%; background: $c-peach; }
	.cal__legend { display: flex; justify-content: center; margin-top: 18rpx; padding-top: 18rpx; border-top: 2rpx solid $c-line; }
	.cal__legend-item { display: flex; align-items: center; margin: 0 20rpx; }
	.cal__dot--legend { position: static; margin-right: 8rpx; }
	.cal__legend-img { height: 28rpx; width: 40rpx; margin-right: 6rpx; }
	.cal__legend-t { font-size: 20rpx; color: $t-tertiary; }

	.cal__sect { margin-top: 28rpx; }
	.cal__sect-head { display: flex; align-items: center; justify-content: space-between; }
	.cal__sect-head-l { display: flex; align-items: center; }
	.cal__sect-t { font-size: 32rpx; font-weight: 800; color: $c-ink; }
	.cal__sect-badge { height: 40rpx; width: 72rpx; margin-left: 12rpx; }
	.cal__sect-s { font-size: 22rpx; color: $t-tertiary; font-family: $ff-num; }

	.cal__item {
		display: flex; align-items: center;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 24rpx;
		margin-top: 16rpx;
	}
	.cal__item-line { width: 8rpx; height: 88rpx; border-radius: $r-pill; margin-right: 20rpx; flex-shrink: 0; }
	.cal__item-body { flex: 1; display: flex; flex-direction: column; min-width: 0; }
	.cal__item-title { font-size: 27rpx; font-weight: 700; color: $t-main; }
	.cal__item-meta { display: flex; align-items: center; margin-top: 8rpx; }
	.cal__item-ico { width: 24rpx; height: 24rpx; opacity: 0.55; }
	.cal__item-meta-t { margin-left: 8rpx; font-size: 21rpx; color: $t-sub; font-family: $ff-num; }
	.cal__status { background: rgba(128, 92, 250, 0.12); border-radius: $r-pill; padding: 8rpx 18rpx; flex-shrink: 0; }
	.cal__status-t { font-size: 21rpx; color: $c-primary; font-weight: 600; }
	.cal__status--done { background: rgba(41, 202, 131, 0.13); }
	.cal__status--done .cal__status-t { color: #1FA86A; }

	.cal__empty { display: flex; flex-direction: column; align-items: center; padding: 60rpx 0 40rpx; }
	.cal__empty-img { width: 160rpx; height: 160rpx; }
	.cal__empty-t { margin-top: 16rpx; font-size: 24rpx; color: $t-tertiary; }
</style>
