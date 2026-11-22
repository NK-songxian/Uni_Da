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
			<view class="pd__post" v-if="post.id">
				<view class="pd__head">
					<view class="pd__avatar" @click="goUser"><text class="pd__avatar-ch">{{ post.user[0] }}</text></view>
					<view class="pd__user">
						<text class="pd__name" @click="goUser">{{ post.user }}</text>
						<text class="pd__time">{{ post.time }} · {{ post.campus }}</text>
					</view>
					<view class="pd__follow" :class="{ 'pd__follow--on': following }" @click="onFollow">
						<text class="pd__follow-t">{{ following ? '已关注' : '+ 关注' }}</text>
					</view>
				</view>
				<text class="pd__text">{{ post.text }}</text>
				<view class="pd__images" v-if="post.images.length">
					<block v-for="(g, i) in post.images" :key="i">
						<image v-if="isHttpImg(g)" class="pd__img pd__img--pic" :src="g" mode="aspectFill" @click="previewImg(i)" />
						<view v-else class="pd__img" :style="{ background: g }"></view>
					</block>
				</view>
				<view class="pd__tags">
					<view class="pd__tag pd__tag--purple"><text class="pd__tag-t"># {{ post.tag }}</text></view>
				</view>
				<view class="pd__stats">
					<view class="pd__stat" :class="{ 'pd__stat--on': post.liked }" @click="onLike">
						<image class="pd__stat-ico" src="/static/icons-dark/heart.png" mode="aspectFit" /><text class="pd__stat-n">{{ post.likes }} 赞</text>
					</view>
					<view class="pd__stat"><image class="pd__stat-ico" src="/static/icons-dark/message.png" mode="aspectFit" /><text class="pd__stat-n">{{ comments.length }} 评论</text></view>
					<view class="pd__stat" :class="{ 'pd__stat--on': post.faved }" @click="onFav">
						<image class="pd__stat-ico" src="/static/icons-dark/box.png" mode="aspectFit" /><text class="pd__stat-n">{{ post.favs }} 收藏</text>
					</view>
				</view>
			</view>

			<!-- 评论区 -->
			<view class="pd__comments">
				<text class="pd__ctitle">评论 ({{ comments.length }})</text>
				<view class="pd__comment" v-for="(c, i) in comments" :key="c.id || i">
					<view class="pd__cavatar" :class="'pd__cavatar--' + c.tone"><text class="pd__cavatar-ch">{{ c.name[0] }}</text></view>
					<view class="pd__cbody">
						<text class="pd__cname">{{ c.name }}</text>
						<text class="pd__ctext">{{ c.text }}</text>
						<text class="pd__ctime">{{ c.time }}</text>
					</view>
				</view>
				<text class="pd__cempty" v-if="comments.length === 0">还没有评论，来说点什么吧～</text>
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
	import { callCloud, getToken } from '@/common/cloud.js';
	import { timeAgo } from '@/common/fmt.js';

	export default {
		data() {
			return {
				statusBar: 0,
				postId: '',
				loading: false,
				following: false,
				comment: '',
				sendBusy: false,
				post: { id: '', user: '', tone: 'purple', campus: '', time: '', tag: '', text: '', images: [], likes: 0, comments: 0, favs: 0, liked: false, faved: false },
				comments: []
			};
		},
		onLoad(options) {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
			this.postId = (options && options.id) || '';
			this.loadDetail();
		},
		methods: {
			goBack() { uni.navigateBack(); },
			goUser() { uni.navigateTo({ url: '/pages/user-home/user-home' }); },
			isHttpImg(g) { return String(g || '').indexOf('http') === 0; },
			previewImg(i) {
				const urls = (this.post.images || []).filter((g) => this.isHttpImg(g));
				if (!urls.length) return;
				uni.previewImage({ urls, current: Math.max(0, urls.indexOf(this.post.images[i])) });
			},
			onMore() { uni.showActionSheet({ itemList: ['举报该帖子'], success: () => uni.navigateTo({ url: '/pages/report/report' }) }); },
			onFollow() { this.following = !this.following; },
			onCommentInput(e) { this.comment = e.detail.value; },
			async loadDetail() {
				if (!this.postId || this.loading) return;
				this.loading = true;
				try {
					const r = await callCloud('posts', { action: 'detail', postId: this.postId, token: getToken() });
					const p = r.post || {};
					this.post = { ...p, time: p.time || timeAgo(p.ts) };
					this.comments = (r.comments || []).map((c) => ({ ...c, time: timeAgo(c.ts) }));
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '加载失败', icon: 'none' });
				} finally {
					this.loading = false;
				}
			},
			async onLike() {
				const p = this.post;
				if (!p.id) return;
				try {
					const r = await callCloud('like', { action: 'toggle', token: getToken(), postId: p.id });
					this.post = { ...p, liked: !!r.liked, likes: typeof r.likes === 'number' ? r.likes : p.likes };
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '点赞失败', icon: 'none' });
				}
			},
			async onFav() {
				const p = this.post;
				if (!p.id) return;
				try {
					const r = await callCloud('favorite', {
						action: 'toggle',
						token: getToken(),
						type: 'post',
						targetId: p.id,
						title: p.tag + ' · ' + p.user,
						cover: '',
						desc: String(p.text || '').slice(0, 80)
					});
					const faved = !!r.faved;
					this.post = { ...p, faved, favs: Math.max(0, p.favs + (faved ? 1 : -1)) };
					uni.showToast({ title: faved ? '已收藏' : '已取消收藏', icon: 'none' });
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '收藏失败', icon: 'none' });
				}
			},
			async sendComment() {
				const text = this.comment.trim();
				if (!text || this.sendBusy || !this.postId) return;
				this.sendBusy = true;
				try {
					const r = await callCloud('posts', {
						action: 'comment',
						token: getToken(),
						postId: this.postId,
						text
					});
					if (r.comment) {
						this.comments = this.comments.concat([{ ...r.comment, time: '刚刚' }]);
					}
					this.post = { ...this.post, comments: this.post.comments + 1 };
					this.comment = '';
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '评论失败', icon: 'none' });
				} finally {
					this.sendBusy = false;
				}
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
	.pd__img--pic { width: 100%; }
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
	.pd__stat--on .pd__stat-ico { opacity: 1; }
	.pd__stat--on .pd__stat-n { color: $c-primary; font-weight: 700; }

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
	.pd__cempty { display: block; margin-top: 24rpx; font-size: 24rpx; color: $t-tertiary; }
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
