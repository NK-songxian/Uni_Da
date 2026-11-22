<template>
	<view class="fv unida-page">
		<!-- ══════════ 自绘顶栏 ══════════ -->
		<view class="fv__nav" :style="{ paddingTop: statusBar + 'px' }">
			<view class="fv__nav-btn" @click="goBack">
				<image class="fv__nav-ico" src="/static/icons-dark/back.png" mode="aspectFit" />
			</view>
			<text class="fv__nav-title">我的收藏</text>
			<view class="fv__nav-btn"></view>
		</view>

		<!-- ══════════ 类型筛选 ══════════ -->
		<view class="fv__tabs">
			<view
				v-for="(t, i) in tabs"
				:key="i"
				class="fv__tab"
				:class="{ 'fv__tab--on': active === i }"
				@click="onTab(i)"
			>
				<text class="fv__tab-t">{{ t.label }}</text>
			</view>
		</view>

		<!-- ══════════ 收藏列表 ══════════ -->
		<view class="fv__list">
			<view class="fv__card" v-for="(x, i) in listShow" :key="x.id" @click="onOpen(x)">
				<view class="fv__cover">
					<image class="fv__cover-img" v-if="x.cover && x.cover[0] === '/'" :src="x.cover" mode="aspectFill" />
					<view class="fv__cover-grad" v-else :style="{ background: x.cover || 'linear-gradient(135deg,#805CFA,#B59BFF)' }"></view>
					<view class="fv__type" :class="'fv__type--' + x.type">
						<text class="fv__type-t">{{ x.type === 'post' ? '帖子' : '活动' }}</text>
					</view>
				</view>
				<view class="fv__body">
					<text class="fv__title">{{ x.title || '未命名收藏' }}</text>
					<text class="fv__desc" v-if="x.desc">{{ x.desc }}</text>
					<view class="fv__foot">
						<text class="fv__time">{{ x.time }}</text>
						<text class="fv__remove" @click.stop="onRemove(i, x)">取消收藏</text>
					</view>
				</view>
			</view>

			<!-- ══════════ 品牌空态 ══════════ -->
			<view class="fv__empty" v-if="!loading && listShow.length === 0">
				<image class="fv__empty-img" src="/static/unida/planet/planet-bubble.png" mode="aspectFit" />
				<text class="fv__empty-t">还没有收藏</text>
				<text class="fv__empty-sub">看到喜欢的活动或帖子，点爱心收藏吧</text>
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
				active: 0,
				tabs: [
					{ label: '全部', key: '' },
					{ label: '活动', key: 'item' },
					{ label: '帖子', key: 'post' }
				],
				list: []
			};
		},
		computed: {
			listShow() {
				const key = this.tabs[this.active].key;
				return key ? this.list.filter((x) => x.type === key) : this.list;
			}
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
			onTab(i) { this.active = i; },
			async loadList() {
				if (this.loading) return;
				this.loading = true;
				try {
					const r = await callCloud('favorite', { action: 'list', token: getToken() });
					this.list = (r.list || []).map((x) => ({ ...x, time: timeAgo(x.createdAt) }));
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '获取收藏失败', icon: 'none' });
				} finally {
					this.loading = false;
				}
			},
			onOpen(x) {
				if (x.type === 'post') {
					uni.navigateTo({ url: '/pages/post-detail/post-detail?id=' + x.id });
				} else {
					uni.navigateTo({ url: '/pages/activity-detail/activity-detail?id=' + x.id });
				}
			},
			async onRemove(i, x) {
				try {
					await callCloud('favorite', {
						action: 'toggle',
						token: getToken(),
						type: x.type,
						targetId: x.id
					});
					this.list = this.list.filter((y) => y.id !== x.id);
					uni.showToast({ title: '已取消收藏', icon: 'none' });
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '操作失败', icon: 'none' });
				}
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.fv { padding-bottom: calc(60rpx + env(safe-area-inset-bottom)); }

	/* ══════════ 顶栏 ══════════ */
	.fv__nav {
		display: flex; align-items: center; justify-content: space-between;
		padding-left: $page-x; padding-right: $page-x; padding-bottom: 16rpx;
	}
	.fv__nav-btn { width: 64rpx; height: 64rpx; display: flex; align-items: center; justify-content: center; }
	.fv__nav-ico { width: 40rpx; height: 40rpx; }
	.fv__nav-title { font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink; letter-spacing: 0.5rpx; }

	/* ══════════ 筛选 ══════════ */
	.fv__tabs { display: flex; margin: 12rpx $page-x 0; }
	.fv__tab {
		padding: 12rpx 28rpx; border-radius: $r-pill; margin-right: 14rpx;
		background: #fff; box-shadow: $sh-card;
		transition: background 0.2s ease;
	}
	.fv__tab--on { background: $g-brand; }
	.fv__tab--on .fv__tab-t { color: #fff; font-weight: $fw-bold; }
	.fv__tab-t { font-size: $fs-caption; color: $t-sub; letter-spacing: 0.3rpx; }

	/* ══════════ 收藏卡 ══════════ */
	.fv__card {
		display: flex;
		margin: 24rpx $page-x 0; padding: 24rpx;
		border-radius: $r-lg; background: #fff; box-shadow: $sh-card;
	}
	.fv__cover { position: relative; width: 180rpx; height: 180rpx; border-radius: $r-md; overflow: hidden; flex-shrink: 0; }
	.fv__cover-img { width: 100%; height: 100%; }
	.fv__cover-grad { width: 100%; height: 100%; }
	.fv__type {
		position: absolute; left: 10rpx; top: 10rpx;
		padding: 4rpx 14rpx; border-radius: $r-pill;
		background: rgba(255, 255, 255, 0.85);
	}
	.fv__type--item { background: rgba(128, 92, 250, 0.85); }
	.fv__type--post { background: rgba(255, 138, 61, 0.88); }
	.fv__type-t { font-size: 20rpx; color: #fff; font-weight: $fw-semibold; }
	.fv__body { flex: 1; min-width: 0; margin-left: 22rpx; display: flex; flex-direction: column; }
	.fv__title {
		font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink;
		letter-spacing: -0.3rpx; line-height: 1.4;
		display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; overflow: hidden;
	}
	.fv__desc {
		margin-top: 10rpx; font-size: $fs-micro; color: $t-sub; line-height: 1.5;
		display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 1; overflow: hidden;
	}
	.fv__foot { display: flex; align-items: center; justify-content: space-between; margin-top: auto; }
	.fv__time { font-size: $fs-micro; color: $t-tertiary; }
	.fv__remove {
		font-size: $fs-caption; font-weight: $fw-semibold;
		color: $t-sub; background: $c-mist;
		padding: 10rpx 24rpx; border-radius: $r-pill;
	}
	.fv__remove:active { opacity: 0.8; }

	/* ══════════ 空态 ══════════ */
	.fv__empty { display: flex; flex-direction: column; align-items: center; padding: 80rpx 0 40rpx; }
	.fv__empty-img { width: 300rpx; height: 300rpx; }
	.fv__empty-t { margin-top: 12rpx; font-size: $fs-body; font-weight: $fw-semibold; color: $t-sub; letter-spacing: 0.5rpx; }
	.fv__empty-sub { margin-top: 10rpx; font-size: $fs-caption; color: $t-tertiary; letter-spacing: 0.3rpx; }
</style>
