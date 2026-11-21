<template>
	<view class="uh unida-page">
		<view class="uh-safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 渐变 hero -->
		<view class="uh__hero">
			<view class="uh__nav">
				<view class="uh__nav-btn" @click="goBack"><image class="uh__nav-img" src="/static/icons-dark/back.png" mode="aspectFit" /></view>
				<text class="uh__nav-title">个人主页</text>
				<view class="uh__nav-btn" @click="onMore"><image class="uh__nav-img" src="/static/icons-dark/bell.png" mode="aspectFit" /></view>
			</view>
			<view class="uh__profile">
				<view class="uh__avatar"><text class="uh__avatar-ch">星</text></view>
				<view class="uh__info">
					<view class="uh__name-row">
						<text class="uh__name">阿星</text>
						<image class="uh__shield" src="/static/unida/bubbles/shield-check.webp" mode="heightFix" />
					</view>
					<text class="uh__sub">阳光大学 · 已认证 <text class="uh__dot">·</text> <text class="uh__score">4.9</text> 分</text>
				</view>
			</view>
			<text class="uh__bio">热爱运动，喜欢认识新朋友～ 一起让校园生活更有趣！</text>
		</view>

		<!-- 数据统计 -->
		<view class="uh__stats">
			<view class="uh__stat" v-for="(s, i) in stats" :key="i">
				<text class="uh__stat-num">{{ s.num }}</text>
				<text class="uh__stat-label">{{ s.label }}</text>
			</view>
		</view>

		<!-- 操作 -->
		<view class="uh__actions">
			<view class="uh__btn uh__btn--primary" @click="onChat">
				<image class="uh__btn-img" src="/static/icons-dark/message.png" mode="aspectFit" />
				<text class="uh__btn-t">私信</text>
			</view>
			<view class="uh__btn {{following ? 'uh__btn--ghost' : 'uh__btn--outline'}}" @click="onFollow">
				<text class="uh__btn-t">{{ following ? '已关注' : '+ 关注' }}</text>
			</view>
		</view>

		<!-- 兴趣标签 -->
		<view class="uh__sect">
			<text class="uh__sect-t">兴趣标签</text>
			<view class="uh__tags">
				<image class="uh__tag-img" v-for="(t, i) in tags" :key="i" :src="t" mode="heightFix" />
			</view>
		</view>

		<!-- 动态 -->
		<view class="uh__sect">
			<text class="uh__sect-t">TA 的动态</text>
			<view class="uh__feed" v-for="(f, i) in feeds" :key="i" @click="openFeed(i)">
				<view class="uh__feed-cover" :style="{ background: f.bg }">
					<image class="uh__feed-img" :src="f.icon" mode="aspectFit" />
				</view>
				<view class="uh__feed-body">
					<text class="uh__feed-text">{{ f.text }}</text>
					<view class="uh__feed-meta">
						<image class="uh__feed-meta-ico" src="/static/icons-dark/clock.png" mode="aspectFit" />
						<text class="uh__feed-meta-t">{{ f.time }}</text>
					</view>
				</view>
				<image class="uh__chev" src="/static/icons-dark/chevron.png" mode="aspectFit" />
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				following: false,
				stats: [{ num: '12', label: '动态' }, { num: '86', label: '获赞' }, { num: '24', label: '关注' }, { num: '132', label: '粉丝' }],
				tags: [
					'/static/unida/bubbles/label-sport.webp',
					'/static/unida/bubbles/label-study.webp',
					'/static/unida/bubbles/label-fun.webp',
					'/static/unida/bubbles/label-hot.webp'
				],
				feeds: [
					{ bg: 'linear-gradient(135deg,#FF8A3D,#FFD76A)', icon: '/static/icons-dark/heart.png', text: '中心湖的晚霞，随手拍都是大片！', time: '10分钟前' },
					{ bg: 'linear-gradient(135deg,#805CFA,#B59BFF)', icon: '/static/icons-dark/buddy.png', text: '周末约球，有没有一起的？', time: '昨天' }
				]
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onMore() { uni.showToast({ title: '举报 / 分享', icon: 'none' }); },
			onChat() { uni.navigateTo({ url: '/pages/chat/chat' }); },
			onFollow() { this.following = !this.following; },
			openFeed(i) { uni.navigateTo({ url: '/pages/post-detail/post-detail' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.uh { min-height: 100vh; padding: 0 $page-x 60rpx; box-sizing: border-box; }

	.uh__hero {
		margin: 0 (-$page-x);
		background: $g-brand;
		border-radius: 0 0 $r-lg $r-lg;
		padding: 0 $page-x 64rpx;
		box-shadow: $sh-float;
	}
	.uh__nav { height: 110rpx; display: flex; align-items: center; justify-content: space-between; }
	.uh__nav-btn {
		width: 68rpx; height: 68rpx;
		background: rgba(255, 255, 255, 0.18);
		border-radius: 50%;
		display: flex; align-items: center; justify-content: center;
	}
	.uh__nav-img { width: 34rpx; height: 34rpx; }
	.uh__nav-title { font-size: 34rpx; font-weight: 800; color: $c-white; letter-spacing: 1rpx; }
	.uh__profile { display: flex; align-items: center; margin-top: 20rpx; }
	.uh__avatar {
		width: 140rpx; height: 140rpx;
		border-radius: 50%;
		background: rgba(255, 255, 255, 0.95);
		display: flex; align-items: center; justify-content: center;
		border: 6rpx solid rgba(255, 255, 255, 0.5);
		margin-right: 24rpx;
		flex-shrink: 0;
	}
	.uh__avatar-ch { font-size: 60rpx; font-weight: 800; color: $c-primary; }
	.uh__info { display: flex; flex-direction: column; min-width: 0; }
	.uh__name-row { display: flex; align-items: center; }
	.uh__name { font-size: 40rpx; font-weight: 800; color: $c-white; letter-spacing: 1rpx; }
	.uh__shield { height: 36rpx; width: 48rpx; margin-left: 12rpx; }
	.uh__sub { margin-top: 10rpx; font-size: 23rpx; color: rgba(255, 255, 255, 0.9); }
	.uh__dot { margin: 0 6rpx; }
	.uh__score { font-family: $ff-num; font-weight: 700; color: $c-sun; }
	.uh__bio { display: block; margin-top: 24rpx; font-size: 26rpx; color: rgba(255, 255, 255, 0.95); line-height: 1.6; }

	.uh__stats {
		display: flex;
		margin-top: -32rpx;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 28rpx 0;
		position: relative;
	}
	.uh__stat { flex: 1; display: flex; flex-direction: column; align-items: center; }
	.uh__stat-num { font-family: $ff-num; font-size: 36rpx; font-weight: 800; color: $c-deep; }
	.uh__stat-label { margin-top: 8rpx; font-size: 22rpx; color: $t-sub; }

	.uh__actions { display: flex; margin-top: 24rpx; }
	.uh__btn {
		flex: 1; height: 88rpx;
		border-radius: $r-pill;
		display: flex; align-items: center; justify-content: center;
		margin-left: 16rpx;
	}
	.uh__btn:first-child { margin-left: 0; }
	.uh__btn--primary { background: $g-cta; box-shadow: 0 10rpx 20rpx rgba(128, 92, 250, 0.28); }
	.uh__btn--outline { background: $c-white; box-shadow: $sh-card; border: 2rpx solid rgba(128, 92, 250, 0.5); box-sizing: border-box; }
	.uh__btn--ghost { background: $c-ice; }
	.uh__btn-img { width: 32rpx; height: 32rpx; margin-right: 10rpx; }
	.uh__btn-t { font-size: 28rpx; font-weight: 700; color: $c-white; }
	.uh__btn--outline .uh__btn-t { color: $c-primary; }
	.uh__btn--ghost .uh__btn-t { color: $t-sub; }

	.uh__sect {
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 28rpx;
		margin-top: 20rpx;
	}
	.uh__sect-t { display: block; font-size: 30rpx; font-weight: 800; color: $c-ink; }
	.uh__tags { display: flex; flex-wrap: wrap; margin-top: 20rpx; }
	.uh__tag-img { height: 56rpx; width: 110rpx; margin: 0 12rpx 12rpx 0; }

	.uh__feed { display: flex; align-items: center; margin-top: 20rpx; }
	.uh__feed-cover {
		width: 100rpx; height: 100rpx;
		border-radius: $r-sm;
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.uh__feed-img { width: 44rpx; height: 44rpx; opacity: 0.7; }
	.uh__feed-body { flex: 1; margin: 0 16rpx; display: flex; flex-direction: column; min-width: 0; }
	.uh__feed-text { font-size: 26rpx; color: $t-main; line-height: 1.5; }
	.uh__feed-meta { display: flex; align-items: center; margin-top: 10rpx; }
	.uh__feed-meta-ico { width: 24rpx; height: 24rpx; opacity: 0.5; }
	.uh__feed-meta-t { margin-left: 6rpx; font-size: 21rpx; color: $t-tertiary; }
	.uh__chev { width: 26rpx; height: 26rpx; opacity: 0.4; flex-shrink: 0; }
</style>
