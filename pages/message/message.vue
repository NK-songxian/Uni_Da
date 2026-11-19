<template>
	<view class="message unida-page unida-page--tab">
		<!-- 顶部 -->
		<view class="message__top">
			<text class="message__title">消息</text>
			<text class="message__action" @click="onAction">✏️</text>
		</view>

		<!-- 通知入口 -->
		<view class="message__notices unida-card">
			<view class="message__notice" v-for="(n, i) in notices" :key="i" @click="onNotice(n)">
				<view class="message__notice-icon" :style="{ background: n.bg }">{{ n.icon }}</view>
				<text class="message__notice-label">{{ n.label }}</text>
				<view v-if="n.count" class="message__notice-count">{{ n.count }}</view>
			</view>
		</view>

		<!-- 会话列表 -->
		<view class="unida-section" style="margin-top:28rpx">
			<view class="unida-section__head">
				<text class="unida-section__title">最近会话</text>
				<text class="unida-section__more">全部 ›</text>
			</view>
			<view class="message__chat unida-card" v-for="(c, i) in chats" :key="i" @click="onChat(c)">
				<view class="message__avatar">{{ c.avatar }}<view v-if="c.unread" class="message__dot"></view></view>
				<view class="message__chat-main">
					<view class="message__chat-row">
						<text class="message__name">{{ c.name }}</text>
						<text class="message__time">{{ c.time }}</text>
					</view>
					<text class="message__preview">{{ c.preview }}</text>
				</view>
			</view>
		</view>

		<unida-tabbar :current="3" :unreadCount="3" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';

	export default {
		components: { unidaTabbar },
		data() {
			return {
				notices: [
					{ label: '活动通知', icon: '📅', bg: 'linear-gradient(135deg,#7B61FF,#B59BFF)', count: 2 },
					{ label: '预约通知', icon: '✅', bg: 'linear-gradient(135deg,#34D399,#86EFAC)', count: 1 },
					{ label: '订单通知', icon: '🛵', bg: 'linear-gradient(135deg,#FF8A3D,#FFD76A)', count: 0 },
					{ label: '系统通知', icon: '📢', bg: 'linear-gradient(135deg,#5B8DEF,#93C5FD)', count: 0 }
				],
				chats: [
					{ avatar: '😄', name: '阿星', time: '10:32', preview: '周六的夜跑还剩一个位置，来吗？', unread: true },
					{ avatar: '🤩', name: '摄影社-小林', time: '昨天', preview: '照片修好啦，发你邮箱了～', unread: true },
					{ avatar: '😎', name: 'Leo', time: '昨天', preview: '快递已经放到楼下了，记得取哦', unread: false }
				]
			};
		},
		methods: {
			onAction() { uni.showToast({ title: '发起会话待开发', icon: 'none' }); },
			onNotice(n) { uni.showToast({ title: n.label + ' 待开发', icon: 'none' }); },
			onChat(c) { uni.showToast({ title: '与 ' + c.name + ' 的会话待开发', icon: 'none' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.message__top {
		padding: 60rpx 24rpx 20rpx;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	.message__title { font-size: 44rpx; font-weight: 800; color: $unida-text; }
	.message__action { font-size: 40rpx; }
	.message__notices { display: flex; justify-content: space-around; padding: 28rpx 12rpx; }
	.message__notice { position: relative; display: flex; flex-direction: column; align-items: center; }
	.message__notice-icon {
		width: 88rpx;
		height: 88rpx;
		border-radius: 26rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 44rpx;
	}
	.message__notice-label { margin-top: 14rpx; font-size: 24rpx; color: $unida-text; }
	.message__notice-count {
		position: absolute;
		top: -8rpx;
		right: -4rpx;
		min-width: 32rpx;
		height: 32rpx;
		padding: 0 8rpx;
		border-radius: 999rpx;
		background: $unida-orange;
		color: #fff;
		font-size: 20rpx;
		line-height: 32rpx;
		text-align: center;
	}
	.message__chat { display: flex; align-items: center; margin-bottom: 16rpx; }
	.message__avatar {
		position: relative;
		width: 92rpx;
		height: 92rpx;
		border-radius: 50%;
		background: linear-gradient(135deg,#B59BFF,#7B61FF);
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 46rpx;
		margin-right: 20rpx;
		flex-shrink: 0;
	}
	.message__dot {
		position: absolute;
		top: 2rpx;
		right: 2rpx;
		width: 18rpx;
		height: 18rpx;
		border-radius: 50%;
		background: $unida-orange;
		border: 3rpx solid #fff;
	}
	.message__chat-main { flex: 1; }
	.message__chat-row { display: flex; align-items: center; justify-content: space-between; }
	.message__name { font-size: 28rpx; font-weight: 700; color: $unida-text; }
	.message__time { font-size: 22rpx; color: $unida-text-sub; }
	.message__preview { display: block; margin-top: 10rpx; font-size: 24rpx; color: $unida-text-sub; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
</style>
