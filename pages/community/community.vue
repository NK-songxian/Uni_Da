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
		<view class="cm__post" v-for="(p, i) in posts" :key="p.id" @click="openPost(i)">
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
					<block v-for="(g, j) in p.images" :key="j">
						<image v-if="isHttpImg(g)" class="cm__post-img cm__post-img--pic" :src="g" mode="aspectFill" @click="previewPostImg(p.images, j)" />
						<view v-else class="cm__post-img" :style="{ background: g }"></view>
					</block>
				</view>
			<view class="cm__post-actions">
				<view class="cm__act" :class="{ 'cm__act--fav': p.liked }" @click.stop="onLike(i)">
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

		<!-- 品牌空态 -->
		<view class="cm__empty" v-if="!loading && posts.length === 0">
			<text class="cm__empty-t">还没有帖子，来发第一条吧～</text>
		</view>

		<view class="cm__bottom-space"></view>
		<unida-tabbar :current="1" />

		<!-- ══════════ 发帖弹层 ══════════ -->
		<view class="cm__mask" v-if="showPublish" @click="closePublish"></view>
		<view class="cm__sheet" v-if="showPublish">
			<view class="cm__sheet-head">
				<text class="cm__sheet-title">发布动态</text>
				<text class="cm__sheet-close" @click="closePublish">×</text>
			</view>
			<textarea class="cm__sheet-input" v-model="draft" :maxlength="500" placeholder="分享你的校园生活，搭子们都在看…" />
			<view class="cm__imgs">
				<view class="cm__img" v-for="(g, i) in pubImgs" :key="i">
					<image class="cm__img-pic" :src="g" mode="aspectFill" @click="previewPubImg(i)" />
					<view class="cm__img-del" @click.stop="removePubImg(i)"><text class="cm__img-del-t">×</text></view>
				</view>
				<view class="cm__img cm__img--add" v-if="pubImgs.length < 6" @click="addPubImg">
					<text class="cm__img-add-ico">＋</text>
					<text class="cm__img-add-n">{{ pubImgs.length }}/6</text>
				</view>
			</view>
			<view class="cm__sheet-tags">
				<view
					class="cm__sheet-tag"
					v-for="(t, i) in pubTags"
					:key="i"
					:class="{ 'cm__sheet-tag--on': pubTag === t }"
					@click="pubTag = t"
				>
					<text class="cm__sheet-tag-t">{{ t }}</text>
				</view>
			</view>
			<view class="cm__sheet-btn" :class="{ 'cm__sheet-btn--off': !draft.trim() || pubBusy }" @click="submitPost">
				<text class="cm__sheet-btn-t">{{ pubBusy ? '发布中…' : '发布' }}</text>
			</view>
		</view>
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';
	import { callCloud, getToken } from '@/common/cloud.js';
	import { uploadImages } from '@/common/upload.js';
	import { timeAgo } from '@/common/fmt.js';

	export default {
		components: { unidaTabbar },
		data() {
			return {
				statusBar: 0,
				loading: false,
				tabs: ['推荐', '关注', '同校'],
				active: 0,
				posts: [],
				// 发帖弹层
				showPublish: false,
				draft: '',
				pubTag: '校园生活',
				pubTags: ['校园生活', '找搭子', '社团活动', '学习打卡', '运动', '美食'],
				pubImgs: [],
				pubBusy: false
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		onShow() {
			this.loadPosts();
		},
		onPullDownRefresh() {
			this.loadPosts();
		},
		methods: {
			async loadPosts() {
				if (this.loading) return;
				this.loading = true;
				try {
					const r = await callCloud('posts', { action: 'list', token: getToken() });
					this.posts = (r.list || []).map((x) => ({ ...x, time: x.time || timeAgo(x.ts) }));
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '加载帖子失败', icon: 'none' });
				} finally {
					this.loading = false;
					uni.stopPullDownRefresh();
				}
			},
			onTab(i) { this.active = i; },
			onPublish() {
				this.draft = '';
				this.pubTag = this.pubTags[0];
				this.pubImgs = [];
				this.showPublish = true;
			},
			closePublish() { this.showPublish = false; },
			isHttpImg(g) { return String(g || '').indexOf('http') === 0; },
			previewPostImg(imgs, i) {
				const urls = (imgs || []).filter((g) => this.isHttpImg(g));
				if (!urls.length) return;
				uni.previewImage({ urls, current: urls.indexOf(imgs[i]) >= 0 ? urls.indexOf(imgs[i]) : 0 });
			},
			previewPubImg(i) {
				uni.previewImage({ urls: this.pubImgs, current: i });
			},
			addPubImg() {
				const left = 6 - this.pubImgs.length;
				if (left <= 0) return;
				uni.chooseImage({
					count: left,
					sizeType: ['compressed'],
					success: (res) => {
						const paths = res.tempFilePaths || [];
						if (paths.length) this.pubImgs = this.pubImgs.concat(paths).slice(0, 6);
					}
				});
			},
			removePubImg(i) { this.pubImgs.splice(i, 1); },
			async submitPost() {
				const text = this.draft.trim();
				if (!text || this.pubBusy) return;
				this.pubBusy = true;
				try {
					let images = [];
					if (this.pubImgs.length) {
						images = await uploadImages(this.pubImgs, 'posts', (i, n) => {
							uni.showLoading({ title: '上传图片 ' + (i + 1) + '/' + n, mask: true });
						});
						uni.hideLoading();
					}
					const r = await callCloud('posts', {
						action: 'publish',
						token: getToken(),
						tag: this.pubTag,
						text,
						images
					});
					if (r.post) {
						this.posts = [{ ...r.post, time: '刚刚' }].concat(this.posts);
					}
					this.showPublish = false;
					uni.showToast({ title: '发布成功', icon: 'success' });
				} catch (e) {
					uni.hideLoading();
					uni.showToast({ title: (e && e.message) || '发布失败', icon: 'none' });
				} finally {
					this.pubBusy = false;
				}
			},
			openPost(i) {
				const p = this.posts[i];
				uni.navigateTo({ url: '/pages/post-detail/post-detail?id=' + (p && p.id) });
			},
			async onLike(i) {
				const p = this.posts[i];
				if (!p) return;
				try {
					const r = await callCloud('like', { action: 'toggle', token: getToken(), postId: p.id });
					const liked = !!r.liked;
					const likes = typeof r.likes === 'number' ? r.likes : p.likes + (p.liked ? -1 : 1);
					this.posts = this.posts.map((x) => x.id === p.id ? { ...x, liked, likes } : x);
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '点赞失败', icon: 'none' });
				}
			},
			onComment(i) { this.openPost(i); },
			async onFav(i) {
				const p = this.posts[i];
				if (!p) return;
				try {
					const r = await callCloud('favorite', {
						action: 'toggle',
						token: getToken(),
						type: 'post',
						targetId: p.id,
						title: p.tag + ' · ' + p.user,
						cover: '',
						desc: p.text.slice(0, 80)
					});
					const faved = !!r.faved;
					const favs = p.favs + (faved ? 1 : -1);
					this.posts = this.posts.map((x) => x.id === p.id ? { ...x, faved, favs: Math.max(0, favs) } : x);
					uni.showToast({ title: faved ? '已收藏' : '已取消收藏', icon: 'none' });
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '收藏失败', icon: 'none' });
				}
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
	.cm__post-img--pic { width: 100%; }

	/* 发帖配图 */
	.cm__imgs { display: flex; flex-wrap: wrap; margin-top: 20rpx; }
	.cm__img {
		box-sizing: border-box; width: 132rpx; height: 132rpx;
		margin: 0 14rpx 14rpx 0; position: relative; flex-shrink: 0;
	}
	.cm__img-pic { width: 132rpx; height: 132rpx; border-radius: 16rpx; }
	.cm__img-del {
		position: absolute; top: -10rpx; right: -10rpx;
		width: 36rpx; height: 36rpx; border-radius: 50%;
		background: rgba(41, 36, 61, 0.72);
		display: flex; align-items: center; justify-content: center;
	}
	.cm__img-del-t { color: #fff; font-size: 26rpx; line-height: 1; margin-top: -2rpx; }
	.cm__img--add {
		border: 2rpx dashed rgba(123, 97, 255, 0.4); border-radius: 16rpx;
		background: rgba(123, 97, 255, 0.06);
		display: flex; flex-direction: column; align-items: center; justify-content: center;
	}
	.cm__img-add-ico { font-size: 44rpx; color: #7B61FF; line-height: 1; font-weight: 300; }
	.cm__img-add-n { margin-top: 8rpx; font-size: 20rpx; color: #AAA2BD; }

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

	.cm__empty { display: flex; justify-content: center; padding: 100rpx 0; }
	.cm__empty-t { font-size: 26rpx; color: $t-tertiary; }

	.cm__bottom-space { height: 140rpx; }

	/* ══════════ 发帖弹层 ══════════ */
	.cm__mask {
		position: fixed; left: 0; right: 0; top: 0; bottom: 0; z-index: 90;
		background: rgba(41, 36, 61, 0.45);
	}
	.cm__sheet {
		position: fixed; left: 0; right: 0; bottom: 0; z-index: 91;
		background: $c-white;
		border-radius: 36rpx 36rpx 0 0;
		padding: 32rpx 32rpx calc(32rpx + env(safe-area-inset-bottom));
	}
	.cm__sheet-head { display: flex; align-items: center; justify-content: space-between; }
	.cm__sheet-title { font-size: 32rpx; font-weight: 800; color: $c-ink; }
	.cm__sheet-close { font-size: 44rpx; color: $t-tertiary; line-height: 1; padding: 0 8rpx; }
	.cm__sheet-input {
		display: block;
		margin-top: 24rpx;
		width: 100%;
		box-sizing: border-box;
		height: 220rpx;
		background: $c-mist;
		border-radius: 20rpx;
		padding: 24rpx;
		font-size: 27rpx;
		color: $t-main;
	}
	.cm__sheet-tags { display: flex; flex-wrap: wrap; margin-top: 22rpx; }
	.cm__sheet-tag {
		padding: 10rpx 24rpx;
		border-radius: $r-pill;
		background: $c-mist;
		margin: 0 14rpx 14rpx 0;
	}
	.cm__sheet-tag--on { background: rgba(128, 92, 250, 0.14); }
	.cm__sheet-tag-t { font-size: 23rpx; color: $t-sub; font-weight: 600; }
	.cm__sheet-tag--on .cm__sheet-tag-t { color: $c-primary; }
	.cm__sheet-btn {
		margin-top: 16rpx;
		height: 88rpx;
		border-radius: $r-pill;
		background: $g-cta;
		display: flex; align-items: center; justify-content: center;
		box-shadow: 0 8rpx 16rpx rgba(255, 122, 82, 0.3);
	}
	.cm__sheet-btn--off { opacity: 0.5; }
	.cm__sheet-btn-t { font-size: 28rpx; color: $c-white; font-weight: 700; letter-spacing: 2rpx; }
</style>
