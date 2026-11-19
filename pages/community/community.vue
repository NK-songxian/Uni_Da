<template>
	<view class="cm unida-page unida-page--tab">
		<view class="cm__top">
			<text class="cm__title">社区</text>
			<view class="cm__tabs">
				<text v-for="(t, i) in tabs" :key="i" :class="{ 'cm__tab--on': active === i }" @click="active = i">{{ t }}</text>
			</view>
		</view>
		<view class="cm__publish" @click="onPublish">
			<text class="cm__publish-avatar">😄</text>
			<text class="cm__publish-ph">分享你的校园生活…</text>
			<text class="cm__publish-btn">发布</text>
		</view>
		<view class="cm__list">
			<view class="cm__post unida-card" v-for="(p, i) in posts" :key="i" @click="openPost(p)">
				<view class="cm__post-head">
					<text class="cm__post-avatar">{{ p.avatar }}</text>
					<view class="cm__post-user"><text class="cm__post-name">{{ p.user }}</text><text class="cm__post-time">{{ p.time }}</text></view>
					<text class="cm__post-tag">{{ p.tag }}</text>
				</view>
				<text class="cm__post-text">{{ p.text }}</text>
				<view class="cm__post-images" v-if="p.images">
					<view class="cm__post-img" v-for="(im, j) in p.images" :key="j" :style="{ background: im }"><text>{{ p.emoji }}</text></view>
				</view>
				<view class="cm__post-actions">
					<text @click.stop="onLike(i)">👍 {{ p.likes }}</text>
					<text @click.stop="onComment(p)">💬 {{ p.comments }}</text>
					<text @click.stop="onFav(i)">{{ p.faved ? '⭐' : '☆' }} {{ p.favs }}</text>
					<text @click.stop="onShare">↗ 分享</text>
				</view>
			</view>
		</view>
		<unida-tabbar :current="1" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';
	export default {
		components: { unidaTabbar },
		data() {
			return {
				tabs: ['推荐', '关注', '同校'],
				active: 0,
				posts: [
					{ avatar: '😄', user: '阿星', time: '10分钟前', tag: '校园生活', text: '今天的晚霞也太美了吧！中心湖边随手一拍就是大片 📷', images: ['linear-gradient(135deg,#FF8A3D,#FFD76A)','linear-gradient(135deg,#7B61FF,#B59BFF)'], emoji: '🌇', likes: 128, comments: 24, favs: 36, faved: false },
					{ avatar: '🤩', user: '小林同学', time: '1小时前', tag: '找搭子', text: '有人一起去图书馆刷题吗？期末了，互相监督！📚 位置已经占好啦～', images: [], emoji: '', likes: 45, comments: 18, favs: 12, faved: false }
				]
			};
		},
		methods: {
			onPublish() { uni.showToast({ title: '发布动态待接入', icon: 'none' }); },
			openPost(p) { uni.navigateTo({ url: '/pages/post-detail/post-detail' }); },
			onLike(i) { this.posts[i].likes++; },
			onComment() { uni.navigateTo({ url: '/pages/post-detail/post-detail' }); },
			onFav(i) { this.posts[i].faved = !this.posts[i].faved; this.posts[i].favs += this.posts[i].faved ? 1 : -1; },
			onShare() { uni.showToast({ title: '分享待接入', icon: 'none' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.cm__top { padding: 60rpx 24rpx 0; }
	.cm__title { display: block; font-size: 44rpx; font-weight: 800; color: $unida-text; }
	.cm__tabs { display: flex; gap: 36rpx; margin-top: 20rpx; }
	.cm__tabs text { font-size: 28rpx; color: $unida-text-sub; }
	.cm__tabs .cm__tab--on { color: $unida-primary; font-weight: 700; }
	.cm__publish { display: flex; align-items: center; margin: 24rpx; padding: 20rpx 24rpx; background: #fff; border-radius: 999rpx; box-shadow: 0 6rpx 20rpx rgba(123,97,255,0.08); }
	.cm__publish-avatar { font-size: 44rpx; margin-right: 16rpx; }
	.cm__publish-ph { flex: 1; font-size: 26rpx; color: $unida-text-sub; }
	.cm__publish-btn { font-size: 24rpx; color: #fff; background: linear-gradient(135deg,#7B61FF,#B59BFF); padding: 12rpx 28rpx; border-radius: 999rpx; }
	.cm__post { margin: 0 24rpx 20rpx; }
	.cm__post-head { display: flex; align-items: center; }
	.cm__post-avatar { font-size: 48rpx; margin-right: 14rpx; }
	.cm__post-user { flex: 1; display: flex; flex-direction: column; }
	.cm__post-name { font-size: 28rpx; font-weight: 700; color: $unida-text; }
	.cm__post-time { margin-top: 4rpx; font-size: 20rpx; color: $unida-text-sub; }
	.cm__post-tag { font-size: 20rpx; color: $unida-primary; background: rgba(123,97,255,0.08); padding: 6rpx 16rpx; border-radius: 999rpx; }
	.cm__post-text { display: block; margin-top: 18rpx; font-size: 27rpx; color: $unida-text; line-height: 1.6; }
	.cm__post-images { display: flex; gap: 12rpx; margin-top: 18rpx; }
	.cm__post-img { flex: 1; height: 240rpx; border-radius: 16rpx; display: flex; align-items: center; justify-content: center; }
	.cm__post-img text { font-size: 72rpx; }
	.cm__post-actions { display: flex; justify-content: space-between; margin-top: 22rpx; padding-top: 18rpx; border-top: 2rpx solid $unida-divider; }
	.cm__post-actions text { font-size: 24rpx; color: $unida-text-sub; }
</style>
