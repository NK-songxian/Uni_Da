<template>
	<view class="pd unida-page">
		<view class="pd-safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 顶栏 -->
		<view class="pd__nav">
			<view class="pd__back" @click="goBack"><image class="pd__back-img" src="/static/icons-dark/back.png" mode="aspectFit" /></view>
			<text class="pd__title">帖子详情</text>
			<view class="pd__more" @click="onMore"><image class="pd__more-img" src="/static/icons-dark/bell.png" mode="aspectFit" /></view>
		</view>

		<scroll-view scroll-y class="pd__scroll">
			<!-- 帖子卡 -->
			<view class="pd__post">
				<view class="pd__head">
					<view class="pd__avatar" @click="goUser"><text class="pd__avatar-ch">阿</text></view>
					<view class="pd__user">
						<text class="pd__name" @click="goUser">阿星</text>
						<text class="pd__time">10分钟前 · 阳光大学</text>
					</view>
					<view class="pd__follow" :class="{ 'pd__follow--on': following }" @click="onFollow">
						<text class="pd__follow-t">{{ following ? '已关注' : '+ 关注' }}</text>
					</view>
				</view>
				<text class="pd__text">今天的晚霞也太美了吧！中心湖边随手一拍就是大片，分享给同样热爱生活的小伙伴们～</text>
				<view class="pd__images">
					<view class="pd__img" v-for="(g, i) in grads" :key="i" :style="{ background: g }"></view>
				</view>
				<view class="pd__tags">
					<view class="pd__tag pd__tag--purple"><text class="pd__tag-t"># 校园生活</text></view>
					<view class="pd__tag pd__tag--orange"><text class="pd__tag-t"># 摄影</text></view>
				</view>
				<view class="pd__stats">
					<view class="pd__stat"><image class="pd__stat-ico" src="/static/icons-dark/heart.png" mode="aspectFit" /><text class="pd__stat-n">{{ likes }} 赞</text></view>
					<view class="pd__stat"><image class="pd__stat-ico" src="/static/icons-dark/message.png" mode="aspectFit" /><text class="pd__stat-n">{{ comments.length }} 评论</text></view>
					<view class="pd__stat"><image class="pd__stat-ico" src="/static/icons-dark/box.png" mode="aspectFit" /><text class="pd__stat-n">{{ favs }} 收藏</text></view>
				</view>
			</view>

			<!-- 评论区 -->
			<view class="pd__comments">
				<text class="pd__ctitle">评论 ({{ comments.length }})</text>
				<view class="pd__comment" v-for="(c, i) in comments" :key="i">
					<view class="pd__cavatar" :class="'pd__cavatar--' + c.tone"><text class="pd__cavatar-ch">{{ c.name[0] }}</text></view>
					<view class="pd__cbody">
						<text class="pd__cname">{{ c.name }}</text>
						<text class="pd__ctext">{{ c.text }}</text>
						<text class="pd__ctime">{{ c.time }}</text>
					</view>
				</view>
			</view>
			<view class="pd__scroll-end"></view>
		</scroll-view>

		<!-- 评论输入栏 -->
		<view class="pd__inputbar">
			<input class="pd__input" :value="comment" placeholder="说点什么…" @input="onCommentInput" @confirm="sendComment" />
			<view class="pd__send" @click="sendComment"><text class="pd__send-t">发送</text></view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				following: false, likes: 128, favs: 36, comment: '',
				grads: ['linear-gradient(135deg,#FF8A3D,#FFD76A)', 'linear-gradient(135deg,#805CFA,#B59BFF)'],
				comments: [
					{ name: '小林', tone: 'green', text: '太好看了！哪个机位拍的？', time: '5分钟前' },
					{ name: 'Leo', tone: 'orange', text: '校园的晚霞真的绝了，改天一起去拍！', time: '2分钟前' }
				]
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			goBack() { uni.navigateBack(); },
			goUser() { uni.navigateTo({ url: '/pages/user-home/user-home' }); },
			onMore() { uni.showToast({ title: '举报 / 分享', icon: 'none' }); },
			onFollow() { this.following = !this.following; },
			onCommentInput(e) { this.comment = e.detail.value; },
			sendComment() {
				if (!this.comment.trim()) return;
				this.comments = this.comments.concat([{ name: '我', tone: 'purple', text: this.comment, time: '刚刚' }]);
				this.comment = '';
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.pd { height: 100vh; display: flex; flex-direction: column; box-sizing: border-box; padding: 0 $page-x; }

	.pd__nav { height: 110rpx; display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; }
	.pd__back {
		width: 68rpx; height: 68rpx;
		background: $c-white;
		border-radius: 50%;
		box-shadow: $sh-card;
		display: flex; align-items: center; justify-content: center;
	}
	.pd__back-img { width: 32rpx; height: 32rpx; }
	.pd__title { font-size: 34rpx; font-weight: 800; color: $c-ink; letter-spacing: 1rpx; }
	.pd__more {
		width: 68rpx; height: 68rpx;
		background: $c-white;
		border-radius: 50%;
		box-shadow: $sh-card;
		display: flex; align-items: center; justify-content: center;
	}
	.pd__more-img { width: 32rpx; height: 32rpx; }

	.pd__scroll { flex: 1; min-height: 0; }

	.pd__post {
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 28rpx;
		margin-top: 8rpx;
	}
	.pd__head { display: flex; align-items: center; }
	.pd__avatar { width: 84rpx; height: 84rpx; border-radius: 50%; background: $g-brand; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
	.pd__avatar-ch { font-size: 32rpx; color: $c-white; font-weight: 700; }
	.pd__user { flex: 1; margin: 0 16rpx; display: flex; flex-direction: column; min-width: 0; }
	.pd__name { font-size: 29rpx; font-weight: 700; color: $t-main; }
	.pd__time { margin-top: 6rpx; font-size: 21rpx; color: $t-tertiary; }
	.pd__follow {
		background: $g-brand;
		border-radius: $r-pill;
		padding: 12rpx 26rpx;
		flex-shrink: 0;
		box-shadow: 0 8rpx 16rpx rgba(128, 92, 250, 0.28);
	}
	.pd__follow--on { background: $c-ice; box-shadow: none; }
	.pd__follow--on .pd__follow-t { color: $t-sub; }
	.pd__follow-t { font-size: 24rpx; color: $c-white; font-weight: 700; }

	.pd__text { display: block; margin-top: 20rpx; font-size: 28rpx; color: $t-main; line-height: 1.7; }
	.pd__images { display: flex; margin-top: 20rpx; }
	.pd__img { flex: 1; height: 300rpx; border-radius: 20rpx; margin-right: 12rpx; }
	.pd__img:last-child { margin-right: 0; }
	.pd__tags { display: flex; margin-top: 20rpx; }
	.pd__tag { border-radius: $r-pill; padding: 8rpx 20rpx; margin-right: 12rpx; }
	.pd__tag--purple { background: rgba(128, 92, 250, 0.12); }
	.pd__tag--orange { background: rgba(255, 155, 119, 0.16); }
	.pd__tag--purple .pd__tag-t { color: $c-primary; }
	.pd__tag--orange .pd__tag-t { color: #E8734A; }
	.pd__tag-t { font-size: 22rpx; font-weight: 600; }
	.pd__stats {
		display: flex; align-items: center;
		margin-top: 24rpx; padding-top: 20rpx;
		border-top: 2rpx solid rgba(57, 0, 126, 0.06);
	}
	.pd__stat { display: flex; align-items: center; margin-right: 36rpx; }
	.pd__stat-ico { width: 32rpx; height: 32rpx; opacity: 0.55; }
	.pd__stat-n { margin-left: 10rpx; font-size: 23rpx; color: $t-sub; }

	.pd__comments {
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 28rpx;
		margin-top: 20rpx;
	}
	.pd__ctitle { display: block; font-size: 30rpx; font-weight: 800; color: $c-ink; }
	.pd__comment { display: flex; margin-top: 26rpx; }
	.pd__cavatar { width: 68rpx; height: 68rpx; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
	.pd__cavatar--green { background: linear-gradient(135deg, #29CA83, #6BE0B3); }
	.pd__cavatar--orange { background: $g-cta; }
	.pd__cavatar--purple { background: $g-brand; }
	.pd__cavatar-ch { font-size: 26rpx; color: $c-white; font-weight: 700; }
	.pd__cbody { flex: 1; margin-left: 16rpx; display: flex; flex-direction: column; min-width: 0; }
	.pd__cname { font-size: 25rpx; font-weight: 600; color: $t-main; }
	.pd__ctext { margin-top: 8rpx; font-size: 26rpx; color: $t-main; line-height: 1.6; }
	.pd__ctime { margin-top: 8rpx; font-size: 20rpx; color: $t-tertiary; }
	.pd__scroll-end { height: 40rpx; }

	.pd__inputbar {
		display: flex; align-items: center;
		flex-shrink: 0;
		padding: 16rpx 0 calc(16rpx + env(safe-area-inset-bottom));
		background: rgba(245, 240, 255, 0.96);
	}
	.pd__input {
		flex: 1; height: 76rpx;
		background: $c-white;
		border-radius: $r-pill;
		padding: 0 30rpx;
		font-size: 26rpx;
		color: $t-main;
		box-shadow: $sh-card;
		box-sizing: border-box;
	}
	.pd__send {
		margin-left: 16rpx;
		background: $g-cta;
		border-radius: $r-pill;
		padding: 20rpx 34rpx;
		flex-shrink: 0;
		box-shadow: 0 8rpx 16rpx rgba(255, 122, 82, 0.3);
	}
	.pd__send-t { font-size: 25rpx; color: $c-white; font-weight: 700; }
</style>
