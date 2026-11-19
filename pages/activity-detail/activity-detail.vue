<template>
	<view class="ad unida-page">
		<!-- 自定义导航 -->
		<view class="ad__nav">
			<text class="ad__nav-btn" @click="goBack">‹</text>
			<text class="ad__nav-title">活动详情</text>
			<text class="ad__nav-btn" @click="onShare">⋯</text>
		</view>

		<!-- 封面 -->
		<view class="ad__cover">
			<text class="ad__cover-emoji">🎪</text>
			<view class="ad__cover-status">🔥 报名中</view>
		</view>

		<!-- 主体信息卡 -->
		<view class="ad__main unida-card">
			<view class="ad__title-row">
				<text class="ad__title">校园草地音乐会 · 一起嗨翻周末</text>
				<view class="ad__fav" @click="faved = !faved">{{ faved ? '❤️' : '🤍' }}</view>
			</view>
			<view class="ad__tags">
				<text class="unida-tag unida-tag--purple">校园活动</text>
				<text class="unida-tag unida-tag--orange">🔥 热门</text>
				<text class="unida-tag unida-tag--green">免费</text>
			</view>
			<view class="ad__meta">
				<view class="ad__meta-item"><text class="ad__meta-icon">🕒</text><view><text class="ad__meta-label">活动时间</text><text class="ad__meta-value">本周六 19:00 - 21:00</text></view></view>
				<view class="ad__meta-item"><text class="ad__meta-icon">📍</text><view><text class="ad__meta-label">活动地点</text><text class="ad__meta-value">中心草坪广场</text></view></view>
			</view>
		</view>

		<!-- 发起人 -->
		<view class="ad__organizer unida-card" @click="goUser">
			<view class="ad__org-avatar">🎸</view>
			<view class="ad__org-info">
				<text class="ad__org-name">音乐社 · 小林</text>
				<text class="ad__org-sub">🎓 已认证 · ⭐ 4.9 分</text>
			</view>
			<text class="ad__org-arrow">›</text>
		</view>

		<!-- 报名人员 -->
		<view class="ad__members unida-card">
			<view class="ad__subhead"><text class="ad__subhead-title">报名人员</text><text class="ad__subhead-more">{{ joined }}/{{ total }} 人 · 查看全部 ›</text></view>
			<view class="ad__avatars">
				<text class="ad__avatar" v-for="(a, i) in avatars" :key="i">{{ a }}</text>
				<view class="ad__avatar ad__avatar--more">+{{ total - joined }}</view>
			</view>
		</view>

		<!-- 活动详情 -->
		<view class="ad__desc unida-card">
			<view class="ad__subhead"><text class="ad__subhead-title">活动详情</text></view>
			<text class="ad__desc-text">一起在草地上听歌、唱歌、认识新朋友！我们准备了音响、吉他和零食，欢迎会乐器或爱唱歌的同学加入，也欢迎来当观众～ 🎶</text>
			<text class="ad__desc-text">请自带野餐垫，注意防蚊。活动结束后一起收拾场地哦～</text>
		</view>

		<!-- 费用说明 -->
		<view class="ad__cost unida-card">
			<view class="ad__subhead"><text class="ad__subhead-title">费用说明</text></view>
			<text class="ad__cost-text">免费参与 · 零食饮料 AA（预计 ¥15/人）</text>
		</view>

		<!-- 底部报名栏 -->
		<view class="ad__bottom">
			<view class="ad__bottom-left" @click="onContact">
				<text class="ad__bottom-icon">💬</text>
				<text class="ad__bottom-label">联系</text>
			</view>
			<view class="ad__bottom-btn" @click="onBooking">立即报名</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				faved: false,
				joined: 36,
				total: 50,
				avatars: ['😄', '🤩', '😎', '👩‍🎓', '🧑‍🎓', '👨‍🎓']
			};
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onShare() { uni.showToast({ title: '分享功能待接入', icon: 'none' }); },
			goUser() { uni.navigateTo({ url: '/pages/user-home/user-home' }); },
			onContact() { uni.navigateTo({ url: '/pages/chat/chat' }); },
			onBooking() { uni.navigateTo({ url: '/pages/booking-confirm/booking-confirm' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.ad { padding-bottom: 160rpx; }
	.ad__nav { height: 120rpx; padding: 60rpx 32rpx 0; display: flex; align-items: center; justify-content: space-between; position: absolute; left: 0; right: 0; top: 0; z-index: 10; }
	.ad__nav-btn { width: 60rpx; height: 60rpx; border-radius: 50%; background: rgba(255,255,255,0.9); color: $unida-text; font-size: 40rpx; display: flex; align-items: center; justify-content: center; }
	.ad__nav-title { font-size: 32rpx; font-weight: 700; color: #fff; text-shadow: 0 2rpx 8rpx rgba(0,0,0,0.2); }
	.ad__cover { height: 480rpx; border-radius: 0 0 40rpx 40rpx; background: linear-gradient(135deg,#7B61FF,#B59BFF,#FFD76A); display: flex; align-items: center; justify-content: center; position: relative; }
	.ad__cover-emoji { font-size: 180rpx; filter: drop-shadow(0 16rpx 24rpx rgba(0,0,0,0.15)); }
	.ad__cover-status { position: absolute; left: 32rpx; bottom: 32rpx; background: $unida-orange; color: #fff; font-size: 24rpx; padding: 10rpx 24rpx; border-radius: 999rpx; }
	.ad__main, .ad__organizer, .ad__members, .ad__desc, .ad__cost { margin: 20rpx 24rpx; }
	.ad__main { margin-top: -40rpx; position: relative; }
	.ad__title-row { display: flex; align-items: flex-start; justify-content: space-between; }
	.ad__title { font-size: 34rpx; font-weight: 800; color: $unida-text; flex: 1; line-height: 1.4; }
	.ad__fav { font-size: 44rpx; margin-left: 16rpx; }
	.ad__tags { display: flex; gap: 12rpx; margin-top: 18rpx; flex-wrap: wrap; }
	.ad__meta { margin-top: 28rpx; padding-top: 24rpx; border-top: 2rpx solid $unida-divider; }
	.ad__meta-item { display: flex; align-items: flex-start; margin-bottom: 20rpx; }
	.ad__meta-icon { font-size: 32rpx; margin-right: 16rpx; }
	.ad__meta-item view { display: flex; flex-direction: column; }
	.ad__meta-label { font-size: 22rpx; color: $unida-text-sub; }
	.ad__meta-value { margin-top: 6rpx; font-size: 28rpx; color: $unida-text; font-weight: 600; }
	.ad__organizer { display: flex; align-items: center; }
	.ad__org-avatar { width: 88rpx; height: 88rpx; border-radius: 50%; background: linear-gradient(135deg,#FF8A3D,#FFD76A); display: flex; align-items: center; justify-content: center; font-size: 44rpx; margin-right: 20rpx; }
	.ad__org-info { flex: 1; display: flex; flex-direction: column; }
	.ad__org-name { font-size: 28rpx; font-weight: 700; color: $unida-text; }
	.ad__org-sub { margin-top: 8rpx; font-size: 22rpx; color: $unida-text-sub; }
	.ad__org-arrow { font-size: 40rpx; color: $unida-text-sub; }
	.ad__subhead { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20rpx; }
	.ad__subhead-title { font-size: 28rpx; font-weight: 700; color: $unida-text; }
	.ad__subhead-more { font-size: 22rpx; color: $unida-text-sub; }
	.ad__avatars { display: flex; }
	.ad__avatar { width: 68rpx; height: 68rpx; border-radius: 50%; background: linear-gradient(135deg,#B59BFF,#7B61FF); display: flex; align-items: center; justify-content: center; font-size: 36rpx; margin-right: -12rpx; border: 4rpx solid #fff; }
	.ad__avatar--more { background: #efebf8; color: $unida-primary; font-size: 22rpx; font-weight: 700; }
	.ad__desc-text { display: block; font-size: 26rpx; color: #4a4560; line-height: 1.8; margin-bottom: 12rpx; }
	.ad__cost-text { font-size: 26rpx; color: $unida-orange; font-weight: 600; }
	.ad__bottom { position: fixed; left: 0; right: 0; bottom: 0; background: #fff; padding: 16rpx 24rpx calc(16rpx + env(safe-area-inset-bottom)); display: flex; align-items: center; box-shadow: 0 -6rpx 24rpx rgba(123,97,255,0.08); z-index: 20; }
	.ad__bottom-left { width: 100rpx; display: flex; flex-direction: column; align-items: center; }
	.ad__bottom-icon { font-size: 40rpx; }
	.ad__bottom-label { font-size: 20rpx; color: $unida-text-sub; }
	.ad__bottom-btn { flex: 1; height: 88rpx; border-radius: 999rpx; background: linear-gradient(135deg,#7B61FF,#B59BFF); color: #fff; font-size: 30rpx; font-weight: 700; display: flex; align-items: center; justify-content: center; box-shadow: 0 10rpx 24rpx rgba(123,97,255,0.28); }
</style>
