<template>
	<view class="home unida-page unida-page--tab">

		<!-- ══════════ 1 · 顶部品牌栏（吸顶，滚动渐白） ══════════ -->
		<view class="hd" :class="{ 'hd--solid': scrolled }" :style="{ paddingTop: statusBar + 'px' }">
			<view class="hd__bar">
				<view class="hd__school" @click="onSwitchSchool">
					<image class="hd__ico" src="/static/icons-dark/pin.png" mode="aspectFit" />
					<text class="hd__name">{{ school }}</text>
					<image class="hd__chev" src="/static/icons-dark/chevron.png" mode="aspectFit" />
				</view>
				<image class="hd__logo" src="/static/unida/brand/logo-topbar.png" mode="heightFix" />
				<view class="hd__bell" @click="onNotice">
					<image class="hd__ico" src="/static/icons-dark/bell.png" mode="aspectFit" />
					<view class="hd__dot"></view>
				</view>
			</view>
		</view>

		<!-- ══════════ 骨架屏（首屏加载） ══════════ -->
		<view v-if="loading" class="sk">
			<view class="sk__hero"></view>
			<view class="sk__cats">
				<view class="sk__cat" v-for="i in 6" :key="i"></view>
			</view>
			<view class="sk__promo"></view>
			<view class="sk__line sk__line--t"></view>
			<view class="sk__rail">
				<view class="sk__card" v-for="i in 2" :key="i"></view>
			</view>
			<view class="sk__line sk__line--t"></view>
			<view class="sk__feed" v-for="i in 2" :key="i"></view>
		</view>

		<!-- 首屏异常态 -->
		<view v-else-if="error" class="err">
			<image class="err__img" src="/static/unida/mascot/u-planet.png" mode="aspectFit" />
			<text class="err__t">网络走丢了</text>
			<text class="err__d">检查一下网络，我们重试一次</text>
			<view class="err__btn" @click="loadOverview(true)">重新加载</view>
		</view>

		<template v-else>

			<!-- ══════════ 2 · Hero 融合 Banner（品牌主视觉 + 高积分任务同屏轮播） ══════════ -->
			<view class="hero">
				<swiper
					class="hero__swiper"
					:indicator-dots="false"
					:autoplay="true"
					:interval="5000"
					:duration="600"
					:circular="true"
					@change="onHeroChange"
				>
					<!-- 第 1 屏 · 品牌主视觉 -->
					<swiper-item>
						<view class="hero__slide hero__slide--brand">
							<image class="hero__sky" src="/static/unida/backgrounds/bg-campus-sky.jpg" mode="aspectFill" />
							<view class="hero__tint"></view>
							<view class="hero__spark hero__spark--1"></view>
							<view class="hero__spark hero__spark--2"></view>
							<view class="hero__spark hero__spark--3"></view>
							<view class="hero__copy">
								<view class="hero__pill">
									<view class="hero__live"></view>
									<text class="hero__pill-txt">今天 <text class="hero__num">{{ todayJoin }}</text> 位同学找到了搭子</text>
								</view>
								<text class="hero__title">在校园，</text>
								<text class="hero__title hero__title--2">找到和你同频的人</text>
								<view class="hero__search" @click="onSearch">
									<image class="hero__search-ico" src="/static/icons-dark/search.png" mode="aspectFit" />
									<text class="hero__search-ph">搜活动、搭子、社团</text>
								</view>
							</view>
							<image class="hero__trio" src="/static/unida/characters/trio-back.webp" mode="widthFix" />
							<image class="hero__planet" src="/static/unida/mascot/u-planet.png" mode="aspectFit" />
							<view class="hero__fade"></view>
						</view>
					</swiper-item>

					<!-- 后续屏 · 校园精选任务大卡 -->
					<swiper-item v-for="(p, i) in promos" :key="p.id">
						<view class="hero__slide hero__slide--task" :style="{ background: p.bg }" @click="onPromoTap(p)">
							<view class="task__tag" :style="{ background: p.tagBg }">{{ p.tag }}</view>
							<view class="task__body">
								<text class="task__eyebrow">校园精选 · 高积分任务</text>
								<text class="task__title">{{ p.title }}</text>
								<text class="task__desc">{{ p.desc }}</text>
								<view class="task__cta">
									<text class="task__cta-t">去完成</text>
									<image class="task__cta-ico" src="/static/icons-dark/chevron.png" mode="aspectFit" />
								</view>
							</view>
							<view class="task__point">
								<text class="task__point-num">{{ p.point }}</text>
								<text class="task__point-unit">积分</text>
							</view>
							<image class="task__art" src="/static/unida/characters/trio-back.webp" mode="widthFix" />
							<view class="task__halo"></view>
						</view>
					</swiper-item>
				</swiper>

				<!-- 统一指示器：1 品牌 + N 任务 -->
				<view class="hero__dots">
					<view class="hero__dot" :class="{ 'hero__dot--on': heroCur === 0 }"></view>
					<view
						class="hero__dot"
						v-for="(p, i) in promos"
						:key="i"
						:class="{ 'hero__dot--on': heroCur === i + 1 }"
					></view>
				</view>
			</view>

			<!-- ══════════ 3 · 六大入口（3D 图标 + 彩色 squircle 底） ══════════ -->
			<view class="cats">
				<view class="cats__item" v-for="(c, i) in cats" :key="i" @click="onCategory(c)">
					<view class="cats__fig" :style="{ background: c.tint }">
						<image class="cats__img" :src="c.icon" mode="aspectFit" />
					</view>
				<text class="cats__label">{{ c.label }}</text>
			</view>
		</view>

		<!-- ══════════ 4 · 现在可以搭（核心差异化 · 榜单出血卡） ══════════ -->
		<view class="sec">
				<view class="sec__hd">
					<view class="sec__hd-l">
						<text class="sec__title">现在可以搭</text>
						<text class="sec__sub">2 小时内 · 还缺人</text>
					</view>
					<text class="sec__more" @click="goDiscover">全部</text>
				</view>

				<scroll-view v-if="nowList.length" scroll-x class="rail" :show-scrollbar="false">
					<view class="rail__inner">
						<view class="now" v-for="(n, i) in nowList" :key="i" @click="onCardTap(n)">
							<view class="now__cover">
								<image class="now__img" :src="n.cover" mode="aspectFill" />
								<view class="now__rank">{{ i + 1 }}</view>
								<view class="now__clock">{{ n.left }}</view>
							</view>
							<view class="now__body">
								<text class="now__title">{{ n.title }}</text>
								<view class="now__meta">
									<image class="now__ico" src="/static/icons-dark/clock.png" mode="aspectFit" />
									<text class="now__meta-txt">{{ n.time }}</text>
									<view class="now__sep"></view>
									<image class="now__ico" src="/static/icons-dark/pin.png" mode="aspectFit" />
									<text class="now__meta-txt">{{ n.place }}</text>
								</view>
								<view class="now__foot">
									<view class="now__people">
										<view
											class="now__av"
											v-for="(av, k) in n.members"
											:key="k"
											:style="{ background: av.bg }"
										>{{ av.ch }}</view>
										<text class="now__count">{{ n.joined }}/{{ n.total }}</text>
									</view>
									<view class="now__join" @click.stop="onJoin(n)">加入</view>
								</view>
							</view>
						</view>
					</view>
				</scroll-view>

				<!-- 空态 -->
				<view v-else class="empty">
					<image class="empty__img" src="/static/unida/mascot/u-planet.png" mode="aspectFit" />
					<text class="empty__t">这个时段还没人组局</text>
					<text class="empty__d">发一个，看看谁和你同频</text>
					<view class="empty__btn" @click="goPublish">发起组局</view>
				</view>
			</view>

			<!-- ══════════ 5 · 同校动态 ══════════ -->
			<view class="sec">
				<view class="sec__hd">
					<view class="sec__hd-l">
						<text class="sec__title">同校动态</text>
					</view>
					<text class="sec__more" @click="goCommunity">进广场</text>
				</view>

				<scroll-view scroll-x class="tabs" :show-scrollbar="false">
					<view class="tabs__inner">
						<view
							class="tabs__item"
							:class="{ 'tabs__item--on': feedTab === i }"
							v-for="(t, i) in feedTabs"
							:key="i"
							@click="feedTab = i"
						>{{ t }}</view>
					</view>
				</scroll-view>

				<view v-if="feedLoading" class="feed-load">
					<view class="spin"></view>
					<text class="feed-load__t">加载中</text>
				</view>

				<view class="feed" v-for="(f, i) in feedList" :key="f.id" @click="onCardTap(f)">
					<view class="feed__head">
						<view class="feed__av" :style="{ background: f.bg }">{{ f.ch }}</view>
						<view class="feed__who">
							<view class="feed__row">
								<text class="feed__name">{{ f.user }}</text>
								<view class="feed__id" :style="{ color: f.bar, background: f.barSoft }">{{ f.cat }}</view>
							</view>
							<text class="feed__meta">{{ f.college }} · {{ f.time }}</text>
						</view>
						<view class="feed__more">···</view>
					</view>
					<view class="feed__main">
						<view class="feed__left">
							<text class="feed__text">{{ f.text }}</text>
							<view class="feed__topics">
								<text class="feed__topic">#{{ f.topic }}</text>
								<text class="feed__topic feed__topic--soft">#校园搭子</text>
							</view>
						</view>
						<image class="feed__thumb" :src="f.cover" mode="aspectFill" />
					</view>
					<view class="feed__acts">
						<view class="feed__act">
							<image class="feed__act-ico" src="/static/icons-dark/heart.png" mode="aspectFit" />
							<text class="feed__act-n">{{ f.like }}</text>
						</view>
						<view class="feed__act">
							<image class="feed__act-ico" src="/static/icons-dark/message.png" mode="aspectFit" />
							<text class="feed__act-n">{{ f.cmt }}</text>
						</view>
						<view class="feed__join" :style="{ color: f.bar, borderColor: f.bar }" @click.stop="onJoin(f)">加入搭子 ›</view>
					</view>
				</view>

				<view class="foot">
					<view v-if="feedLoadingMore" class="foot__loading">
						<view class="spin"></view>
						<text class="foot__t">正在加载更多</text>
					</view>
					<view v-else-if="feedError" class="foot__retry" @click="loadFeed(false)">
						<text class="foot__retry-t">加载失败，点击重试</text>
					</view>
					<view v-else-if="!feedHasMore && feedList.length" class="foot__end">
						<view class="foot__line"></view>
						<text class="foot__t">没有更多了</text>
						<view class="foot__line"></view>
					</view>
					<view v-else-if="!feedList.length && !feedLoading" class="foot__empty">
						<image class="foot__empty-img" src="/static/unida/illustrations/deco-chat.png" mode="aspectFit" />
						<text class="foot__t">这个分类还没有动态</text>
					</view>
				</view>
			</view>

			<!-- ══════════ 6 · 校园活动（横滑大卡） ══════════ -->
			<view class="sec">
				<view class="sec__hd">
					<view class="sec__hd-l">
						<text class="sec__title">校园活动</text>
						<text class="sec__sub">官方 · 社团</text>
					</view>
					<text class="sec__more" @click="goDiscover">更多</text>
				</view>

				<scroll-view scroll-x class="rail" :show-scrollbar="false">
					<view class="rail__inner">
						<view class="act" v-for="(a, i) in acts" :key="i" @click="onCardTap(a)">
							<image class="act__img" :src="a.cover" mode="aspectFill" />
							<view class="act__mask"></view>
							<view class="act__flag" :class="'act__flag--' + a.tone">{{ a.flag }}</view>
							<view class="act__info">
								<text class="act__title">{{ a.title }}</text>
								<view class="act__meta">
									<text class="act__meta-txt">{{ a.time }}</text>
									<view class="act__dot"></view>
									<text class="act__meta-txt">{{ a.place }}</text>
								</view>
								<view class="act__foot">
									<text class="act__host">{{ a.host }}</text>
									<text class="act__join">{{ a.joined }} 人已报名</text>
								</view>
							</view>
						</view>
					</view>
				</scroll-view>
			</view>

			<!-- ══════════ 7 · 同频推荐 ══════════ -->
			<view class="sec">
				<view class="sec__hd">
					<view class="sec__hd-l">
						<text class="sec__title">和你同频</text>
						<text class="sec__sub">兴趣重合度排序</text>
					</view>
					<text class="sec__more" @click="goDiscover">换一批</text>
				</view>

				<scroll-view scroll-x class="rail" :show-scrollbar="false">
					<view class="rail__inner">
						<view class="mate" v-for="(m, i) in mates" :key="i" @click="onCardTap(m)">
							<view class="mate__av" :style="{ background: m.bg }">
								<text class="mate__ch">{{ m.ch }}</text>
								<view class="mate__on" v-if="m.online"></view>
							</view>
							<text class="mate__name">{{ m.name }}</text>
							<text class="mate__college">{{ m.college }}</text>
							<view class="mate__tags">
								<text class="mate__tag" v-for="(t, k) in m.tags" :key="k">{{ t }}</text>
							</view>
							<view class="mate__hi">打招呼</view>
						</view>
					</view>
				</scroll-view>
			</view>

			<!-- ══════════ 8 · 结尾互动（U 星球 CTA） ══════════ -->
			<view class="end">
				<image class="end__planet" src="/static/unida/mascot/u-planet.png" mode="aspectFit" />
				<text class="end__t">UNIDA 想更认识你</text>
				<text class="end__d">补完兴趣标签，推荐会准很多</text>
				<view class="end__btn" @click="goMine">完善我的兴趣</view>
			</view>

		</template>

		<unida-tabbar :selected="0" :unread-count="3" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';
	import { fetchOverview, fetchFeed } from '@/common/api/home.js';

	const PAGE_SIZE = 3;

	export default {
		components: { unidaTabbar },
		data() {
			return {
				statusBar: 0,
				scrolled: false,

				// 首屏
				loading: true,
				error: '',

				// 概览数据
				school: '',
				todayJoin: '',
				cats: [],
				nowList: [],
				acts: [],
				mates: [],

				// 校园任务轮播（已融合进 Hero，heroCur 0=品牌屏，1..N=任务屏）
				promos: [],
				heroCur: 0,

				// 同校动态（分页）
				feedTabs: ['全部', '找搭子', '求助', '出闲置'],
				feedTab: 0,
				feedList: [],
				feedPage: 1,
				feedHasMore: true,
				feedLoading: false,     // 切 tab 时的轻量加载
				feedLoadingMore: false, // 上拉加载更多
				feedError: false,
				feedReqId: 0            // 防竞态：只认最后一次请求的结果
			};
		},
		onLoad() {
			// 灵动岛 / 状态栏：拿真实高度，避免 logo 被挡
			try {
				const info = uni.getSystemInfoSync();
				this.statusBar = info.statusBarHeight || 0;
			} catch (e) {
				this.statusBar = 20;
			}
			this.loadOverview();
		},
		onPageScroll(e) {
			const s = e.scrollTop > 30;
			if (s !== this.scrolled) this.scrolled = s;
		},
		// 下拉刷新
		onPullDownRefresh() {
			this.refresh();
		},
		// 上拉加载更多
		onReachBottom() {
			this.loadFeed(false);
		},
		watch: {
			feedTab() {
				this.feedPage = 1;
				this.feedHasMore = true;
				this.feedList = [];
				this.loadFeed(true);
			}
		},
		methods: {
			/* ═════════ 数据 ═════════ */

			async loadOverview(isRetry) {
				if (!isRetry) this.loading = true;
				this.error = '';
				try {
					const d = await fetchOverview();
					this.applyOverview(d);
					this.loading = false;
					this.feedPage = 1;
					this.feedHasMore = true;
					this.loadFeed(true);
				} catch (e) {
					this.loading = false;
					this.error = 'NETWORK';
				}
			},

			applyOverview(d) {
				this.school = d.school;
				this.todayJoin = d.todayJoin;
				this.cats = d.cats;
				this.nowList = d.nowList;
				this.acts = d.acts;
				this.mates = d.mates;
				this.promos = d.promos || [];
			},

			/**
			 * @param {boolean} reset true = 从第 1 页重新取（切 tab / 刷新）
			 *                        false = 追加下一页（上拉）
			 */
			async loadFeed(reset) {
				if (!reset && (this.feedLoadingMore || this.feedLoading || !this.feedHasMore)) return;

				const reqId = ++this.feedReqId;
				if (reset) {
					this.feedLoading = true;
				} else {
					this.feedLoadingMore = true;
				}
				this.feedError = false;

				try {
					const res = await fetchFeed({
						tab: this.feedTab,
						page: reset ? 1 : this.feedPage + 1,
						size: PAGE_SIZE
					});
					if (reqId !== this.feedReqId) return; // 有更新的请求了，丢弃这次结果
					this.feedList = reset ? res.list : this.feedList.concat(res.list);
					this.feedHasMore = res.hasMore;
					this.feedPage = reset ? 1 : this.feedPage + 1;
				} catch (e) {
					if (reqId === this.feedReqId) this.feedError = true;
				} finally {
					if (reqId === this.feedReqId) {
						this.feedLoading = false;
						this.feedLoadingMore = false;
					}
				}
			},

			async refresh() {
				try {
					const d = await fetchOverview();
					this.applyOverview(d);
					this.error = '';
					// 让在途请求全部失效，再重新拉第一页
					this.feedReqId++;
					this.feedLoading = false;
					this.feedLoadingMore = false;
					this.feedError = false;
					this.feedPage = 1;
					this.feedHasMore = true;
					await this.loadFeed(true);
				} catch (e) {
					uni.showToast({ title: '刷新失败，请稍后再试', icon: 'none' });
				} finally {
					uni.stopPullDownRefresh();
				}
			},

			/* ═════════ 交互 ═════════ */

			onHeroChange(e) {
				this.heroCur = e.detail.current;
			},
			onPromoTap(p) {
				// 兼容三种入参：小程序 event（dataset）/ Vue 字符串 id / Vue 对象
				let id = p;
				if (p && p.currentTarget) id = p.currentTarget.dataset.id;
				else if (p && typeof p === 'object' && p.id) id = p.id;
				uni.navigateTo({ url: '/pages/activity-detail/activity-detail?id=' + id });
			},
			onSwitchSchool() {
				uni.showToast({ title: '切换学校待开发', icon: 'none' });
			},
			onNotice() {
				uni.reLaunch({ url: '/pages/message/message' });
			},
			onSearch() {
				uni.showToast({ title: '搜索页待开发', icon: 'none' });
			},
			onCategory(c) {
				uni.showToast({ title: c.label, icon: 'none' });
			},
			onCardTap(item) {
				uni.navigateTo({ url: '/pages/activity-detail/activity-detail' });
			},
			onJoin(item) {
				uni.showToast({ title: '已提交加入申请', icon: 'none' });
			},
			goDiscover() {
				uni.reLaunch({ url: '/pages/discover/discover' });
			},
			goCommunity() {
				uni.reLaunch({ url: '/pages/community/community' });
			},
			goPublish() {
				uni.reLaunch({ url: '/pages/publish/publish' });
			},
			goMine() {
				uni.reLaunch({ url: '/pages/mine/mine' });
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	/* ══════════ 1 顶部品牌栏 ══════════ */
	.hd {
		position: sticky;
		top: 0;
		z-index: 60;
		background: transparent;
		transition: background 240ms $ease-out, box-shadow 240ms $ease-out;
	}
	.hd--solid {
		background: rgba(255, 255, 255, 0.96);
		box-shadow: 0 2rpx 16rpx rgba(123, 97, 255, 0.08);
	}
	.hd__bar {
		height: 96rpx;
		padding: 0 $page-x;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	.hd__school {
		display: flex;
		align-items: center;
		height: 60rpx;
	}
	.hd__ico { width: 30rpx; height: 30rpx; }
	.hd__name {
		margin-left: 8rpx;
		font-size: 30rpx;
		font-weight: $fw-bold;
		color: $t-main;
		letter-spacing: -0.3rpx;
	}
	.hd__chev {
		width: 22rpx;
		height: 22rpx;
		margin-left: 6rpx;
		transform: rotate(90deg);
		opacity: 0.6;
	}
	.hd__logo { height: 44rpx; }
	.hd__bell {
		position: relative;
		width: 60rpx;
		height: 60rpx;
		border-radius: $r-sm;
		background: rgba(255, 255, 255, 0.86);
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 0 4rpx 14rpx rgba(123, 97, 255, 0.10);
	}
	.hd__dot {
		position: absolute;
		top: 11rpx;
		right: 12rpx;
		width: 13rpx;
		height: 13rpx;
		border-radius: 50%;
		background: $c-danger;
		border: 2rpx solid #fff;
	}

	/* ══════════ 2 Hero 融合 Banner ══════════ */
	.hero {
		position: relative;
		margin: 8rpx $page-x 0;
		height: 520rpx;
		border-radius: $r-lg;
		overflow: hidden;
		box-shadow: 0 16rpx 40rpx rgba(84, 45, 175, 0.22);
	}
	.hero__swiper { width: 100%; height: 100%; }
	.hero__slide {
		position: relative;
		width: 100%;
		height: 100%;
		overflow: hidden;
	}
	.hero__sky {
		position: absolute;
		left: 0; right: 0; top: 0;
		width: 100%;
		height: 100%;
	}
	.hero__tint {
		position: absolute;
		left: 0; right: 0; top: 0;
		height: 100%;
		background: linear-gradient(168deg, rgba(155,123,255,0.80) 0%, rgba(128,92,250,0.70) 40%, rgba(108,63,242,0.34) 72%, rgba(245,240,255,0.34) 100%);
	}
	.hero__spark {
		position: absolute;
		border-radius: 50%;
		background: $c-sun;
		box-shadow: 0 0 0 8rpx rgba(255, 201, 79, 0.18);
		animation: sparkFloat 3.4s ease-in-out infinite;
	}
	.hero__spark--1 { width: 14rpx; height: 14rpx; top: 78rpx; right: 56rpx; }
	.hero__spark--2 { width: 10rpx; height: 10rpx; top: 140rpx; right: 138rpx; background: #fff; box-shadow: 0 0 0 6rpx rgba(255,255,255,0.2); animation-delay: .6s; }
	.hero__spark--3 { width: 12rpx; height: 12rpx; top: 208rpx; right: 34rpx; background: $c-mint-light; box-shadow: 0 0 0 6rpx rgba(147,237,207,0.22); animation-delay: 1.2s; }
	@keyframes sparkFloat {
		0%, 100% { transform: translateY(0); opacity: 1; }
		50% { transform: translateY(-10rpx); opacity: .65; }
	}
	.hero__copy {
		position: relative;
		z-index: 5;
		padding: 24rpx 28rpx 0;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
	}
	.hero__pill {
		display: flex;
		align-items: center;
		height: 46rpx;
		padding: 0 16rpx;
		border-radius: $r-pill;
		background: rgba(255, 255, 255, 0.94);
		box-shadow: 0 6rpx 18rpx rgba(84, 45, 175, 0.18);
	}
	.hero__live {
		width: 12rpx;
		height: 12rpx;
		border-radius: 50%;
		background: $c-mint;
		margin-right: 10rpx;
		box-shadow: 0 0 0 6rpx rgba(41, 202, 131, 0.16);
	}
	.hero__pill-txt { font-size: $fs-caption; color: $c-deep; font-weight: $fw-medium; }
	.hero__num {
		font-family: $ff-num;
		font-size: 25rpx;
		font-weight: $fw-bold;
		color: $c-primary;
	}
	.hero__title {
		display: block;
		margin-top: 20rpx;
		font-size: 52rpx;
		line-height: 1.14;
		font-weight: $fw-bold;
		color: #fff;
		letter-spacing: -1.4rpx;
		text-shadow: 0 4rpx 20rpx rgba(46, 12, 106, 0.55), 0 2rpx 6rpx rgba(46, 12, 106, 0.4);
	}
	.hero__title--2 { margin-top: 2rpx; color: #FFF0B8; }
	.hero__search {
		margin-top: 18rpx;
		width: 370rpx;
		height: 66rpx;
		border-radius: $r-pill;
		background: rgba(255, 255, 255, 0.97);
		box-shadow: 0 10rpx 28rpx rgba(46, 12, 106, 0.26), inset 0 2rpx 0 #fff;
		display: flex;
		align-items: center;
		padding: 0 24rpx;
	}
	.hero__search-ico { width: 28rpx; height: 28rpx; opacity: 0.6; }
	.hero__search-ph {
		margin-left: 12rpx;
		font-size: $fs-body;
		color: $t-sub;
	}
	.hero__trio {
		position: absolute;
		z-index: 3;
		left: 52%;
		bottom: -6rpx;
		width: 430rpx;
	}
	.hero__planet {
		position: absolute;
		z-index: 6;
		right: 14rpx;
		bottom: 16rpx;
		width: 112rpx;
		height: 108rpx;
		filter: drop-shadow(0 8rpx 18rpx rgba(46, 12, 106, 0.4));
		animation: haloFloat 4s ease-in-out infinite;
	}
	.hero__fade {
		position: absolute;
		left: 0; right: 0; bottom: 0;
		height: 80rpx;
		background: linear-gradient(180deg, rgba(128, 92, 250, 0) 0%, rgba(84, 45, 175, 0.22) 100%);
		z-index: 4;
		pointer-events: none;
	}

	/* 任务大卡（满幅，与品牌屏同高） */
	.hero__slide--task { padding: 0; }
	.task__tag {
		position: absolute;
		left: 0; top: 0;
		height: 42rpx;
		padding: 0 20rpx;
		border-radius: 0 0 $r-sm 0;
		color: #fff;
		font-size: 21rpx;
		font-weight: $fw-semibold;
		line-height: 42rpx;
		z-index: 4;
	}
	.task__body {
		position: absolute;
		left: 30rpx;
		top: 66rpx;
		z-index: 5;
		width: 440rpx;
	}
	.task__eyebrow {
		display: block;
		font-size: 21rpx;
		font-weight: $fw-semibold;
		color: $c-primary;
		letter-spacing: 1rpx;
	}
	.task__title {
		display: block;
		margin-top: 14rpx;
		font-size: 42rpx;
		line-height: 1.22;
		font-weight: $fw-bold;
		color: $c-ink;
		letter-spacing: -1rpx;
	}
	.task__desc {
		display: block;
		margin-top: 14rpx;
		font-size: 23rpx;
		color: $c-deep;
		opacity: 0.86;
		line-height: 1.4;
	}
	.task__cta {
		display: flex;
		align-items: center;
		justify-content: center;
		margin-top: 26rpx;
		width: 168rpx;
		height: 60rpx;
		border-radius: $r-pill;
		background: $g-cta;
		box-shadow: 0 10rpx 22rpx rgba(128, 92, 250, 0.30);
	}
	.task__cta-t {
		color: #fff;
		font-size: 24rpx;
		font-weight: $fw-semibold;
	}
	.task__cta-ico {
		width: 22rpx;
		height: 22rpx;
		margin-left: 6rpx;
		transform: rotate(-90deg);
		filter: brightness(0) invert(1);
	}
	.task__point {
		position: absolute;
		right: 28rpx;
		top: 70rpx;
		z-index: 5;
		display: flex;
		align-items: baseline;
		height: 56rpx;
		padding: 0 18rpx;
		border-radius: $r-pill;
		background: linear-gradient(135deg, #FFE39B 0%, $c-sun 100%);
		box-shadow: 0 8rpx 18rpx rgba(255, 201, 79, 0.42);
	}
	.task__point-num {
		font-family: $ff-num;
		font-size: 36rpx;
		font-weight: $fw-bold;
		color: #7A5200;
		line-height: 56rpx;
	}
	.task__point-unit {
		margin-left: 4rpx;
		font-size: 20rpx;
		color: #7A5200;
		line-height: 56rpx;
	}
	.task__art {
		position: absolute;
		z-index: 2;
		right: -20rpx;
		bottom: -30rpx;
		width: 400rpx;
		opacity: 0.96;
	}
	.task__halo {
		position: absolute;
		z-index: 1;
		right: 40rpx;
		top: 150rpx;
		width: 260rpx;
		height: 260rpx;
		border-radius: 50%;
		background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0) 72%);
		animation: haloFloat 5s ease-in-out infinite;
	}
	@keyframes haloFloat {
		0%, 100% { transform: translateY(0) scale(1); opacity: .9; }
		50% { transform: translateY(-12rpx) scale(1.04); opacity: .7; }
	}

	/* 统一指示器 */
	.hero__dots {
		position: absolute;
		left: 0; right: 0;
		bottom: 18rpx;
		z-index: 9;
		display: flex;
		justify-content: center;
		align-items: center;
	}
	.hero__dot {
		width: 10rpx;
		height: 10rpx;
		border-radius: $r-pill;
		background: rgba(255, 255, 255, 0.5);
		margin: 0 5rpx;
		box-shadow: 0 1rpx 4rpx rgba(46, 12, 106, 0.3);
		transition: width 240ms $ease-out;
	}
	.hero__dot--on {
		width: 30rpx;
		background: #fff;
	}

	/* ══════════ 3 类目 ══════════ */
	.cats {
		display: flex;
		flex-wrap: wrap;
		margin: 22rpx $page-x 0;
		padding: 30rpx 16rpx 14rpx;
		border-radius: $r-lg;
		background: $g-glass;
		border: 2rpx solid rgba(255, 255, 255, 0.9);
		box-shadow: 0 14rpx 36rpx rgba(123, 97, 255, 0.12), inset 0 2rpx 0 rgba(255, 255, 255, 0.95);
	}
	.cats__item {
		width: 33.333%;
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-bottom: 26rpx;
	}
	.cats__fig {
		width: 112rpx;
		height: 112rpx;
		border-radius: 34rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: inset 0 2rpx 0 rgba(255, 255, 255, 0.9);
	}
	.cats__img { width: 92rpx; height: 92rpx; }
	.cats__label {
		margin-top: 12rpx;
		font-size: $fs-caption;
		font-weight: $fw-semibold;
		color: $t-main;
	}

	/* ══════════ 通用区块头 ══════════ */
	.sec { margin-top: 44rpx; }
	.sec__hd {
		display: flex;
		align-items: flex-end;
		justify-content: space-between;
		padding: 0 $page-x;
		margin-bottom: 22rpx;
	}
	.sec__hd-l { display: flex; align-items: baseline; }
	.sec__title {
		font-size: $fs-h1;
		font-weight: $fw-bold;
		color: $c-ink;
		letter-spacing: -1rpx;
	}
	.sec__sub {
		margin-left: 14rpx;
		font-size: $fs-caption;
		color: $t-sub;
		letter-spacing: 0.2rpx;
	}
	.sec__more {
		font-size: $fs-caption;
		color: $c-primary;
		font-weight: $fw-semibold;
	}

	/* ══════════ 横向滚动容器 ══════════ */
	.rail { width: 100%; white-space: nowrap; }
	.rail__inner {
		display: inline-block;
		padding: 4rpx $page-x 8rpx;
		white-space: nowrap;
	}

	/* ══════════ 4 现在可以搭（榜单出血卡） ══════════ */
	.now {
		position: relative;
		display: inline-block;
		vertical-align: top;
		width: 520rpx;
		margin-right: 22rpx;
		border-radius: $r-md;
		background: #fff;
		box-shadow: 0 12rpx 30rpx rgba(84, 45, 175, 0.14);
		overflow: hidden;
	}
	.now__cover {
		position: relative;
		width: 100%;
		height: 240rpx;
	}
	.now__img { width: 100%; height: 100%; display: block; }
	.now__rank {
		position: absolute;
		left: 0;
		top: 0;
		min-width: 48rpx;
		height: 48rpx;
		padding: 0 10rpx;
		border-radius: 0 0 $r-sm 0;
		background: $g-cta;
		color: #fff;
		font-family: $ff-num;
		font-size: 26rpx;
		font-weight: $fw-bold;
		line-height: 48rpx;
		text-align: center;
		box-shadow: 0 4rpx 12rpx rgba(128, 92, 250, 0.28);
	}
	.now__clock {
		position: absolute;
		right: 16rpx;
		top: 16rpx;
		height: 40rpx;
		padding: 0 16rpx;
		border-radius: $r-pill;
		background: rgba(42, 36, 64, 0.58);
		color: #fff;
		font-size: 20rpx;
		line-height: 40rpx;
	}
	.now__body { padding: 20rpx 22rpx 22rpx; }
	.now__title {
		display: block;
		font-size: 32rpx;
		font-weight: $fw-semibold;
		color: $t-main;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	.now__meta {
		display: flex;
		align-items: center;
		margin-top: 12rpx;
	}
	.now__ico { width: 24rpx; height: 24rpx; opacity: 0.8; }
	.now__meta-txt {
		margin-left: 6rpx;
		font-size: 22rpx;
		color: $t-sub;
	}
	.now__sep {
		width: 2rpx;
		height: 18rpx;
		background: $c-line;
		margin: 0 12rpx;
	}
	.now__foot {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-top: 20rpx;
	}
	.now__people { display: flex; align-items: center; }
	.now__av {
		width: 46rpx;
		height: 46rpx;
		border-radius: 50%;
		border: 3rpx solid #fff;
		color: #fff;
		font-size: 20rpx;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.now__av + .now__av { margin-left: -12rpx; }
	.now__count {
		margin-left: 12rpx;
		font-family: $ff-num;
		font-size: 24rpx;
		font-weight: $fw-bold;
		color: $c-primary;
	}
	.now__join {
		height: 56rpx;
		padding: 0 30rpx;
		border-radius: $r-pill;
		background: $g-cta;
		color: #fff;
		font-size: 24rpx;
		font-weight: $fw-semibold;
		line-height: 56rpx;
		box-shadow: 0 8rpx 20rpx rgba(128, 92, 250, 0.28);
	}

	/* ══════════ 空态 ══════════ */
	.empty {
		margin: 0 $page-x;
		padding: 44rpx 0 40rpx;
		border-radius: $r-lg;
		background: $g-glass;
		border: 2rpx dashed rgba(128, 92, 250, 0.22);
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	.empty__img { width: 140rpx; height: 136rpx; }
	.empty__t {
		margin-top: 12rpx;
		font-size: 30rpx;
		font-weight: $fw-semibold;
		color: $t-main;
	}
	.empty__d {
		margin-top: 8rpx;
		font-size: $fs-caption;
		color: $t-sub;
	}
	.empty__btn {
		margin-top: 24rpx;
		height: 68rpx;
		padding: 0 40rpx;
		border-radius: $r-pill;
		background: $g-cta;
		color: #fff;
		font-size: $fs-body;
		font-weight: $fw-semibold;
		line-height: 68rpx;
		box-shadow: 0 10rpx 24rpx rgba(128, 92, 250, 0.28);
	}

	/* ══════════ 5 同校动态 ══════════ */
	.tabs { width: 100%; white-space: nowrap; margin-bottom: 20rpx; }
	.tabs__inner { display: inline-block; padding: 0 $page-x; }
	.tabs__item {
		display: inline-block;
		height: 60rpx;
		padding: 0 28rpx;
		margin-right: 14rpx;
		border-radius: $r-pill;
		background: rgba(255, 255, 255, 0.78);
		color: $t-sub;
		font-size: $fs-caption;
		font-weight: $fw-medium;
		letter-spacing: 0.4rpx;
		line-height: 60rpx;
		border: 2rpx solid transparent;
	}
	.tabs__item--on {
		background: $g-brand;
		color: #fff;
		font-weight: $fw-bold;
		letter-spacing: 0.2rpx;
		box-shadow: 0 8rpx 20rpx rgba(128, 92, 250, 0.26);
	}
	.feed {
		position: relative;
		margin: 0 $page-x 20rpx;
		padding: 24rpx 26rpx 20rpx;
		border-radius: $r-md;
		background: rgba(255, 255, 255, 0.94);
		border: 2rpx solid rgba(255, 255, 255, 0.96);
		box-shadow: 0 10rpx 30rpx rgba(123, 97, 255, 0.10);
	}
	.feed__head { display: flex; align-items: center; }
	.feed__av {
		width: 68rpx;
		height: 68rpx;
		border-radius: 50%;
		border: 3rpx solid #fff;
		color: #fff;
		font-size: 27rpx;
		font-weight: $fw-semibold;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 0 5rpx 14rpx rgba(123, 97, 255, 0.20);
	}
	.feed__who { margin-left: 14rpx; flex: 1; }
	.feed__row { display: flex; align-items: center; }
	/* 品牌排版：不加载外部字体（保启动速度），靠字重/字距/颜色分层做设计感 */
	.feed__name {
		font-size: 31rpx;
		font-weight: $fw-bold;
		color: $c-ink;
		letter-spacing: -0.6rpx;
	}
	.feed__id {
		margin-left: 12rpx;
		height: 32rpx;
		padding: 0 13rpx;
		border-radius: $r-pill;
		font-size: 19rpx;
		font-weight: $fw-semibold;
		letter-spacing: 0.2rpx;
		line-height: 32rpx;
	}
	.feed__meta {
		display: block;
		margin-top: 7rpx;
		font-size: 21rpx;
		color: $t-tertiary;
		letter-spacing: 0.5rpx;
	}
	.feed__more {
		font-size: 30rpx;
		color: $t-tertiary;
		letter-spacing: 2rpx;
		padding: 0 6rpx;
		line-height: 1;
	}
	.feed__main {
		display: flex;
		align-items: stretch;
		margin-top: 18rpx;
	}
	.feed__left {
		flex: 1;
		min-width: 0;
		display: flex;
		flex-direction: column;
	}
	.feed__text {
		font-size: 28rpx;
		line-height: 1.66;
		color: #37314E;
		letter-spacing: 0.3rpx;
	}
	.feed__topics {
		display: flex;
		flex-wrap: wrap;
		margin-top: auto;
		padding-top: 14rpx;
	}
	.feed__topic {
		height: 42rpx;
		padding: 0 16rpx;
		margin-right: 10rpx;
		border-radius: $r-pill;
		background: rgba(128, 92, 250, 0.10);
		color: $c-primary;
		font-size: 21rpx;
		font-weight: $fw-semibold;
		letter-spacing: 0.3rpx;
		line-height: 42rpx;
	}
	.feed__topic--soft {
		background: rgba(255, 201, 79, 0.14);
		color: #B07A00;
	}
	.feed__thumb {
		width: 168rpx;
		height: 168rpx;
		margin-left: 18rpx;
		border-radius: 20rpx;
		flex-shrink: 0;
	}
	.feed__acts {
		display: flex;
		align-items: center;
		margin-top: 18rpx;
		padding-top: 16rpx;
		border-top: 2rpx solid rgba(128, 92, 250, 0.08);
	}
	.feed__act { display: flex; align-items: center; margin-right: 30rpx; }
	.feed__act-ico { width: 28rpx; height: 28rpx; opacity: 0.55; }
	.feed__act-n {
		margin-left: 8rpx;
		font-family: $ff-num;
		font-size: 25rpx;
		font-weight: $fw-semibold;
		color: $t-sub;
	}
	.feed__join {
		margin-left: auto;
		height: 50rpx;
		padding: 0 22rpx;
		border-radius: $r-pill;
		border: 2rpx solid $c-primary;
		background: #fff;
		font-size: 22rpx;
		font-weight: $fw-bold;
		letter-spacing: 0.3rpx;
		line-height: 46rpx;
	}

	/* ══════════ 6 校园活动 ══════════ */
	.act {
		position: relative;
		display: inline-block;
		vertical-align: top;
		width: 600rpx;
		height: 400rpx;
		margin-right: 22rpx;
		border-radius: $r-md;
		overflow: hidden;
		box-shadow: 0 14rpx 34rpx rgba(90, 60, 180, 0.18);
	}
	.act__img { width: 100%; height: 100%; display: block; }
	.act__mask {
		position: absolute;
		left: 0; right: 0; bottom: 0;
		height: 76%;
		background: linear-gradient(180deg, rgba(32, 24, 58, 0) 0%, rgba(32, 24, 58, 0.72) 100%);
	}
	.act__flag {
		position: absolute;
		left: 20rpx;
		top: 20rpx;
		height: 44rpx;
		padding: 0 18rpx;
		border-radius: $r-pill;
		font-size: 20rpx;
		font-weight: $fw-semibold;
		line-height: 44rpx;
	}
	.act__flag--sun { background: $c-sun; color: #6B4A00; }
	.act__flag--mint { background: $c-mint; color: #fff; }
	.act__flag--purple { background: $c-primary; color: #fff; }
	.act__info {
		position: absolute;
		left: 26rpx; right: 26rpx; bottom: 24rpx;
	}
	.act__title {
		display: block;
		font-size: 34rpx;
		font-weight: $fw-bold;
		color: #fff;
		letter-spacing: -0.4rpx;
	}
	.act__meta { display: flex; align-items: center; margin-top: 10rpx; }
	.act__meta-txt { font-size: 22rpx; color: rgba(255, 255, 255, 0.86); }
	.act__dot {
		width: 6rpx;
		height: 6rpx;
		border-radius: 50%;
		background: rgba(255, 255, 255, 0.6);
		margin: 0 12rpx;
	}
	.act__foot {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-top: 14rpx;
	}
	.act__host { font-size: 22rpx; color: rgba(255, 255, 255, 0.7); }
	.act__join {
		height: 42rpx;
		padding: 0 16rpx;
		border-radius: $r-pill;
		background: rgba(255, 255, 255, 0.22);
		color: #fff;
		font-size: 20rpx;
		line-height: 42rpx;
	}

	/* ══════════ 7 同频推荐 ══════════ */
	.mate {
		display: inline-block;
		vertical-align: top;
		width: 216rpx;
		margin-right: 18rpx;
		padding: 26rpx 18rpx 22rpx;
		border-radius: $r-md;
		background: $g-glass;
		border: 2rpx solid rgba(255, 255, 255, 0.9);
		box-shadow: 0 10rpx 26rpx rgba(123, 97, 255, 0.10);
		text-align: center;
	}
	.mate__av {
		position: relative;
		width: 96rpx;
		height: 96rpx;
		border-radius: 50%;
		margin: 0 auto;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 0 6rpx 18rpx rgba(123, 97, 255, 0.20);
	}
	.mate__ch { color: #fff; font-size: 36rpx; font-weight: $fw-semibold; }
	.mate__on {
		position: absolute;
		right: 0;
		bottom: 4rpx;
		width: 20rpx;
		height: 20rpx;
		border-radius: 50%;
		background: $c-mint;
		border: 3rpx solid #fff;
	}
	.mate__name {
		display: block;
		margin-top: 14rpx;
		font-size: 26rpx;
		font-weight: $fw-semibold;
		color: $t-main;
	}
	.mate__college {
		display: block;
		margin-top: 4rpx;
		font-size: 20rpx;
		color: $t-sub;
	}
	.mate__tags {
		display: flex;
		flex-wrap: wrap;
		justify-content: center;
		margin-top: 12rpx;
	}
	.mate__tag {
		height: 34rpx;
		padding: 0 12rpx;
		margin: 0 4rpx 6rpx;
		border-radius: $r-pill;
		background: rgba(128, 92, 250, 0.09);
		color: $c-primary;
		font-size: 19rpx;
		line-height: 34rpx;
	}
	.mate__hi {
		margin-top: 10rpx;
		height: 52rpx;
		border-radius: $r-pill;
		background: rgba(128, 92, 250, 0.10);
		color: $c-primary;
		font-size: 22rpx;
		font-weight: $fw-semibold;
		line-height: 52rpx;
	}

	/* ══════════ 8 结尾 ══════════ */
	.end {
		margin: 48rpx $page-x 0;
		padding: 40rpx 32rpx 38rpx;
		border-radius: $r-lg;
		background: linear-gradient(160deg, #F1E9FF 0%, #FBF7FF 60%, #FFF6DF 100%);
		border: 2rpx solid rgba(255, 255, 255, 0.9);
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	.end__planet { width: 128rpx; height: 124rpx; }
	.end__t {
		margin-top: 14rpx;
		font-size: 32rpx;
		font-weight: $fw-bold;
		color: $c-ink;
	}
	.end__d {
		margin-top: 8rpx;
		font-size: $fs-caption;
		color: $t-sub;
	}
	.end__btn {
		margin-top: 26rpx;
		height: 72rpx;
		padding: 0 44rpx;
		border-radius: $r-pill;
		background: $g-cta;
		color: #fff;
		font-size: $fs-body;
		font-weight: $fw-semibold;
		line-height: 72rpx;
		box-shadow: 0 12rpx 28rpx rgba(128, 92, 250, 0.30);
	}

	/* ══════════ 首屏异常态 ══════════ */
	.err {
		padding: 180rpx $page-x 0;
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	.err__img { width: 180rpx; height: 174rpx; opacity: 0.9; }
	.err__t {
		margin-top: 20rpx;
		font-size: 34rpx;
		font-weight: $fw-bold;
		color: $t-main;
	}
	.err__d {
		margin-top: 10rpx;
		font-size: $fs-caption;
		color: $t-sub;
	}
	.err__btn {
		margin-top: 36rpx;
		height: 76rpx;
		padding: 0 52rpx;
		border-radius: $r-pill;
		background: $g-cta;
		color: #fff;
		font-size: $fs-body;
		font-weight: $fw-semibold;
		line-height: 76rpx;
		box-shadow: 0 12rpx 28rpx rgba(128, 92, 250, 0.28);
	}

	/* ══════════ 切 tab 轻量加载 / 分页底部 ══════════ */
	.feed-load {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 10rpx 0 26rpx;
	}
	.feed-load__t {
		margin-left: 12rpx;
		font-size: $fs-caption;
		color: $t-sub;
	}
	.spin {
		width: 28rpx;
		height: 28rpx;
		border-radius: 50%;
		border: 4rpx solid rgba(128, 92, 250, 0.18);
		border-top-color: $c-primary;
		animation: spinRotate 700ms linear infinite;
	}
	@keyframes spinRotate {
		to { transform: rotate(360deg); }
	}
	.foot { padding: 8rpx $page-x 10rpx; }
	.foot__loading {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 26rpx 0;
	}
	.foot__t {
		margin-left: 12rpx;
		font-size: $fs-caption;
		color: $t-tertiary;
	}
	.foot__retry {
		display: flex;
		justify-content: center;
		padding: 24rpx 0;
	}
	.foot__retry-t {
		height: 60rpx;
		padding: 0 28rpx;
		border-radius: $r-pill;
		background: rgba(128, 92, 250, 0.08);
		color: $c-primary;
		font-size: $fs-caption;
		line-height: 60rpx;
	}
	.foot__end {
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 30rpx 0 10rpx;
	}
	.foot__line {
		width: 56rpx;
		height: 2rpx;
		background: $c-line;
	}
	.foot__end .foot__t { margin: 0 16rpx; }
	.foot__empty {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 40rpx 0 20rpx;
	}
	.foot__empty-img { width: 120rpx; height: 86rpx; opacity: 0.85; }
	.foot__empty .foot__t { margin: 12rpx 0 0; }

	/* ══════════ 骨架屏 ══════════ */
	.sk { padding: 24rpx 0 0; }
	.sk__hero {
		margin: 0 $page-x;
		height: 400rpx;
		border-radius: $r-lg;
		background: #ECE5FA;
		animation: skBreath 1.4s ease-in-out infinite;
	}
	.sk__cats {
		display: flex;
		flex-wrap: wrap;
		margin: 24rpx $page-x 0;
	}
	.sk__cat {
		width: 33.333%;
		height: 150rpx;
	}
	.sk__cat::after {
		content: '';
		display: block;
		width: 92rpx;
		height: 92rpx;
		margin: 0 auto;
		border-radius: 50%;
		background: #ECE5FA;
		animation: skBreath 1.4s ease-in-out infinite;
	}
	.sk__promo {
		margin: 24rpx $page-x 0;
		height: 152rpx;
		border-radius: $r-md;
		background: #ECE5FA;
		animation: skBreath 1.4s ease-in-out infinite;
	}
	.sk__line {
		margin: 36rpx $page-x 20rpx;
		height: 40rpx;
		width: 240rpx;
		border-radius: 8rpx;
		background: #ECE5FA;
		animation: skBreath 1.4s ease-in-out infinite;
	}
	.sk__rail { white-space: nowrap; padding-left: $page-x; overflow: hidden; }
	.sk__card {
		display: inline-block;
		width: 520rpx;
		height: 380rpx;
		margin-right: 22rpx;
		border-radius: $r-md;
		background: #ECE5FA;
		animation: skBreath 1.4s ease-in-out infinite;
	}
	.sk__feed {
		margin: 0 $page-x 20rpx;
		height: 220rpx;
		border-radius: $r-md;
		background: #ECE5FA;
		animation: skBreath 1.4s ease-in-out infinite;
	}
	@keyframes skBreath {
		0%, 100% { opacity: 1; }
		50% { opacity: 0.55; }
	}
</style>
