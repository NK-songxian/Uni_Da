<template>
	<view class="ch">
		<!-- 导航 -->
		<view class="ch__nav">
			<text class="ch__back" @click="goBack">‹</text>
			<view class="ch__peer"><text class="ch__peer-avatar">😄</text><view><text class="ch__peer-name">周同学</text><text class="ch__peer-status">在线 · 已认证</text></view></view>
			<text class="ch__more">⋯</text>
		</view>

		<!-- 消息区 -->
		<scroll-view scroll-y class="ch__msgs" :scroll-top="scrollTop">
			<view class="ch__time">今天 10:24</view>
			<view class="ch__msg ch__msg--in">
				<text class="ch__msg-avatar">😄</text>
				<view class="ch__bubble">你好！看到你发布的跑腿需求，我可以帮你取～</view>
			</view>
			<view class="ch__msg ch__msg--in">
				<text class="ch__msg-avatar">😄</text>
				<view class="ch__bubble">我在东区，离北区驿站挺近的 😊</view>
			</view>
			<!-- 订单卡片 -->
			<view class="ch__ordercard">
				<view class="ch__ordercard-head"><text>🛵 跑腿订单</text><text class="ch__ordercard-status">待接单</text></view>
				<text class="ch__ordercard-title">帮忙取快递（中通北区）</text>
				<text class="ch__ordercard-reward">赏金 ¥8.00</text>
			</view>
			<view class="ch__msg ch__msg--out">
				<view class="ch__bubble">太好了！取件码我私你，送到东园3栋楼下就行～</view>
				<text class="ch__msg-avatar">😄</text>
			</view>
			<view class="ch__msg ch__msg--in">
				<text class="ch__msg-avatar">😄</text>
				<view class="ch__bubble">没问题，大概半小时到 👌</view>
			</view>
		</scroll-view>

		<!-- 输入区 -->
		<view class="ch__inputbar">
			<text class="ch__tool" @click="onTool">＋</text>
			<input class="ch__input" v-model="text" placeholder="发消息…" @confirm="send" />
			<view class="ch__send" @click="send">发送</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return { text: '', scrollTop: 0, msgs: [] };
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onTool() { uni.showToast({ title: '更多工具待接入', icon: 'none' }); },
			send() {
				if (!this.text.trim()) return;
				// 演示：真实聊天需接入会话架构 + 实时推送（uniCloud 需评估能力）
				this.msgs.push(this.text);
				this.text = '';
				uni.showToast({ title: '消息已发送（演示）', icon: 'none' });
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.ch { height: 100vh; display: flex; flex-direction: column; background: $unida-bg; }
	.ch__nav { height: 140rpx; padding: 60rpx 24rpx 0; display: flex; align-items: center; background: #fff; }
	.ch__back { font-size: 48rpx; width: 60rpx; }
	.ch__peer { flex: 1; display: flex; align-items: center; }
	.ch__peer-avatar { font-size: 48rpx; margin-right: 14rpx; }
	.ch__peer view { display: flex; flex-direction: column; }
	.ch__peer-name { font-size: 28rpx; font-weight: 700; }
	.ch__peer-status { font-size: 20rpx; color: $unida-green; margin-top: 4rpx; }
	.ch__more { font-size: 40rpx; width: 60rpx; text-align: right; }
	.ch__msgs { flex: 1; padding: 24rpx; }
	.ch__time { text-align: center; font-size: 22rpx; color: $unida-text-sub; margin: 12rpx 0 28rpx; }
	.ch__msg { display: flex; align-items: flex-start; margin-bottom: 28rpx; }
	.ch__msg-avatar { width: 72rpx; height: 72rpx; border-radius: 50%; background: linear-gradient(135deg,#B59BFF,#7B61FF); display: flex; align-items: center; justify-content: center; font-size: 40rpx; flex-shrink: 0; }
	.ch__bubble { max-width: 70%; padding: 22rpx 26rpx; font-size: 26rpx; line-height: 1.6; }
	.ch__msg--in .ch__bubble { background: #fff; border-radius: 6rpx 24rpx 24rpx 24rpx; margin-left: 16rpx; color: $unida-text; }
	.ch__msg--out { justify-content: flex-end; }
	.ch__msg--out .ch__bubble { background: linear-gradient(135deg,#7B61FF,#B59BFF); border-radius: 24rpx 6rpx 24rpx 24rpx; margin-right: 16rpx; color: #fff; }
	.ch__ordercard { background: #fff; border-radius: 20rpx; padding: 24rpx; margin: 0 88rpx 28rpx; box-shadow: 0 6rpx 18rpx rgba(123,97,255,0.08); }
	.ch__ordercard-head { display: flex; justify-content: space-between; font-size: 24rpx; color: $unida-text-sub; }
	.ch__ordercard-status { color: $unida-orange; }
	.ch__ordercard-title { display: block; margin-top: 16rpx; font-size: 26rpx; font-weight: 600; color: $unida-text; }
	.ch__ordercard-reward { display: block; margin-top: 10rpx; font-size: 28rpx; font-weight: 800; color: $unida-orange; }
	.ch__inputbar { display: flex; align-items: center; padding: 16rpx 24rpx calc(16rpx + env(safe-area-inset-bottom)); background: #fff; }
	.ch__tool { font-size: 44rpx; color: $unida-text-sub; width: 60rpx; }
	.ch__input { flex: 1; height: 72rpx; background: $unida-bg; border-radius: 999rpx; padding: 0 28rpx; font-size: 26rpx; }
	.ch__send { margin-left: 16rpx; font-size: 26rpx; color: #fff; background: linear-gradient(135deg,#7B61FF,#B59BFF); padding: 16rpx 30rpx; border-radius: 999rpx; }
</style>
