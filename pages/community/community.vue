<template>
	<view class="cm unida-page unida-page--tab">
		<view class="cm__safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 顶栏 + 分类 -->
		<view class="cm__top">
			<text class="cm__title">社区</text>
			<text class="cm__sub">看看同学们在玩什么</text>
			<view class="cm__tabs">
				<view class="cm__tab" v-for="(t, i) in tabs" :key="i" :class="{ 'cm__tab--on': active === i }" @click="onTab(i)">
					<text class="cm__tab-t">{{ t }}</text>
				</view>
			</view>
		</view>

		<!-- 发布入口 -->
		<view class="cm__publish" @click="onPublish">
			<view class="cm__pub-avatar"><text class="cm__pub-avatar-ch">我</text></view>
			<text class="cm__pub-ph">分享你的校园生活…</text>
			<view class="cm__pub-btn"><text class="cm__pub-btn-t">发布</text></view>
		</view>

		<!-- 帖子列表 -->
		<view class="cm__post" v-for="(p, i) in posts" :key="i" @click="openPost(i)">
			<view class="cm__post-head">
				<view class="cm__post-avatar" :class="'cm__post-avatar--' + p.tone"><text class="cm__post-avatar-ch">{{ p.user[0] }}</text></view>
				<view class="cm__post-user">
					<text class="cm__post-name">{{ p.user }}</text>
					<text class="cm__post-time">{{ p.time }} · {{ p.campus }}</text>
				</view>
				<view class="cm__post-tag" :class="'cm__post-tag--' + p.tone"><text class="cm__post-tag-t">{{ p.tag }}</text></view>
			</view>
			<text class="cm__post-text">{{ p.text }}</text>
			<view class="cm__post-images" v-if="p.images.length">
				<view class="cm__post-img" v-for="(g, j) in p.images" :key="j" :style="{ background: g }"></view>
			</view>
			<view class="cm__post-actions">
				<view class="cm__act" @click.stop="onLike(i)">
					<image class="cm__act-ico" src="/static/icons-dark/heart.png" mode="aspectFit" />
					<text class="cm__act-n">{{ p.likes }}</text>
				</view>
				<view class="cm__act" @click.stop="onComment(i)">
					<image class="cm__act-ico" src="/static/icons-dark/message.png" mode="aspectFit" />
					<text class="cm__act-n">{{ p.comments }}</text>
				</view>
				<view class="cm__act" :class="{ 'cm__act--fav': p.faved }" @click.stop="onFav(i)">
					<image class="cm__act-ico" src="/static/icons-dark/box.png" mode="aspectFit" />
					<text class="cm__act-n">{{ p.favs }}</text>
				</view>
				<view class="cm__act" @click.stop="onShare(i)">
					<image class="cm__act-ico" src="/static/icons-dark/chevron.png" mode="aspectFit" />
					<text class="cm__act-n">分享</text>
				</view>
			</view>
		</view>

		<view class="cm__bottom-space"></view>
		<unida-tabbar :current="1" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';
	export default {
		components: { unidaTabbar },
		data() {
			return {
				statusBar: 0,
				tabs: ['推荐', '关注', '同校'],
				active: 0,
				posts: [
					{ user: '阿星', tone: 'purple', campus: '阳光大学', time: '10分钟前', tag: '校园生活', text: '今天的晚霞也太美了吧！中心湖边随手一拍就是大片，分享给同样热爱生活的小伙伴们～', images: ['linear-gradient(135deg,#FF8A3D,#FFD76A)', 'linear-gradient(135deg,#805CFA,#B59BFF)'], likes: 128, comments: 24, favs: 36, liked: false, faved: false },
					{ user: '小林同学', tone: 'green', campus: '阳光大学', time: '1小时前', tag: '找搭子', text: '有人一起去图书馆刷题吗？期末了，互相监督！位置已经占好啦，三楼靠窗～', images: [], likes: 45, comments: 18, favs: 12, liked: true, faved: false },
					{ user: '丸子', tone: 'orange', campus: '阳光大学', time: '2小时前', tag: '社团活动', text: '周六下午街舞社在天台有公开课，零基础也能来玩，带上水就行！', images: ['linear-gradient(135deg,#F472B6,#FF8A3D)'], likes: 89, comments: 31, favs: 27, liked: false, faved: false }
				]
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			onTab(i) { this.active = i; },
			onPublish() { uni.navigateTo({ url: '/pages/publish/publish' }); },
			openPost(i) { uni.navigateTo({ url: '/pages/post-detail/post-detail' }); },
			onLike(i) {
				this.posts = this.posts.map((x, j) => j === i ? { user: x.user, tone: x.tone, campus: x.campus, time: x.time, tag: x.tag, text: x.text, images: x.images, likes: x.likes + (x.liked ? -1 : 1), comments: x.comments, favs: x.favs, liked: !x.liked, faved: x.faved } : x);
			},
			onComment(i) { uni.navigateTo({ url: '/pages/post-detail/post-detail' }); },
			onFav(i) {
				this.posts = this.posts.map((x, j) => j === i ? { user: x.user, tone: x.tone, campus: x.campus, time: x.time, tag: x.tag, text: x.text, images: x.images, likes: x.likes, comments: x.comments, favs: x.favs + (x.faved ? -1 : 1), liked: x.liked, faved: !x.faved } : x);
			},
			onShare(i) { uni.showToast({ title: '分享卡片待接入', icon: 'none' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.cm { padding: 0 $page-x 0; box-sizing: border-box; }

	.cm__top { display: flex; flex-direction: column; }
	.cm__title { font-size: 44rpx; font-weight: 800; color: $c-ink; letter-spacing: 1rpx; }
	.cm__sub { margin-top: 8rpx; font-size: 24rpx; color: $t-tertiary; }
	.cm__tabs { display: flex; margin-top: 24rpx; background: $c-white; border-radius: $r-pill; padding: 6rpx; box-shadow: $sh-card; }
	.cm__tab { flex: 1; height: 72rpx; border-radius: $r-pill; display: flex; align-items: center; justify-content: center; }
	.cm__tab--on { background: $g-brand; box-shadow: 0 8rpx 16rpx rgba(128, 92, 250, 0.28); }
	.cm__tab-t { font-size: 26rpx; color: $t-sub; font-weight: 600; }
	.cm__tab--on .cm__tab-t { color: $c-white; font-weight: 700; }

	.cm__publish {
		display: flex; align-items: center;
		margin-top: 24rpx;
		background: $c-white;
		border-radius: $r-pill;
		box-shadow: $sh-card;
		padding: 14rpx 16rpx 14rpx 14rpx;
	}
	.cm__pub-avatar { width: 64rpx; height: 64rpx; border-radius: 50%; background: $g-cta; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
	.cm__pub-avatar-ch { font-size: 26rpx; color: $c-white; font-weight: 700; }
	.cm__pub-ph { flex: 1; margin-left: 16rpx; font-size: 26rpx; color: $t-tertiary; }
	.cm__pub-btn { background: $g-cta; border-radius: $r-pill; padding: 14rpx 30rpx; box-shadow: 0 8rpx 16rpx rgba(255, 122, 82, 0.3); flex-shrink: 0; }
	.cm__pub-btn-t { font-size: 24rpx; color: $c-white; font-weight: 700; }

	.cm__post {
		margin-top: 20rpx;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 28rpx;
	}
	.cm__post-head { display: flex; align-items: center; }
	.cm__post-avatar { width: 76rpx; height: 76rpx; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
	.cm__post-avatar--purple { background: $g-brand; }
	.cm__post-avatar--green { background: linear-gradient(135deg, #29CA83, #6BE0B3); }
	.cm__post-avatar--orange { background: $g-cta; }
	.cm__post-avatar-ch { font-size: 30rpx; color: $c-white; font-weight: 700; }
	.cm__post-user { flex: 1; margin: 0 16rpx; display: flex; flex-direction: column; min-width: 0; }
	.cm__post-name { font-size: 28rpx; font-weight: 700; color: $t-main; }
	.cm__post-time { margin-top: 6rpx; font-size: 21rpx; color: $t-tertiary; }
	.cm__post-tag { border-radius: $r-pill; padding: 8rpx 18rpx; flex-shrink: 0; }
	.cm__post-tag--purple { background: rgba(128, 92, 250, 0.12); }
	.cm__post-tag--green { background: rgba(41, 202, 131, 0.14); }
	.cm__post-tag--orange { background: rgba(255, 155, 119, 0.16); }
	.cm__post-tag-t { font-size: 21rpx; color: $c-primary; font-weight: 600; }
	.cm__post-tag--green .cm__post-tag-t { color: #1FA86A; }
	.cm__post-tag--orange .cm__post-tag-t { color: #E8734A; }

	.cm__post-text { display: block; margin-top: 18rpx; font-size: 27rpx; color: $t-main; line-height: 1.65; }

	.cm__post-images { display: flex; margin-top: 18rpx; }
	.cm__post-img {
		flex: 1; height: 220rpx; border-radius: 20rpx;
		display: flex; align-items: center; justify-content: center;
		margin-right: 12rpx;
	}
	.cm__post-img:last-child { margin-right: 0; }

	.cm__post-actions {
		display: flex; align-items: center; justify-content: space-between;
		margin-top: 24rpx; padding-top: 20rpx;
		border-top: 2rpx solid rgba(57, 0, 126, 0.06);
	}
	.cm__act { display: flex; align-items: center; }
	.cm__act-ico { width: 34rpx; height: 34rpx; opacity: 0.55; }
	.cm__act-n { margin-left: 10rpx; font-size: 24rpx; color: $t-sub; font-family: $ff-num; }
	.cm__act--fav .cm__act-ico { opacity: 1; }
	.cm__act--fav .cm__act-n { color: $c-primary; font-weight: 700; }

	.cm__bottom-space { height: 140rpx; }
</style>
