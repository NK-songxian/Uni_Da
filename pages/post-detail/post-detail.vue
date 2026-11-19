<template>
	<view class="pd unida-page">
		<view class="pd__nav"><text class="pd__back" @click="goBack">‹</text><text class="pd__title">帖子详情</text><text class="pd__more" @click="onMore">⋯</text></view>
		<scroll-view scroll-y class="pd__scroll">
			<view class="pd__post unida-card">
				<view class="pd__head">
					<text class="pd__avatar" @click="goUser">😄</text>
					<view class="pd__user"><text class="pd__name" @click="goUser">阿星</text><text class="pd__time">10分钟前 · 阳光大学</text></view>
					<view class="pd__follow" @click="following = !following">{{ following ? '已关注' : '+ 关注' }}</view>
				</view>
				<text class="pd__text">今天的晚霞也太美了吧！中心湖边随手一拍就是大片 📷 分享给同样热爱生活的小伙伴们～</text>
				<view class="pd__images"><view class="pd__img" v-for="(g, i) in grads" :key="i" :style="{ background: g }"><text>🌇</text></view></view>
				<view class="pd__tags"><text class="unida-tag unida-tag--purple">#校园生活</text><text class="unida-tag unida-tag--orange"># Photography</text></view>
				<view class="pd__stats"><text>👍 {{ likes }} 赞</text><text>💬 {{ comments.length }} 评论</text><text>⭐ {{ favs }} 收藏</text></view>
			</view>
			<!-- 评论区 -->
			<view class="pd__comments unida-card">
				<text class="pd__ctitle">评论 ({{ comments.length }})</text>
				<view class="pd__comment" v-for="(c, i) in comments" :key="i">
					<text class="pd__cavatar">{{ c.avatar }}</text>
					<view class="pd__cbody"><text class="pd__cname">{{ c.name }}</text><text class="pd__ctext">{{ c.text }}</text><text class="pd__ctime">{{ c.time }}</text></view>
				</view>
			</view>
		</scroll-view>
		<!-- 评论输入 -->
		<view class="pd__inputbar">
			<input class="pd__input" v-model="comment" placeholder="说点什么…" @confirm="sendComment" />
			<text class="pd__send" @click="sendComment">发送</text>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				following: false, likes: 128, favs: 36, comment: '',
				grads: ['linear-gradient(135deg,#FF8A3D,#FFD76A)', 'linear-gradient(135deg,#7B61FF,#B59BFF)'],
				comments: [
					{ avatar: '🤩', name: '小林', text: '太好看了！哪个机位拍的？', time: '5分钟前' },
					{ avatar: '😎', name: 'Leo', text: '校园的晚霞真的绝了 👏', time: '2分钟前' }
				]
			};
		},
		methods: {
			goBack() { uni.navigateBack(); },
			goUser() { uni.navigateTo({ url: '/pages/user-home/user-home' }); },
			onMore() { uni.showToast({ title: '举报/分享', icon: 'none' }); },
			sendComment() {
				if (!this.comment.trim()) return;
				this.comments.push({ avatar: '😄', name: '我', text: this.comment, time: '刚刚' });
				this.comment = '';
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.pd { height: 100vh; display: flex; flex-direction: column; }
	.pd__nav { height: 120rpx; padding: 60rpx 24rpx 0; display: flex; align-items: center; justify-content: space-between; background: #fff; }
	.pd__back { font-size: 48rpx; width: 60rpx; }
	.pd__title { font-size: 32rpx; font-weight: 700; }
	.pd__more { font-size: 40rpx; width: 60rpx; text-align: right; }
	.pd__scroll { flex: 1; }
	.pd__post { margin: 20rpx 24rpx; }
	.pd__head { display: flex; align-items: center; }
	.pd__avatar { font-size: 56rpx; margin-right: 16rpx; }
	.pd__user { flex: 1; display: flex; flex-direction: column; }
	.pd__name { font-size: 28rpx; font-weight: 700; color: $unida-text; }
	.pd__time { margin-top: 6rpx; font-size: 20rpx; color: $unida-text-sub; }
	.pd__follow { font-size: 24rpx; color: #fff; background: linear-gradient(135deg,#7B61FF,#B59BFF); padding: 10rpx 24rpx; border-radius: 999rpx; }
	.pd__text { display: block; margin-top: 20rpx; font-size: 28rpx; line-height: 1.7; color: $unida-text; }
	.pd__images { display: flex; gap: 12rpx; margin-top: 20rpx; }
	.pd__img { flex: 1; height: 300rpx; border-radius: 16rpx; display: flex; align-items: center; justify-content: center; }
	.pd__img text { font-size: 96rpx; }
	.pd__tags { display: flex; gap: 12rpx; margin-top: 20rpx; }
	.pd__stats { display: flex; gap: 32rpx; margin-top: 24rpx; padding-top: 20rpx; border-top: 2rpx solid $unida-divider; }
	.pd__stats text { font-size: 24rpx; color: $unida-text-sub; }
	.pd__comments { margin: 0 24rpx 20rpx; }
	.pd__ctitle { display: block; font-size: 28rpx; font-weight: 700; color: $unida-text; margin-bottom: 20rpx; }
	.pd__comment { display: flex; margin-bottom: 24rpx; }
	.pd__cavatar { font-size: 44rpx; margin-right: 14rpx; }
	.pd__cbody { flex: 1; display: flex; flex-direction: column; }
	.pd__cname { font-size: 26rpx; font-weight: 600; color: $unida-text; }
	.pd__ctext { margin-top: 6rpx; font-size: 26rpx; color: #4a4560; }
	.pd__ctime { margin-top: 6rpx; font-size: 20rpx; color: $unida-text-sub; }
	.pd__inputbar { display: flex; align-items: center; padding: 16rpx 24rpx calc(16rpx + env(safe-area-inset-bottom)); background: #fff; }
	.pd__input { flex: 1; height: 72rpx; background: $unida-bg; border-radius: 999rpx; padding: 0 28rpx; font-size: 26rpx; }
	.pd__send { margin-left: 16rpx; font-size: 26rpx; color: #fff; background: linear-gradient(135deg,#7B61FF,#B59BFF); padding: 16rpx 28rpx; border-radius: 999rpx; }
</style>
