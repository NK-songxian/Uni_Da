<template>
	<view class="ms unida-page unida-page--tab">
		<view class="ms-safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- hero 背景（设计稿原图：logo/消息/副标题/吉祥物/校园） -->
		<view class="ms__hero">
			<image class="ms__hero-img" src="/static/unida/msg/msg-hero.jpg" mode="widthFix" />
		</view>

		<!-- 搜索框 -->
		<view class="ms__search" @click="onSearch">
			<image class="ms__search-ico" src="/static/unida/msg/ico-search.webp" mode="aspectFit" />
			<text class="ms__search-ph">搜索聊天、活动、订单等消息</text>
		</view>

		<!-- 分类 tabs（设计稿胶囊素材） -->
		<scroll-view scroll-x class="ms__tabs" :show-scrollbar="false">
			<view class="ms__tabs-row">
				<view class="ms__tab ms__tab--all" :class="{ 'ms__tab--on': active === 0 }" @click="onTab(0)"><text class="ms__tab-all-t">全部</text></view>
				<view class="ms__tab" v-for="(t, i) in tabs" :key="i" @click="onTab(i + 1)">
					<image class="ms__tab-img" :class="{ 'ms__tab-img--off': active !== i + 1 }" :src="t.icon" mode="heightFix" />
				</view>
			</view>
		</scroll-view>

		<!-- 置顶系统通知卡 -->
		<view class="ms__pin" @click="onSystem">
			<image class="ms__pin-mascot" src="/static/unida/msg/mascot-wave.webp" mode="widthFix" />
			<view class="ms__pin-body">
				<view class="ms__pin-row">
					<text class="ms__pin-name">UNIDA（有你搭）</text>
					<image class="ms__pin-shield" src="/static/unida/msg/ico-shield.webp" mode="heightFix" />
					<text class="ms__pin-sys">系统</text>
				</view>
				<text class="ms__pin-title">欢迎来到 UNIDA!</text>
				<text class="ms__pin-desc">在这里，找到同频的搭子、参与精彩的校园活动、解锁更丰富的大学生活！一起搭出属于你的校园故事吧！</text>
			</view>
			<image class="ms__pin-badge" src="/static/unida/msg/pin-yellow.webp" mode="widthFix" />
		</view>

		<!-- 通知中心入口（5 类通知 + 未读数） -->
		<view class="ms__notify" @click="onNotify">
			<view class="ms__notify-ico"><image class="ms__notify-img" src="/static/icons-dark/bell.png" mode="aspectFit" /></view>
			<view class="ms__notify-body">
				<text class="ms__notify-t">通知中心</text>
				<text class="ms__notify-s">系统 · 活动 · 订单 · 预约 · 互动</text>
			</view>
			<view class="ms__notify-badge" v-if="notifyUnread > 0"><text class="ms__notify-badge-t">{{ notifyUnread > 99 ? '99+' : notifyUnread }}</text></view>
			<image class="ms__chev ms__chev--mid" src="/static/icons-dark/chevron.png" mode="aspectFit" />
		</view>

		<!-- 会话列表 -->
		<view class="ms__item" v-for="(c, i) in chats" :key="i" @click="onChat(i)">
			<view class="ms__avatar-wrap">
				<view class="ms__avatar ms__avatar--letter"><text class="ms__avatar-ch">{{ c.name[0] }}</text></view>
				<view class="ms__online" v-if="c.online"></view>
			</view>
			<view class="ms__main">
				<view class="ms__row">
					<text class="ms__name">{{ c.name }}</text>
					<image class="ms__row-tag" :src="c.tagIcon" mode="heightFix" />
					<view class="ms__row-right">
						<text class="ms__time">{{ c.time }}</text>
						<view class="ms__unread-n" v-if="c.unreadN > 0"><text class="ms__unread-t">{{ c.unreadN > 99 ? '99+' : c.unreadN }}</text></view>
					</view>
				</view>
				<text class="ms__preview">{{ c.preview }}</text>
			</view>
			<image class="ms__chev" src="/static/icons-dark/chevron.png" mode="aspectFit" />
		</view>

		<!-- 品牌空态 -->
		<view class="ms__empty" v-if="!loading && chats.length === 0">
			<text class="ms__empty-t">还没有会话，去社区认识新朋友吧～</text>
		</view>

		<view class="ms__bottom-space"></view>
		<unida-tabbar :current="3" :unread-count="totalUnread" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';
	import { callCloud, getToken } from '@/common/cloud.js';

	export default {
		components: { unidaTabbar },
		data() {
			return {
				statusBar: 0,
				loading: false,
				active: 0,
				notifyUnread: 0,
				tabs: [
					{ icon: '/static/unida/msg/tag-chat.webp' },
					{ icon: '/static/unida/msg/tag-book.webp' },
					{ icon: '/static/unida/msg/tag-event.webp' },
					{ icon: '/static/unida/msg/tag-order.webp' },
					{ icon: '/static/unida/msg/tag-system.webp' }
				],
				chats: []
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		onShow() {
			this.loadChats();
			this.loadNotifyUnread();
		},
		computed: {
			totalUnread() {
				return this.chats.reduce((s, c) => s + (Number(c.unreadN) || 0), 0) + (Number(this.notifyUnread) || 0);
			}
		},
		methods: {
			async loadChats() {
				if (this.loading) return;
				this.loading = true;
				try {
					const r = await callCloud('chat', { action: 'conversations', token: getToken() });
					this.chats = (r.list || []).map((x) => ({
						peer: x.peer,
						name: x.name || '同学',
						tagIcon: x.peer === 'official' ? '/static/unida/msg/tag-system.webp' : '/static/unida/msg/tag-chat.webp',
						time: x.time,
						preview: x.preview,
						unreadN: Number(x.unread) || 0,
						online: x.peer === 'official'
					}));
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '加载会话失败', icon: 'none' });
				} finally {
					this.loading = false;
				}
			},
			async loadNotifyUnread() {
				try {
					const r = await callCloud('notify', { action: 'unread', token: getToken() });
					this.notifyUnread = Number(r.total) || 0;
				} catch (e) {}
			},
			onNotify() { uni.navigateTo({ url: '/pages/notifications/notifications' }); },
			onSearch() { uni.showToast({ title: '消息搜索待接入', icon: 'none' }); },
			onTab(i) { this.active = i; },
			onSystem() { uni.navigateTo({ url: '/pages/notifications/notifications' }); },
			onChat(i) {
				const c = this.chats[i];
				if (!c) return;
				uni.navigateTo({ url: '/pages/chat/chat?peer=' + c.peer + '&name=' + encodeURIComponent(c.name) });
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.ms { min-height: 100vh; padding: 0 $page-x; box-sizing: border-box; background: linear-gradient(180deg, #E9DBFF 0%, $c-mist 22%, #F7F3FF 100%); }

	/* ---------- hero ---------- */
	.ms__hero { margin: 0 (-$page-x); }
	.ms__hero-img { width: 100%; display: block; }

	/* ---------- 搜索 ---------- */
	.ms__search {
		display: flex; align-items: center;
		height: 84rpx;
		background: $c-white;
		border-radius: $r-pill;
		box-shadow: $sh-card;
		padding: 0 28rpx;
		margin-top: 4rpx;
	}
	.ms__search-ico { width: 52rpx; height: 52rpx; margin-right: 14rpx; }
	.ms__search-ph { font-size: 26rpx; color: $t-tertiary; }

	/* ---------- 分类 tabs ---------- */
	.ms__tabs { margin: 22rpx (-$page-x) 0; white-space: nowrap; }
	.ms__tabs-row { display: inline-flex; align-items: center; padding: 0 $page-x; }
	.ms__tab { margin-right: 10rpx; height: 52rpx; display: flex; align-items: center; }
	.ms__tab--all {
		background: $g-brand;
		border-radius: $r-pill;
		padding: 0 32rpx;
		box-shadow: 0 8rpx 18rpx rgba(128, 92, 250, 0.28);
	}
	.ms__tab--on.ms__tab--all { background: $g-brand; }
	.ms__tab-all-t { font-size: 28rpx; color: $c-white; font-weight: 700; letter-spacing: 2rpx; }
	.ms__tab-img { height: 46rpx; width: 106rpx; }
	.ms__tab-img--off { opacity: 0.72; filter: grayscale(0.25); }

	/* ---------- 置顶系统卡 ---------- */
	.ms__pin {
		position: relative;
		display: flex; align-items: center;
		background: linear-gradient(110deg, #C6A8FF 0%, #B79BFF 45%, #D9C4FF 100%);
		border-radius: $r-md;
		box-shadow: $sh-float;
		padding: 24rpx 24rpx 24rpx 12rpx;
		margin-top: 24rpx;
		overflow: hidden;
	}
	.ms__pin-mascot { width: 180rpx; flex-shrink: 0; margin-top: 8rpx; }
	.ms__pin-body { flex: 1; min-width: 0; margin-left: 6rpx; }
	.ms__pin-row { display: flex; align-items: center; }
	.ms__pin-name { font-size: 27rpx; color: #2B0A5E; font-weight: 800; }
	.ms__pin-shield { height: 30rpx; width: 30rpx; margin-left: 8rpx; }
	.ms__pin-sys { font-size: 19rpx; color: #5B3699; background: rgba(255, 255, 255, 0.55); border-radius: $r-pill; padding: 4rpx 14rpx; margin-left: 10rpx; }
	.ms__pin-title { display: block; margin-top: 12rpx; font-size: 27rpx; color: #2B0A5E; font-weight: 700; }
	.ms__pin-desc { display: block; margin-top: 8rpx; font-size: 21rpx; color: rgba(43, 10, 94, 0.75); line-height: 1.55; }
	.ms__pin-badge { position: absolute; right: 20rpx; top: 20rpx; width: 96rpx; }

	/* ---------- 通知中心入口 ---------- */
	.ms__notify {
		display: flex; align-items: center;
		margin-top: 24rpx;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 22rpx 24rpx;
	}
	.ms__notify-ico {
		width: 76rpx; height: 76rpx;
		border-radius: 24rpx;
		background: rgba(128, 92, 250, 0.12);
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.ms__notify-img { width: 40rpx; height: 40rpx; }
	.ms__notify-body { flex: 1; min-width: 0; margin-left: 20rpx; display: flex; flex-direction: column; }
	.ms__notify-t { font-size: 28rpx; font-weight: 700; color: $t-main; }
	.ms__notify-s { margin-top: 6rpx; font-size: 21rpx; color: $t-tertiary; }
	.ms__notify-badge {
		min-width: 40rpx; height: 40rpx;
		box-sizing: border-box;
		padding: 0 12rpx;
		background: #FF5A4E;
		border-radius: $r-pill;
		display: flex; align-items: center; justify-content: center;
		margin-right: 12rpx;
	}
	.ms__notify-badge-t { font-size: 20rpx; color: $c-white; font-weight: 700; font-family: $ff-num; }
	.ms__chev--mid { margin-top: 0; }

	/* ---------- 会话列表 ---------- */
	.ms__item {
		display: flex; align-items: flex-start;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 22rpx 20rpx;
		margin-top: 16rpx;
	}
	.ms__avatar-wrap { position: relative; width: 118rpx; height: 118rpx; flex-shrink: 0; }
	.ms__avatar--letter {
		width: 118rpx; height: 118rpx; border-radius: 20rpx;
		background: $g-brand;
		display: flex; align-items: center; justify-content: center;
	}
	.ms__avatar-ch { font-size: 46rpx; color: $c-white; font-weight: 800; }
	.ms__online { position: absolute; right: 4rpx; bottom: 4rpx; width: 18rpx; height: 18rpx; border-radius: 50%; background: $c-mint; border: 3rpx solid $c-white; box-sizing: border-box; }
	.ms__main { flex: 1; min-width: 0; margin: 0 12rpx 0 18rpx; }
	.ms__row { display: flex; align-items: center; }
	.ms__name { font-size: 27rpx; font-weight: 700; color: $t-main; max-width: 300rpx; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
	.ms__row-tag { height: 32rpx; width: 92rpx; margin-left: 10rpx; flex-shrink: 0; }
	.ms__row-right { margin-left: auto; display: flex; align-items: center; flex-shrink: 0; }
	.ms__time { font-size: 20rpx; color: $t-tertiary; }
	.ms__unread-n {
		min-width: 44rpx; height: 36rpx;
		box-sizing: border-box;
		padding: 0 12rpx;
		margin-left: 12rpx;
		background: $g-cta;
		border-radius: $r-pill;
		display: flex; align-items: center; justify-content: center;
	}
	.ms__unread-t { font-size: 20rpx; color: $c-white; font-weight: 700; font-family: $ff-num; }
	.ms__preview { display: block; margin-top: 10rpx; font-size: 23rpx; color: $t-sub; line-height: 1.5; }
	.ms__chev { width: 24rpx; height: 24rpx; opacity: 0.3; flex-shrink: 0; margin-top: 44rpx; }

	.ms__empty { display: flex; justify-content: center; padding: 80rpx 0; }
	.ms__empty-t { font-size: 26rpx; color: $t-tertiary; }

	.ms__bottom-space { height: 180rpx; }
</style>
