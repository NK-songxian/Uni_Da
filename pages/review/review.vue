<template>
	<view class="rv unida-page">
		<view class="rv-safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 顶栏 -->
		<view class="rv__nav">
			<view class="rv__back" @click="goBack"><image class="rv__back-img" src="/static/icons-dark/back.png" mode="aspectFit" /></view>
			<text class="rv__title">活动评价</text>
			<view class="rv__ph"></view>
		</view>

		<!-- 活动卡 -->
		<view class="rv__event">
			<view class="rv__event-cover">
				<image class="rv__event-img" src="/static/unida/bubbles/pennant-star.webp" mode="aspectFit" />
			</view>
			<view class="rv__event-info">
				<text class="rv__event-title">校园草地音乐会</text>
				<view class="rv__event-meta">
					<image class="rv__event-ico" src="/static/icons-dark/calendar.png" mode="aspectFit" />
					<text class="rv__event-meta-t">本周六 · 中心草坪</text>
				</view>
			</view>
			<image class="rv__event-badge" src="/static/unida/bubbles/label-hot.webp" mode="heightFix" />
		</view>

		<!-- 星级 -->
		<view class="rv__card">
			<text class="rv__label">整体体验</text>
			<view class="rv__stars">
				<view class="rv__star" v-for="(s, i) in stars" :key="i" :class="{ 'rv__star--on': s.on }" @click="onRate(i)"></view>
			</view>
			<text class="rv__hint">{{ ratingTexts[rating] }}</text>
		</view>

		<!-- 快速评价 -->
		<view class="rv__card">
			<text class="rv__label">快速评价 <text class="rv__label-sub">（可多选）</text></text>
			<view class="rv__tags">
				<view class="rv__tag" v-for="(t, i) in tags" :key="i" :class="{ 'rv__tag--on': t.on }" @click="onTag(i)">
					<text class="rv__tag-t">{{ t.name }}</text>
				</view>
			</view>
		</view>

		<!-- 文字评价 -->
		<view class="rv__card">
			<text class="rv__label">说说你的感受</text>
			<textarea class="rv__textarea" :value="content" placeholder="活动怎么样？有什么想说的～" maxlength="200" @input="onContent" />
			<text class="rv__count">{{ content.length }}/200</text>
		</view>

		<!-- 提交 -->
		<view class="rv__submit" @click="onSubmit"><text class="rv__submit-t">提交评价</text></view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				rating: 5,
				stars: [
					{ n: 1, on: true }, { n: 2, on: true }, { n: 3, on: true }, { n: 4, on: true }, { n: 5, on: true }
				],
				ratingTexts: ['', '很差', '一般', '还行', '不错', '超棒！'],
				tags: [
					{ name: '组织有序', on: false }, { name: '氛围超好', on: false },
					{ name: '认识新朋友', on: false }, { name: '场地不错', on: false },
					{ name: '值得一来', on: false }, { name: '下次还来', on: false }
				],
				content: ''
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onRate(i) {
				this.rating = i + 1;
				this.stars = this.stars.map((x, j) => j <= i ? { n: x.n, on: true } : { n: x.n, on: false });
			},
			onTag(i) {
				this.tags = this.tags.map((x, j) => j === i ? { name: x.name, on: !x.on } : x);
			},
			onContent(e) { this.content = e.detail.value; },
			onSubmit() {
				if (!this.content.trim()) { uni.showToast({ title: '写点评价再提交吧', icon: 'none' }); return; }
				uni.showToast({ title: '评价已提交（演示）', icon: 'success' });
				setTimeout(() => uni.navigateBack(), 1200);
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.rv { padding: 0 $page-x 60rpx; box-sizing: border-box; }

	.rv__nav { height: 110rpx; display: flex; align-items: center; justify-content: space-between; }
	.rv__back {
		width: 68rpx; height: 68rpx;
		background: $c-white;
		border-radius: 50%;
		box-shadow: $sh-card;
		display: flex; align-items: center; justify-content: center;
	}
	.rv__back-img { width: 32rpx; height: 32rpx; }
	.rv__title { font-size: 34rpx; font-weight: 800; color: $c-ink; letter-spacing: 1rpx; }
	.rv__ph { width: 68rpx; }

	.rv__event {
		display: flex; align-items: center;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 24rpx;
	}
	.rv__event-cover {
		width: 96rpx; height: 96rpx;
		border-radius: $r-sm;
		background: rgba(128, 92, 250, 0.1);
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.rv__event-img { width: 64rpx; height: 64rpx; }
	.rv__event-info { flex: 1; margin: 0 16rpx; display: flex; flex-direction: column; min-width: 0; }
	.rv__event-title { font-size: 28rpx; font-weight: 700; color: $t-main; }
	.rv__event-meta { display: flex; align-items: center; margin-top: 10rpx; }
	.rv__event-ico { width: 24rpx; height: 24rpx; opacity: 0.55; }
	.rv__event-meta-t { margin-left: 8rpx; font-size: 21rpx; color: $t-sub; }
	.rv__event-badge { height: 48rpx; width: 88rpx; flex-shrink: 0; }

	.rv__card {
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 28rpx;
		margin-top: 20rpx;
	}
	.rv__label { display: block; font-size: 30rpx; font-weight: 800; color: $c-ink; }
	.rv__label-sub { font-size: 22rpx; color: $t-tertiary; font-weight: 400; }

	.rv__stars { display: flex; justify-content: center; margin-top: 28rpx; }
	.rv__star {
		width: 68rpx; height: 68rpx;
		margin: 0 16rpx;
		background: $c-ice;
		clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
	}
	.rv__star--on { background: $c-sun; }
	.rv__hint { display: block; text-align: center; margin-top: 18rpx; font-size: 26rpx; color: $c-peach; font-weight: 700; }

	.rv__tags { display: flex; flex-wrap: wrap; margin-top: 20rpx; }
	.rv__tag {
		background: $c-mist;
		border-radius: $r-pill;
		padding: 14rpx 26rpx;
		margin: 0 16rpx 16rpx 0;
		border: 2rpx solid transparent;
		box-sizing: border-box;
	}
	.rv__tag--on { background: rgba(128, 92, 250, 0.1); border-color: $c-primary; }
	.rv__tag-t { font-size: 24rpx; color: $t-sub; }
	.rv__tag--on .rv__tag-t { color: $c-primary; font-weight: 600; }

	.rv__textarea {
		width: 100%; height: 180rpx;
		margin-top: 20rpx;
		font-size: 26rpx;
		line-height: 1.6;
		color: $t-main;
		box-sizing: border-box;
	}
	.rv__count { display: block; text-align: right; font-size: 22rpx; color: $t-tertiary; font-family: $ff-num; }

	.rv__submit {
		margin-top: 40rpx;
		height: 92rpx;
		border-radius: $r-pill;
		background: $g-cta;
		box-shadow: $sh-float;
		display: flex; align-items: center; justify-content: center;
	}
	.rv__submit-t { font-size: 30rpx; color: $c-white; font-weight: 700; letter-spacing: 2rpx; }
</style>
