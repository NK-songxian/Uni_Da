<template>
	<view class="discover unida-page unida-page--tab">

		<!-- ══════════ 顶部品牌头 ══════════ -->
		<view class="hd" :style="{ paddingTop: statusBar + 'px' }">
			<view class="hd__bar">
				<view class="hd__title">
					<text class="hd__title-main">发现</text>
					<text class="hd__title-sub">找到现在就能一起的人</text>
				</view>
				<view class="hd__search" @click="onSearch">
					<image class="hd__search-ico" src="/static/icons-dark/search.png" mode="aspectFit" />
					<text class="hd__search-ph">搜索搭子、活动</text>
				</view>
			</view>
		</view>

		<view v-if="loading" class="sk">
			<view class="sk__chips"><view class="sk__chip" v-for="i in 5" :key="i"></view></view>
			<view class="sk__grid">
				<view class="sk__card" v-for="i in 4" :key="i"></view>
			</view>
		</view>

		<template v-else>

			<!-- ══════════ 三大主类 tab ══════════ -->
			<view class="maintabs">
				<view
					class="maintabs__item"
					v-for="(t, i) in mainTabs"
					:key="i"
					:class="{ 'maintabs__item--on': mainTab === i }"
					@click="onMainTab(i)"
				>
					<image class="maintabs__ico" :src="t.icon" mode="aspectFit" />
					<text class="maintabs__label">{{ t.label }}</text>
				</view>
			</view>

			<!-- ══════════ 筛选 chip ══════════ -->
			<scroll-view scroll-x class="chips" :show-scrollbar="false">
				<view class="chips__inner">
					<view
						class="chips__item"
						v-for="(c, i) in chips"
						:key="i"
						:class="{ 'chips__item--on': activeChip === i }"
						@click="onChip(i)"
					>{{ c }}</view>
				</view>
			</scroll-view>

			<!-- ══════════ 双列瀑布流 ══════════ -->
			<view class="grid">
				<view class="card" v-for="(item, i) in feedList" :key="item.id" @click="onCardTap(item)">
					<view class="card__cover">
						<image class="card__img" :src="item.cover" mode="aspectFill" />
						<view class="card__flag" v-if="item.hot">热门</view>
						<view class="card__slot">{{ item.time }}</view>
						<view class="card__ring" :style="{ borderColor: item.bar }">
							<text class="card__ring-t" :style="{ color: item.bar }">缺{{ item.total - item.joined }}</text>
						</view>
					</view>
					<view class="card__body">
						<view class="card__cate" :style="{ color: item.bar, background: item.barSoft }">{{ item.category }}</view>
						<text class="card__title">{{ item.title }}</text>
						<view class="card__meta">
							<image class="card__meta-ico" src="/static/icons-dark/pin.png" mode="aspectFit" />
							<text class="card__meta-t">{{ item.place }}</text>
						</view>
						<view class="card__foot">
							<view class="card__avatars">
								<view
									class="card__av"
									v-for="(av, k) in item.members"
									:key="k"
									:style="{ background: av.bg }"
								>{{ av.ch }}</view>
								<text class="card__joined">{{ item.joined }}/{{ item.total }}</text>
							</view>
							<text class="card__price" :style="{ color: item.price === '免费' ? '#29CA83' : item.bar }">{{ item.price }}</text>
						</view>
					</view>
				</view>
			</view>

			<!-- 上拉底部状态 -->
			<view class="foot">
				<view v-if="loadingMore" class="foot__loading">
					<view class="spin"></view>
					<text class="foot__t">正在加载更多</text>
				</view>
				<view v-else-if="feedError" class="foot__retry" @click="loadFeed(false)">
					<text class="foot__retry-t">加载失败，点击重试</text>
				</view>
				<view v-else-if="!hasMore && feedList.length" class="foot__end">
					<view class="foot__line"></view>
					<text class="foot__t">没有更多了</text>
					<view class="foot__line"></view>
				</view>
			</view>

		</template>

		<unida-tabbar :selected="1" :unread-count="3" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';
	import { fetchDiscover, DISCOVER_FILTERS } from '@/common/api/discover.js';

	export default {
		components: { unidaTabbar },
		data() {
			return {
				statusBar: 0,
				loading: true,
				loadingMore: false,
				feedError: false,
				hasMore: true,
				page: 1,
				reqId: 0,
				mainTabs: [
					{ label: '找搭子', icon: '/static/unida/illustrations/icon-run.png', key: 'buddy' },
					{ label: '校园活动', icon: '/static/unida/illustrations/icon-horn.png', key: 'activity' },
					{ label: '社团招新', icon: '/static/unida/illustrations/icon-team.png', key: 'club' }
				],
				mainTab: 0,
				chips: DISCOVER_FILTERS,
				activeChip: 0,
				feedList: []
			};
		},
		onLoad() {
			try {
				const info = uni.getSystemInfoSync();
				this.statusBar = info.statusBarHeight || 0;
			} catch (e) {
				this.statusBar = 20;
			}
			this.loadFeed(true);
		},
		onPullDownRefresh() {
			this.loadFeed(true);
		},
		onReachBottom() {
			this.loadFeed(false);
		},
		methods: {
			async loadFeed(reset) {
				if (!reset && (this.loadingMore || this.loading || !this.hasMore)) return;
				const reqId = ++this.reqId;
				if (reset) {
					this.loading = true;
				} else {
					this.loadingMore = true;
				}
				this.feedError = false;
				try {
					const res = await fetchDiscover({
						tab: this.mainTab,
						filter: this.activeChip,
						page: reset ? 1 : this.page + 1,
						size: 6
					});
					if (reqId !== this.reqId) return;
					this.feedList = reset ? res.list : this.feedList.concat(res.list);
					this.hasMore = res.hasMore;
					this.page = reset ? 1 : this.page + 1;
				} catch (e) {
					if (reqId === this.reqId) this.feedError = true;
				} finally {
					if (reqId === this.reqId) {
						this.loading = false;
						this.loadingMore = false;
					}
					uni.stopPullDownRefresh();
				}
			},
			onMainTab(i) {
				if (i === this.mainTab) return;
				this.mainTab = i;
				this.loadFeed(true);
			},
			onChip(i) {
				if (i === this.activeChip) return;
				this.activeChip = i;
				this.loadFeed(true);
			},
			onSearch() {
				uni.showToast({ title: '搜索页待开发', icon: 'none' });
			},
			onCardTap(item) {
				uni.navigateTo({ url: '/pages/activity-detail/activity-detail?id=' + item.id });
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	/* ══════════ 顶部 ══════════ */
	.hd {
		position: sticky;
		top: 0;
		z-index: 60;
		background: $c-mist;
	}
	.hd__bar {
		padding: 8rpx $page-x 16rpx;
	}
	.hd__title-main {
		display: block;
		font-size: $fs-display;
		font-weight: $fw-bold;
		color: $c-ink;
		letter-spacing: -1.2rpx;
		line-height: 1.1;
	}
	.hd__title-sub {
		display: block;
		margin-top: 4rpx;
		font-size: $fs-caption;
		color: $t-sub;
	}
	.hd__search {
		margin-top: 20rpx;
		height: 72rpx;
		padding: 0 24rpx;
		border-radius: $r-pill;
		background: #fff;
		box-shadow: $sh-card;
		display: flex;
		align-items: center;
	}
	.hd__search-ico { width: 30rpx; height: 30rpx; opacity: 0.55; }
	.hd__search-ph { margin-left: 14rpx; font-size: $fs-body; color: $t-tertiary; }

	/* ══════════ 三大主类 ══════════ */
	.maintabs {
		display: flex;
		margin: 8rpx $page-x 0;
		padding: 14rpx 10rpx;
		border-radius: $r-lg;
		background: $g-glass;
		border: 2rpx solid rgba(255, 255, 255, 0.9);
		box-shadow: $sh-card, inset 0 2rpx 0 rgba(255, 255, 255, 0.95);
	}
	.maintabs__item {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 12rpx 0;
		border-radius: $r-md;
	}
	.maintabs__item--on {
		background: $g-brand;
		box-shadow: 0 8rpx 20rpx rgba(128, 92, 250, 0.26);
	}
	.maintabs__ico { width: 60rpx; height: 60rpx; }
	.maintabs__label {
		margin-top: 8rpx;
		font-size: $fs-caption;
		font-weight: $fw-semibold;
		color: $t-main;
	}
	.maintabs__item--on .maintabs__label { color: #fff; }

	/* ══════════ 筛选 chip ══════════ */
	.chips { width: 100%; white-space: nowrap; margin-top: 24rpx; }
	.chips__inner { display: inline-block; padding: 0 $page-x; }
	.chips__item {
		display: inline-block;
		height: 56rpx;
		padding: 0 26rpx;
		margin-right: 14rpx;
		border-radius: $r-pill;
		background: rgba(255, 255, 255, 0.82);
		color: $t-sub;
		font-size: $fs-caption;
		line-height: 56rpx;
	}
	.chips__item--on {
		background: $g-cta;
		color: #fff;
		font-weight: $fw-semibold;
		box-shadow: 0 8rpx 18rpx rgba(128, 92, 250, 0.24);
	}

	/* ══════════ 双列瀑布流 ══════════ */
	.grid {
		display: flex;
		flex-wrap: wrap;
		padding: 20rpx $page-x 0;
	}
	.card {
		width: calc(50% - 11rpx);
		margin-bottom: 22rpx;
		border-radius: $r-md;
		background: #fff;
		box-shadow: 0 8rpx 22rpx rgba(123, 97, 255, 0.10);
		overflow: hidden;
	}
	.card:nth-child(odd) { margin-right: 22rpx; }
	.card__cover {
		position: relative;
		width: 100%;
		height: 220rpx;
	}
	.card__img { width: 100%; height: 100%; display: block; }
	.card__flag {
		position: absolute;
		left: 12rpx;
		top: 12rpx;
		height: 34rpx;
		padding: 0 12rpx;
		border-radius: $r-pill;
		background: $g-cta;
		color: #fff;
		font-size: 19rpx;
		font-weight: $fw-semibold;
		line-height: 34rpx;
		box-shadow: 0 4rpx 12rpx rgba(128, 92, 250, 0.3);
	}
	.card__slot {
		position: absolute;
		left: 12rpx;
		bottom: 12rpx;
		height: 34rpx;
		padding: 0 12rpx;
		border-radius: $r-pill;
		background: rgba(42, 36, 64, 0.55);
		color: #fff;
		font-size: 19rpx;
		line-height: 34rpx;
	}
	.card__ring {
		position: absolute;
		right: 12rpx;
		bottom: 12rpx;
		width: 76rpx;
		height: 76rpx;
		border-radius: 50%;
		border: 5rpx solid $c-primary;
		background: rgba(255, 255, 255, 0.94);
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 0 4rpx 12rpx rgba(42, 36, 64, 0.2);
	}
	.card__ring-t {
		font-size: 20rpx;
		font-weight: $fw-bold;
	}
	.card__body { padding: 16rpx 18rpx 18rpx; }
	.card__cate {
		display: inline-block;
		height: 32rpx;
		padding: 0 12rpx;
		border-radius: 8rpx;
		font-size: 19rpx;
		font-weight: $fw-medium;
		line-height: 32rpx;
	}
	.card__title {
		display: block;
		margin-top: 10rpx;
		font-size: 28rpx;
		font-weight: $fw-semibold;
		color: $t-main;
		line-height: 1.4;
		min-height: 78rpx;
	}
	.card__meta {
		display: flex;
		align-items: center;
		margin-top: 8rpx;
	}
	.card__meta-ico { width: 22rpx; height: 22rpx; opacity: 0.7; }
	.card__meta-t { margin-left: 4rpx; font-size: 20rpx; color: $t-sub; }
	.card__foot {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-top: 14rpx;
		padding-top: 14rpx;
		border-top: 2rpx solid $c-line;
	}
	.card__avatars { display: flex; align-items: center; }
	.card__av {
		width: 36rpx;
		height: 36rpx;
		border-radius: 50%;
		border: 2rpx solid #fff;
		color: #fff;
		font-size: 17rpx;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.card__av + .card__av { margin-left: -10rpx; }
	.card__joined {
		margin-left: 8rpx;
		font-family: $ff-num;
		font-size: 19rpx;
		font-weight: $fw-bold;
		color: $c-primary;
	}
	.card__price { font-size: 22rpx; font-weight: $fw-bold; }

	/* ══════════ 底部状态 ══════════ */
	.foot { padding: 8rpx $page-x 20rpx; }
	.foot__loading { display: flex; align-items: center; justify-content: center; padding: 26rpx 0; }
	.foot__t { margin-left: 12rpx; font-size: $fs-caption; color: $t-tertiary; }
	.foot__retry { display: flex; justify-content: center; padding: 24rpx 0; }
	.foot__retry-t {
		height: 60rpx;
		padding: 0 28rpx;
		border-radius: $r-pill;
		background: rgba(128, 92, 250, 0.08);
		color: $c-primary;
		font-size: $fs-caption;
		line-height: 60rpx;
	}
	.foot__end { display: flex; align-items: center; justify-content: center; padding: 30rpx 0 10rpx; }
	.foot__line { width: 56rpx; height: 2rpx; background: $c-line; }
	.foot__end .foot__t { margin: 0 16rpx; }
	.spin {
		width: 28rpx; height: 28rpx; border-radius: 50%;
		border: 4rpx solid rgba(128, 92, 250, 0.18);
		border-top-color: $c-primary;
		animation: spinRotate 700ms linear infinite;
	}
	@keyframes spinRotate { to { transform: rotate(360deg); } }

	/* ══════════ 骨架屏 ══════════ */
	.sk { padding: 24rpx $page-x 0; }
	.sk__chips { display: flex; }
	.sk__chip {
		width: 120rpx; height: 56rpx; margin-right: 14rpx;
		border-radius: $r-pill; background: #ECE5FA;
		animation: skBreath 1.4s ease-in-out infinite;
	}
	.sk__grid { display: flex; flex-wrap: wrap; margin-top: 24rpx; }
	.sk__card {
		width: calc(50% - 11rpx); height: 440rpx; margin-bottom: 22rpx;
		border-radius: $r-md; background: #ECE5FA;
		animation: skBreath 1.4s ease-in-out infinite;
	}
	.sk__card:nth-child(odd) { margin-right: 22rpx; }
	@keyframes skBreath { 0%, 100% { opacity: 1; } 50% { opacity: 0.55; } }
</style>
