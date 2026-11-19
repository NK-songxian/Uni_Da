<template>
	<view class="uh">
		<!-- 头部渐变 -->
		<view class="uh__hero">
			<view class="uh__nav"><text class="uh__back" @click="goBack">‹</text><text class="uh__nav-title">个人主页</text><text class="uh__more">⋯</text></view>
			<view class="uh__profile">
				<text class="uh__avatar">😄</text>
				<view class="uh__info">
					<text class="uh__name">阿星 <text class="uh__verify">🎓</text></text>
					<text class="uh__sub">阳光大学 · 已认证 · ⭐ 4.9</text>
				</view>
			</view>
			<text class="uh__bio">热爱运动，喜欢认识新朋友～ 一起让校园生活更有趣！</text>
		</view>
		<!-- 数据 -->
		<view class="uh__stats unida-card">
			<view class="uh__stat" v-for="(s, i) in stats" :key="i"><text class="uh__stat-num">{{ s.num }}</text><text class="uh__stat-label">{{ s.label }}</text></view>
		</view>
		<!-- 操作 -->
		<view class="uh__actions">
			<view class="uh__btn uh__btn--primary" @click="onChat">💬 私信</view>
			<view class="uh__btn" :class="following ? 'uh__btn--ghost' : 'uh__btn--outline'" @click="following = !following">{{ following ? '✓ 已关注' : '+ 关注' }}</view>
		</view>
		<!-- 兴趣标签 -->
		<view class="uh__section unida-card">
			<text class="uh__section-title">兴趣标签</text>
			<view class="uh__tags"><text class="unida-tag unida-tag--purple" v-for="(t, i) in tags" :key="i">{{ t }}</text></view>
		</view>
		<!-- 动态 -->
		<view class="uh__section unida-card">
			<text class="uh__section-title">TA 的动态</text>
			<view class="uh__feed" v-for="(f, i) in feeds" :key="i">
				<view class="uh__feed-cover" :style="{ background: f.bg }"><text>{{ f.emoji }}</text></view>
				<text class="uh__feed-text">{{ f.text }}</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				following: false,
				stats: [{ num: 12, label: '动态' }, { num: 86, label: '获赞' }, { num: 24, label: '关注' }, { num: 132, label: '粉丝' }],
				tags: ['🏃 运动', '📚 学习', '🎮 游戏', '🎪 活动'],
				feeds: [
					{ emoji: '🌇', bg: 'linear-gradient(135deg,#FF8A3D,#FFD76A)', text: '中心湖的晚霞，随手拍都是大片！' },
					{ emoji: '🏀', bg: 'linear-gradient(135deg,#7B61FF,#B59BFF)', text: '周末约球，有没有一起的？' }
				]
			};
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onChat() { uni.navigateTo({ url: '/pages/chat/chat' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.uh { min-height: 100vh; background: $unida-bg; padding-bottom: 60rpx; }
	.uh__hero { background: linear-gradient(135deg,#7B61FF,#B59BFF); padding: 0 32rpx 60rpx; border-radius: 0 0 40rpx 40rpx; }
	.uh__nav { height: 120rpx; padding-top: 60rpx; display: flex; align-items: center; justify-content: space-between; }
	.uh__back { font-size: 48rpx; color: #fff; width: 60rpx; }
	.uh__nav-title { font-size: 32rpx; font-weight: 700; color: #fff; }
	.uh__more { font-size: 40rpx; color: #fff; width: 60rpx; text-align: right; }
	.uh__profile { display: flex; align-items: center; margin-top: 20rpx; }
	.uh__avatar { font-size: 120rpx; width: 140rpx; height: 140rpx; border-radius: 50%; background: #fff; display: flex; align-items: center; justify-content: center; border: 6rpx solid rgba(255,255,255,0.6); margin-right: 24rpx; }
	.uh__info { display: flex; flex-direction: column; }
	.uh__name { font-size: 38rpx; font-weight: 800; color: #fff; }
	.uh__verify { font-size: 28rpx; }
	.uh__sub { margin-top: 10rpx; font-size: 24rpx; color: rgba(255,255,255,0.9); }
	.uh__bio { display: block; margin-top: 24rpx; font-size: 26rpx; color: rgba(255,255,255,0.95); line-height: 1.6; }
	.uh__stats { display: flex; margin: -30rpx 24rpx 0; position: relative; padding: 28rpx 0; }
	.uh__stat { flex: 1; display: flex; flex-direction: column; align-items: center; }
	.uh__stat-num { font-size: 34rpx; font-weight: 800; color: $unida-primary; }
	.uh__stat-label { margin-top: 6rpx; font-size: 22rpx; color: $unida-text-sub; }
	.uh__actions { display: flex; gap: 20rpx; margin: 24rpx; }
	.uh__btn { flex: 1; height: 84rpx; border-radius: 999rpx; display: flex; align-items: center; justify-content: center; font-size: 28rpx; font-weight: 700; }
	.uh__btn--primary { background: linear-gradient(135deg,#7B61FF,#B59BFF); color: #fff; }
	.uh__btn--outline { background: #fff; color: $unida-primary; border: 2rpx solid $unida-primary; }
	.uh__btn--ghost { background: #f0ecf8; color: $unida-text-sub; }
	.uh__section { margin: 0 24rpx 20rpx; }
	.uh__section-title { display: block; font-size: 28rpx; font-weight: 700; color: $unida-text; margin-bottom: 18rpx; }
	.uh__tags { display: flex; flex-wrap: wrap; gap: 12rpx; }
	.uh__feed { display: flex; align-items: center; margin-bottom: 16rpx; }
	.uh__feed-cover { width: 100rpx; height: 100rpx; border-radius: 16rpx; display: flex; align-items: center; justify-content: center; font-size: 48rpx; margin-right: 16rpx; }
	.uh__feed-text { flex: 1; font-size: 26rpx; color: $unida-text; }
</style>
