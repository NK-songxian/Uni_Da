<template>
	<view class="ms unida-page unida-page--tab">
		<view class="ms__safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 顶栏 -->
		<view class="ms__top">
			<text class="ms__title">消息</text>
			<view class="ms__compose" @click="onCompose"><image class="ms__compose-img" src="/static/icons-dark/plus.png" mode="aspectFit" /></view>
		</view>

		<!-- 通知入口 -->
		<view class="ms__notices">
			<view class="ms__notice" v-for="(n, i) in notices" :key="i" @click="onNotice(i)">
				<view class="ms__notice-ico" :class="'ms__notice-ico--' + n.tone">
					<image class="ms__notice-img" :src="n.icon" mode="aspectFit" />
					<view v-if="n.count > 0" class="ms__notice-count"><text class="ms__notice-count-t">{{ n.count }}</text></view>
				</view>
				<text class="ms__notice-label">{{ n.label }}</text>
			</view>
		</view>

		<!-- 最近会话 -->
		<view class="ms__sect">
			<text class="ms__sect-t">最近会话</text>
			<text class="ms__sect-s">全部 ›</text>
		</view>
		<view class="ms__chat" v-for="(c, i) in chats" :key="i" @click="onChat(i)">
			<view class="ms__avatar" :class="'ms__avatar--' + c.tone"><text class="ms__avatar-ch">{{ c.name[0] }}</text><view v-if="c.unread" class="ms__dot"></view></view>
			<view class="ms__main">
				<view class="ms__row">
					<text class="ms__name">{{ c.name }}</text>
					<text class="ms__time">{{ c.time }}</text>
				</view>
				<text class="ms__preview">{{ c.preview }}</text>
			</view>
			<image class="ms__chev" src="/static/icons-dark/chevron.png" mode="aspectFit" />
		</view>

		<view class="ms__bottom-space"></view>
		<unida-tabbar :current="3" :unread-count="3" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';

	export default {
		components: { unidaTabbar },
		data() {
			return {
				statusBar: 0,
				notices: [
					{ label: '活动通知', icon: '/static/icons-dark/calendar.png', tone: 'purple', count: 2 },
					{ label: '预约通知', icon: '/static/icons-dark/heart.png', tone: 'green', count: 1 },
					{ label: '订单通知', icon: '/static/icons-dark/box.png', tone: 'orange', count: 0 },
					{ label: '系统通知', icon: '/static/icons-dark/bell.png', tone: 'sky', count: 0 }
				],
				chats: [
					{ name: '阿星', tone: 'a', time: '10:32', preview: '周六的夜跑还剩一个位置，来吗？', unread: true },
					{ name: '摄影社-小林', tone: 'b', time: '昨天', preview: '照片修好啦，发你邮箱了～', unread: true },
					{ name: 'Leo', tone: 'c', time: '昨天', preview: '快递已经放到楼下了，记得取哦', unread: false }
				]
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			onCompose() { uni.showToast({ title: '发起会话待开发', icon: 'none' }); },
			onNotice(i) { uni.showToast({ title: this.notices[i].label + '待开发', icon: 'none' }); },
			onChat(i) { uni.navigateTo({ url: '/pages/chat/chat?name=' + this.chats[i].name }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.ms { min-height: 100vh; }

	/* ---------- 顶栏 ---------- */
	.ms__top { display: flex; align-items: center; padding: 24rpx $page-x 0; }
	.ms__title { flex: 1; font-size: 44rpx; font-weight: 800; color: $c-ink; }
	.ms__compose {
		width: 72rpx; height: 72rpx;
		background: $g-cta;
		border-radius: 50%;
		display: flex; align-items: center; justify-content: center;
		box-shadow: $sh-float;
	}
	.ms__compose-img { width: 34rpx; height: 34rpx; filter: brightness(0) invert(1); }

	/* ---------- 通知入口 ---------- */
	.ms__notices { display: flex; justify-content: space-between; margin: 28rpx $page-x 0; background: $c-white; border-radius: $r-lg; box-shadow: $sh-card; padding: 28rpx 26rpx; }
	.ms__notice { position: relative; display: flex; flex-direction: column; align-items: center; flex: 1; }
	.ms__notice-ico { position: relative; width: 84rpx; height: 84rpx; border-radius: 26rpx; display: flex; align-items: center; justify-content: center; }
	.ms__notice-ico--purple { background: rgba(128, 92, 250, 0.13); }
	.ms__notice-ico--green { background: rgba(41, 202, 131, 0.14); }
	.ms__notice-ico--orange { background: rgba(255, 155, 119, 0.16); }
	.ms__notice-ico--sky { background: rgba(105, 185, 245, 0.16); }
	.ms__notice-img { width: 42rpx; height: 42rpx; }
	.ms__notice-count {
		position: absolute; top: -10rpx; right: -12rpx;
		min-width: 34rpx; height: 34rpx;
		padding: 0 8rpx;
		background: $c-peach;
		border-radius: $r-pill;
		display: flex; align-items: center; justify-content: center;
	}
	.ms__notice-count-t { font-size: 20rpx; color: $c-white; font-family: $ff-num; font-weight: 700; }
	.ms__notice-label { margin-top: 14rpx; font-size: 23rpx; color: $t-main; }

	/* ---------- 最近会话 ---------- */
	.ms__sect { display: flex; align-items: baseline; margin: 36rpx $page-x 0; }
	.ms__sect-t { font-size: 32rpx; font-weight: 800; color: $c-ink; }
	.ms__sect-s { margin-left: auto; font-size: 22rpx; color: $t-tertiary; }
	.ms__chat {
		display: flex; align-items: center;
		margin: 16rpx $page-x 0;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 24rpx;
	}
	.ms__avatar {
		position: relative;
		width: 92rpx; height: 92rpx;
		border-radius: 50%;
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.ms__avatar--a { background: $g-brand; }
	.ms__avatar--b { background: linear-gradient(160deg, #FF9B77, #FFC94F); }
	.ms__avatar--c { background: linear-gradient(160deg, #69B9F5, #29CA83); }
	.ms__avatar-ch { font-size: 38rpx; font-weight: 800; color: $c-white; }
	.ms__dot { position: absolute; top: 2rpx; right: 2rpx; width: 18rpx; height: 18rpx; border-radius: 50%; background: $c-peach; border: 3rpx solid $c-white; }
	.ms__main { flex: 1; min-width: 0; margin: 0 20rpx; }
	.ms__row { display: flex; align-items: center; justify-content: space-between; }
	.ms__name { font-size: 28rpx; font-weight: 700; color: $t-main; }
	.ms__time { font-size: 21rpx; color: $t-tertiary; font-family: $ff-num; }
	.ms__preview { display: block; margin-top: 10rpx; font-size: 24rpx; color: $t-sub; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
	.ms__chev { width: 26rpx; height: 26rpx; opacity: 0.35; flex-shrink: 0; }

	.ms__bottom-space { height: 200rpx; }
</style>
