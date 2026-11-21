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

		<!-- 会话列表 -->
		<view class="ms__item" v-for="(c, i) in chats" :key="i" @click="onChat(i)">
			<view class="ms__avatar-wrap">
				<image class="ms__avatar" v-if="c.avatar" :src="c.avatar" mode="aspectFit" />
				<view class="ms__avatar-group" v-else-if="c.group">
					<view class="ms__group-face" v-for="(g, j) in c.group" :key="j" :class="'ms__group-face--' + g.tone"><text class="ms__group-ch">{{ g.ch }}</text></view>
				</view>
				<view class="ms__online" v-if="c.online"></view>
			</view>
			<view class="ms__main">
				<view class="ms__row">
					<text class="ms__name">{{ c.name }}</text>
					<image class="ms__row-tag" :src="c.tagIcon" mode="heightFix" />
					<view class="ms__row-right">
						<text class="ms__time">{{ c.time }}</text>
						<image class="ms__unread" v-if="c.unread" :src="c.unread" mode="widthFix" />
					</view>
				</view>
				<text class="ms__preview">{{ c.preview }}</text>
				<view class="ms__meta" v-if="c.meta">
					<text class="ms__meta-t" v-for="(m, j) in c.meta" :key="j">{{ m }}</text>
				</view>
				<view class="ms__progress" v-if="c.progress">
					<view class="ms__progress-line" v-for="(p, j) in c.progress" :key="j">
						<view class="ms__progress-dot" :class="{ 'ms__progress-dot--on': p.on }"></view>
						<text class="ms__progress-t" :class="{ 'ms__progress-t--on': p.on }">{{ p.t }}</text>
					</view>
				</view>
				<image class="ms__status" v-if="c.status" :src="c.status" mode="heightFix" />
			</view>
			<image class="ms__chev" src="/static/icons-dark/chevron.png" mode="aspectFit" />
		</view>

		<view class="ms__bottom-space"></view>
		<unida-tabbar :current="3" :unread-count="15" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';

	export default {
		components: { unidaTabbar },
		data() {
			return {
				statusBar: 0,
				active: 0,
				tabs: [
					{ icon: '/static/unida/msg/tag-chat.webp' },
					{ icon: '/static/unida/msg/tag-book.webp' },
					{ icon: '/static/unida/msg/tag-event.webp' },
					{ icon: '/static/unida/msg/tag-order.webp' },
					{ icon: '/static/unida/msg/tag-system.webp' }
				],
				chats: [
					{
						name: '林小悠', tagIcon: '/static/unida/msg/tag-chat.webp', time: '10:12',
						avatar: '/static/unida/msg/mascot-star.webp', online: true,
						preview: '今天图书馆自习还去吗？要不要一起？',
						unread: '/static/unida/msg/badge-3.webp'
					},
					{
						name: '校园活动｜春日校园跑', tagIcon: '/static/unida/msg/tag-event.webp', time: '昨天 20:30',
						avatar: '/static/unida/msg/scene-booth.webp',
						preview: '【报名开启】UNIDA 春日校园跑来啦！一起在阳光下奔跑，结识更多运动搭子！'
					},
					{
						name: '学习健身搭子预约', tagIcon: '/static/unida/msg/tag-book.webp', time: '昨天 18:05',
						avatar: '/static/unida/msg/scene-fitness.webp',
						preview: '预约已确认！你已成功约到「图书馆自习 · 健身打卡」搭子～',
						meta: ['3月12日（周三）', '19:00 – 21:00'],
						status: '/static/unida/msg/badge-check.webp'
					},
					{
						name: '校园跑腿订单', tagIcon: '/static/unida/msg/tag-order.webp', time: '09:36',
						avatar: '/static/unida/msg/scene-takeout.webp',
						preview: '【进行中】你的跑腿订单已接单！帮取：食堂奶茶（2杯）› 送达：紫荆宿舍楼 3栋',
						progress: [
							{ t: '已接单', on: true }, { t: '取货中', on: true }, { t: '配送中', on: false }, { t: '已完成', on: false }
						],
						status: '/static/unida/msg/badge-doing.webp'
					},
					{
						name: '校园活动搭子群（128）', tagIcon: '/static/unida/msg/tag-chat.webp', time: '08:47',
						group: [{ ch: '阿', tone: 'purple' }, { ch: '星', tone: 'orange' }, { ch: '林', tone: 'green' }, { ch: 'Leo', tone: 'sky' }],
						preview: '阿晨：周六的飞盘活动还有名额！要一起组队吗？',
						unread: '/static/unida/msg/badge-12.webp'
					}
				]
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			onSearch() { uni.showToast({ title: '消息搜索待接入', icon: 'none' }); },
			onTab(i) { this.active = i; },
			onSystem() { uni.showToast({ title: '系统通知', icon: 'none' }); },
			onChat(i) { uni.navigateTo({ url: '/pages/chat/chat?name=' + this.chats[i].name }); }
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
	.ms__avatar { width: 118rpx; height: 118rpx; border-radius: 20rpx; background: $c-mist; }
	.ms__avatar-group { display: flex; flex-wrap: wrap; width: 118rpx; height: 118rpx; }
	.ms__group-face { width: 55rpx; height: 55rpx; border-radius: 12rpx; display: flex; align-items: center; justify-content: center; margin: 0 4rpx 4rpx 0; }
	.ms__group-face--purple { background: rgba(128, 92, 250, 0.24); }
	.ms__group-face--orange { background: rgba(255, 155, 119, 0.28); }
	.ms__group-face--green { background: rgba(41, 202, 131, 0.24); }
	.ms__group-face--sky { background: rgba(105, 185, 245, 0.24); }
	.ms__group-ch { font-size: 24rpx; color: #4B2B80; font-weight: 700; }
	.ms__online { position: absolute; right: 4rpx; bottom: 4rpx; width: 18rpx; height: 18rpx; border-radius: 50%; background: $c-mint; border: 3rpx solid $c-white; box-sizing: border-box; }
	.ms__main { flex: 1; min-width: 0; margin: 0 12rpx 0 18rpx; }
	.ms__row { display: flex; align-items: center; }
	.ms__name { font-size: 27rpx; font-weight: 700; color: $t-main; max-width: 300rpx; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
	.ms__row-tag { height: 32rpx; width: 92rpx; margin-left: 10rpx; flex-shrink: 0; }
	.ms__row-right { margin-left: auto; display: flex; align-items: center; flex-shrink: 0; }
	.ms__time { font-size: 20rpx; color: $t-tertiary; }
	.ms__unread { width: 44rpx; margin-left: 10rpx; }
	.ms__preview { display: block; margin-top: 10rpx; font-size: 23rpx; color: $t-sub; line-height: 1.5; }
	.ms__meta { display: flex; flex-wrap: wrap; margin-top: 12rpx; }
	.ms__meta-t { font-size: 20rpx; color: #6C5A93; background: $c-mist; border-radius: $r-pill; padding: 6rpx 16rpx; margin: 0 10rpx 8rpx 0; }
	.ms__progress { display: flex; align-items: flex-start; margin-top: 16rpx; }
	.ms__progress-line { display: flex; flex-direction: column; align-items: center; width: 25%; }
	.ms__progress-dot { width: 22rpx; height: 22rpx; border-radius: 50%; background: $c-white; border: 3rpx solid $t-tertiary; box-sizing: border-box; }
	.ms__progress-dot--on { background: $c-primary; border-color: $c-primary; }
	.ms__progress-t { margin-top: 6rpx; font-size: 19rpx; color: $t-tertiary; }
	.ms__progress-t--on { color: $c-primary; font-weight: 600; }
	.ms__status { height: 40rpx; margin-top: 14rpx; }
	.ms__chev { width: 24rpx; height: 24rpx; opacity: 0.3; flex-shrink: 0; margin-top: 44rpx; }

	.ms__bottom-space { height: 180rpx; }
</style>
