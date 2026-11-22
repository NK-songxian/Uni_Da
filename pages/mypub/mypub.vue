<template>
	<view class="mp unida-page">
		<!-- ══════════ 自绘顶栏 ══════════ -->
		<view class="mp__nav" :style="{ paddingTop: statusBar + 'px' }">
			<view class="mp__nav-btn" @click="goBack">
				<image class="mp__nav-ico" src="/static/icons-dark/back.png" mode="aspectFit" />
			</view>
			<text class="mp__nav-title">我的发布</text>
			<view class="mp__nav-btn"></view>
		</view>

		<!-- ══════════ 统计头 ══════════ -->
		<view class="mp__hero">
			<image class="mp__hero-img" src="/static/unida/planet/planet-cal.png" mode="aspectFit" />
			<view class="mp__hero-info">
				<text class="mp__hero-title">我的发布</text>
				<view class="mp__hero-stats">
					<view class="mp__stat">
						<text class="mp__stat-n">{{ total }}</text>
						<text class="mp__stat-k">全部</text>
					</view>
					<view class="mp__stat-divider"></view>
					<view class="mp__stat">
						<text class="mp__stat-n">{{ totalLikes }}</text>
						<text class="mp__stat-k">收到赞</text>
					</view>
					<view class="mp__stat-divider"></view>
					<view class="mp__stat">
						<text class="mp__stat-n">{{ totalComments }}</text>
						<text class="mp__stat-k">收到评论</text>
					</view>
				</view>
			</view>
		</view>

		<!-- ══════════ 帖子列表 ══════════ -->
		<view class="mp__list">
			<view class="mp__card" v-for="(p, i) in list" :key="p.id" @click="onOpen(p)">
				<view class="mp__head">
					<view class="mp__tag"><text class="mp__tag-t">{{ p.tag }}</text></view>
					<text class="mp__time">{{ p.time }}</text>
				</view>
				<text class="mp__text">{{ p.text }}</text>
				<view class="mp__foot">
					<view class="mp__metric">
						<image class="mp__metric-ico" src="/static/icons-dark/heart.png" mode="aspectFit" />
						<text class="mp__metric-n">{{ p.likes }}</text>
					</view>
					<view class="mp__metric">
						<image class="mp__metric-ico" src="/static/icons-dark/message.png" mode="aspectFit" />
						<text class="mp__metric-n">{{ p.comments }}</text>
					</view>
					<view class="mp__metric">
						<image class="mp__metric-ico" src="/static/icons-dark/box.png" mode="aspectFit" />
						<text class="mp__metric-n">{{ p.favs }}</text>
					</view>
					<view class="mp__spacer"></view>
					<text class="mp__del" @click.stop="onDelete(i, p)">删除</text>
				</view>
			</view>

			<!-- ══════════ 空态 ══════════ -->
			<view class="mp__empty" v-if="!loading && list.length === 0">
				<image class="mp__empty-img" src="/static/unida/planet/planet-bubble.png" mode="aspectFit" />
				<text class="mp__empty-t">还没有发布过动态</text>
				<text class="mp__empty-sub">去社区发第一条帖子吧</text>
				<view class="mp__empty-btn" @click="goPublish"><text class="mp__empty-btn-t">去发布</text></view>
			</view>
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
				loading: false,
				list: []
			};
		},
		computed: {
			total() { return this.list.length; },
			totalLikes() { return this.list.reduce((s, x) => s + (Number(x.likes) || 0), 0); },
			totalComments() { return this.list.reduce((s, x) => s + (Number(x.comments) || 0), 0); }
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = (sys && sys.statusBarHeight) || 0;
		},
		onShow() {
			this.loadList();
		},
		methods: {
			goBack() { uni.navigateBack(); },
			goPublish() { uni.navigateTo({ url: '/pages/community/community' }); },
			async loadList() {
				if (this.loading) return;
				this.loading = true;
				try {
					const r = await callCloud('posts', { action: 'mine', token: getToken() });
					this.list = (r.list || []).map((x) => ({ ...x, time: x.time || timeAgo(x.ts) }));
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '获取发布失败', icon: 'none' });
				} finally {
					this.loading = false;
				}
			},
			onOpen(p) {
				uni.navigateTo({ url: '/pages/post-detail/post-detail?id=' + p.id });
			},
			onDelete(i, p) {
				uni.showModal({
					title: '删除动态',
					content: '删除后无法恢复，确定删除这条动态吗？',
					confirmColor: '#FF5A4E',
					success: async (res) => {
						if (!res.confirm) return;
						try {
							await callCloud('posts', { action: 'remove', token: getToken(), postId: p.id });
							this.list = this.list.filter((x) => x.id !== p.id);
							uni.showToast({ title: '已删除', icon: 'none' });
						} catch (e) {
							uni.showToast({ title: (e && e.message) || '删除失败', icon: 'none' });
						}
					}
				});
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.mp { padding-bottom: calc(60rpx + env(safe-area-inset-bottom)); }

	/* ══════════ 顶栏 ══════════ */
	.mp__nav {
		display: flex; align-items: center; justify-content: space-between;
		padding-left: $page-x; padding-right: $page-x; padding-bottom: 16rpx;
	}
	.mp__nav-btn { width: 64rpx; height: 64rpx; display: flex; align-items: center; justify-content: center; }
	.mp__nav-ico { width: 40rpx; height: 40rpx; }
	.mp__nav-title { font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink; letter-spacing: 0.5rpx; }

	/* ══════════ 统计头 ══════════ */
	.mp__hero {
		display: flex; align-items: center;
		margin: 8rpx $page-x 0; padding: 24rpx 28rpx;
		border-radius: $r-lg; background: #fff; box-shadow: $sh-card;
	}
	.mp__hero-img { width: 150rpx; height: 150rpx; flex-shrink: 0; }
	.mp__hero-info { flex: 1; margin-left: 20rpx; }
	.mp__hero-title {
		display: block;
		font-size: $fs-h2; font-weight: $fw-bold; color: $c-ink; letter-spacing: -0.8rpx;
	}
	.mp__hero-stats { display: flex; align-items: center; margin-top: 18rpx; }
	.mp__stat { display: flex; flex-direction: column; align-items: center; margin-right: 28rpx; }
	.mp__stat-n { font-family: $ff-num; font-size: $fs-h2; font-weight: $fw-bold; color: $c-primary; line-height: 1.1; }
	.mp__stat-k { margin-top: 4rpx; font-size: $fs-micro; color: $t-sub; letter-spacing: 0.3rpx; }
	.mp__stat-divider { width: 2rpx; height: 52rpx; background: $c-line; margin-right: 28rpx; }

	/* ══════════ 帖子卡 ══════════ */
	.mp__card {
		margin: 24rpx $page-x 0; padding: 26rpx 28rpx;
		border-radius: $r-lg; background: #fff; box-shadow: $sh-card;
	}
	.mp__head { display: flex; align-items: center; justify-content: space-between; }
	.mp__tag { padding: 8rpx 20rpx; border-radius: $r-pill; background: rgba(128, 92, 250, 0.10); }
	.mp__tag-t { font-size: $fs-micro; font-weight: $fw-semibold; color: $c-primary; }
	.mp__time { font-size: $fs-micro; color: $t-tertiary; }
	.mp__text {
		display: block; margin-top: 16rpx;
		font-size: $fs-body; color: $t-main; line-height: 1.6;
		display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3; overflow: hidden;
	}
	.mp__foot {
		display: flex; align-items: center;
		margin-top: 20rpx; padding-top: 18rpx; border-top: 2rpx solid $c-line;
	}
	.mp__metric { display: flex; align-items: center; margin-right: 30rpx; }
	.mp__metric-ico { width: 30rpx; height: 30rpx; opacity: 0.5; }
	.mp__metric-n { margin-left: 8rpx; font-size: $fs-caption; color: $t-sub; font-family: $ff-num; }
	.mp__spacer { flex: 1; }
	.mp__del {
		font-size: $fs-caption; font-weight: $fw-semibold;
		color: #E86154; background: rgba(232, 97, 84, 0.10);
		padding: 10rpx 24rpx; border-radius: $r-pill;
	}
	.mp__del:active { opacity: 0.8; }

	/* ══════════ 空态 ══════════ */
	.mp__empty { display: flex; flex-direction: column; align-items: center; padding: 80rpx 0 40rpx; }
	.mp__empty-img { width: 300rpx; height: 300rpx; }
	.mp__empty-t { margin-top: 12rpx; font-size: $fs-body; font-weight: $fw-semibold; color: $t-sub; letter-spacing: 0.5rpx; }
	.mp__empty-sub { margin-top: 10rpx; font-size: $fs-caption; color: $t-tertiary; letter-spacing: 0.3rpx; }
	.mp__empty-btn {
		margin-top: 30rpx;
		padding: 18rpx 60rpx;
		border-radius: $r-pill;
		background: $g-cta;
		box-shadow: 0 8rpx 18rpx rgba(123, 97, 255, 0.22);
	}
	.mp__empty-btn-t { font-size: $fs-body; font-weight: $fw-bold; color: #fff; letter-spacing: 1rpx; }
</style>
