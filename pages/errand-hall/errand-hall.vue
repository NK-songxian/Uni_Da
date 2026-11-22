<template>
	<view class="eh unida-page unida-page--tab">
		<view class="eh-safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 3D hero：吉祥物 + 场景 -->
		<view class="eh__hero">
			<image class="eh__hero-bubble" src="/static/unida/msg/ico-bubble.webp" mode="aspectFit" />
			<view class="eh__hero-txt">
				<text class="eh__title">跑腿大厅</text>
				<text class="eh__sub">同学互助，小事不用愁</text>
			</view>
			<view class="eh__mine" @click="goMine"><text class="eh__mine-t">我的订单</text></view>
			<image class="eh__hero-mascot" src="/static/unida/msg/mascot-wave.webp" mode="widthFix" />
		</view>

		<!-- 搜索框 -->
		<view class="eh__search" @click="onSearch">
			<image class="eh__search-ico" src="/static/unida/msg/ico-search.webp" mode="aspectFit" />
			<text class="eh__search-ph">搜索跑腿需求（快递、外卖…）</text>
		</view>

		<!-- 快捷分类：立体图标 -->
		<view class="eh__cats">
			<view class="eh__cat" v-for="(c, i) in cats" :key="i" @click="onCat(i)">
				<view class="eh__cat-icon" :class="'eh__cat-icon--' + c.tone">
					<image class="eh__cat-img" :src="c.icon" mode="aspectFit" />
				</view>
				<text class="eh__cat-label">{{ c.label }}</text>
			</view>
		</view>

		<!-- 发布 CTA：3D 购物袋场景 -->
		<view class="eh__cta" @click="onPublish">
			<image class="eh__cta-scene" src="/static/unida/msg/scene-takeout.webp" mode="aspectFit" />
			<view class="eh__cta-info">
				<text class="eh__cta-title">需要帮忙？发布需求</text>
				<text class="eh__cta-sub">同学接单，快速搞定</text>
				<view class="eh__cta-btn"><text class="eh__cta-btn-t">去发布 ›</text></view>
			</view>
		</view>

		<!-- 需求列表 -->
		<view class="eh__sect">
			<text class="eh__sect-t">{{ activeCat > 0 ? cats[activeCat - 1].label : '附近需求' }}</text>
			<view class="eh__sect-r">
				<text class="eh__sort" :class="{ 'eh__sort--on': sort === 'new' }" @click="onSort('new')">最新</text>
				<text class="eh__sort" :class="{ 'eh__sort--on': sort === 'reward' }" @click="onSort('reward')">赏金最高</text>
			</view>
		</view>
		<view class="eh__item" v-for="(o, i) in orders" :key="o.id" @click="onOrder(i)">
			<view class="eh__item-head">
				<view class="eh__cat-chip"><text class="eh__cat-chip-t">{{ o.type }}</text></view>
				<view class="eh__reward"><text class="eh__reward-s">¥</text><text class="eh__reward-n">{{ o.rewardText }}</text></view>
			</view>
			<text class="eh__item-title">{{ o.title }}</text>
			<view class="eh__item-meta">
				<view class="eh__meta-row"><image class="eh__meta-ico" src="/static/icons-dark/pin.png" mode="aspectFit" /><text class="eh__meta-t">{{ o.pickup }} → {{ o.delivery }}</text></view>
				<view class="eh__meta-row"><image class="eh__meta-ico" src="/static/icons-dark/clock.png" mode="aspectFit" /><text class="eh__meta-t">{{ o.deadline || '时间灵活' }}</text></view>
			</view>
			<view class="eh__item-foot">
				<view class="eh__user">
					<view class="eh__avatar"><text class="eh__avatar-ch">{{ o.publisherName[0] }}</text></view>
					<text class="eh__user-t">{{ o.publisherName }} · {{ o.time }}发布</text>
				</view>
				<view class="eh__status"><text class="eh__status-t">立即接单</text></view>
			</view>
		</view>

		<!-- 空态 -->
		<view class="eh__empty" v-if="!loading && orders.length === 0">
			<text class="eh__empty-t">{{ activeCat > 0 ? '该分类暂时没有待接单需求' : '这个时段还没人发单，你来发第一个？' }}</text>
		</view>

		<view class="eh__bottom-space"></view>
		<unida-tabbar :current="1" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';
	import { callCloud } from '@/common/cloud.js';
	import { timeAgo } from '@/common/fmt.js';

	export default {
		components: { unidaTabbar },
		data() {
			return {
				statusBar: 0,
				loading: false,
				cats: [
					{ label: '快递代取', icon: '/static/unida/msg/ico-bag.webp', tone: 'purple' },
					{ label: '外卖代拿', icon: '/static/unida/msg/ico-megaphone.webp', tone: 'orange' },
					{ label: '物品代送', icon: '/static/unida/msg/ico-calendar.webp', tone: 'pink' },
					{ label: '其他互助', icon: '/static/unida/msg/ico-bubble.webp', tone: 'green' }
				],
				activeCat: 0,
				sort: 'new',
				orders: []
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		onShow() {
			this.loadHall();
		},
		onPullDownRefresh() {
			this.loadHall();
		},
		methods: {
			goMine() { uni.navigateTo({ url: '/pages/my-errands/my-errands' }); },
			onSort(s) {
				if (this.sort === s) return;
				this.sort = s;
				this.loadHall();
			},
			onCat(i) {
				this.activeCat = this.activeCat === i ? 0 : i;
				this.loadHall();
			},
			async loadHall() {
				if (this.loading) return;
				this.loading = true;
				try {
					const r = await callCloud('errand', {
						action: 'hall',
						cat: this.activeCat > 0 ? this.cats[this.activeCat - 1].label : '',
						sort: this.sort
					});
					this.orders = (r.list || []).map((x) => ({
						...x,
						rewardText: x.reward % 1 === 0 ? String(x.reward) : x.reward.toFixed(2),
						time: timeAgo(x.createdAt)
					}));
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '加载跑腿大厅失败', icon: 'none' });
				} finally {
					this.loading = false;
					uni.stopPullDownRefresh();
				}
			},
			onSearch() { uni.showToast({ title: '搜索待接入', icon: 'none' }); },
			onPublish() { uni.navigateTo({ url: '/pages/errand-publish/errand-publish' }); },
			onOrder(i) {
				const o = this.orders[i];
				uni.navigateTo({ url: '/pages/errand-detail/errand-detail?id=' + (o && o.id) });
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.eh { min-height: 100vh; padding: 0 $page-x; box-sizing: border-box; background: linear-gradient(180deg, #E4D3FF 0%, $c-mist 20%, #F7F3FF 100%); }

	/* ---------- 3D hero ---------- */
	.eh__hero {
		position: relative;
		display: flex; align-items: flex-start;
		min-height: 200rpx;
		padding-top: 32rpx;
	}
	.eh__hero-txt { display: flex; flex-direction: column; position: relative; z-index: 2; }
	.eh__title { font-size: 48rpx; font-weight: 800; color: $c-ink; letter-spacing: 2rpx; }
	.eh__sub { margin-top: 10rpx; font-size: 24rpx; color: $t-sub; }
	.eh__hero-mascot { position: absolute; right: -20rpx; top: 0; width: 220rpx; z-index: 1; }
	.eh__hero-bubble { position: absolute; right: 200rpx; top: 4rpx; width: 60rpx; opacity: 0.9; z-index: 1; }
	.eh__mine {
		align-self: center;
		margin-top: 40rpx;
		margin-left: 24rpx;
		z-index: 2;
		background: rgba(255, 255, 255, 0.7);
		border-radius: $r-pill;
		padding: 10rpx 24rpx;
		box-shadow: $sh-card;
	}
	.eh__mine-t { font-size: 22rpx; color: $c-primary; font-weight: 700; }

	/* ---------- 搜索 ---------- */
	.eh__search {
		display: flex; align-items: center;
		height: 84rpx;
		background: $c-white;
		border-radius: $r-pill;
		box-shadow: $sh-card;
		padding: 0 28rpx;
	}
	.eh__search-ico { width: 52rpx; height: 52rpx; margin-right: 14rpx; }
	.eh__search-ph { font-size: 26rpx; color: $t-tertiary; }

	/* ---------- 分类：立体图标 ---------- */
	.eh__cats { display: flex; margin-top: 28rpx; }
	.eh__cat { flex: 1; display: flex; flex-direction: column; align-items: center; }
	.eh__cat-icon {
		width: 128rpx; height: 128rpx;
		border-radius: 36rpx;
		display: flex; align-items: center; justify-content: center;
		box-shadow: $sh-card;
	}
	.eh__cat-icon--purple { background: rgba(128, 92, 250, 0.13); }
	.eh__cat-icon--orange { background: rgba(255, 155, 119, 0.16); }
	.eh__cat-icon--pink { background: rgba(244, 114, 182, 0.14); }
	.eh__cat-icon--green { background: rgba(41, 202, 131, 0.14); }
	.eh__cat-img { width: 100rpx; height: 100rpx; }
	.eh__cat-label { margin-top: 14rpx; font-size: 24rpx; color: $t-main; font-weight: 600; }

	/* ---------- 发布 CTA ---------- */
	.eh__cta {
		display: flex; align-items: center;
		margin-top: 32rpx;
		padding: 24rpx;
		background: $g-brand;
		border-radius: $r-md;
		box-shadow: $sh-float;
	}
	.eh__cta-scene { width: 150rpx; height: 150rpx; margin-right: 16rpx; flex-shrink: 0; }
	.eh__cta-info { flex: 1; display: flex; flex-direction: column; }
	.eh__cta-title { font-size: 30rpx; font-weight: 700; color: $c-white; }
	.eh__cta-sub { margin-top: 10rpx; font-size: 22rpx; color: rgba(255, 255, 255, 0.85); }
	.eh__cta-btn {
		align-self: flex-start;
		margin-top: 20rpx;
		background: $c-white;
		border-radius: $r-pill;
		padding: 12rpx 26rpx;
	}
	.eh__cta-btn-t { font-size: 23rpx; color: $c-primary; font-weight: 700; }

	/* ---------- 需求列表 ---------- */
	.eh__sect { display: flex; align-items: baseline; margin-top: 36rpx; }
	.eh__sect-t { font-size: 32rpx; font-weight: 800; color: $c-ink; }
	.eh__sect-r { margin-left: auto; display: flex; align-items: center; }
	.eh__sort { font-size: 22rpx; color: $t-tertiary; margin-left: 20rpx; }
	.eh__sort--on { color: $c-primary; font-weight: 700; }
	.eh__item {
		margin-top: 16rpx;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 26rpx;
	}
	.eh__item-head { display: flex; align-items: center; justify-content: space-between; }
	.eh__cat-chip { background: rgba(128, 92, 250, 0.10); border-radius: $r-pill; padding: 8rpx 20rpx; }
	.eh__cat-chip-t { font-size: 21rpx; color: $c-primary; font-weight: 600; }
	.eh__reward { display: flex; align-items: baseline; }
	.eh__reward-s { font-size: 26rpx; color: $c-peach; font-weight: 700; }
	.eh__reward-n { font-size: 44rpx; color: $c-peach; font-weight: 800; font-family: $ff-num; }
	.eh__item-title { display: block; margin-top: 14rpx; font-size: 28rpx; font-weight: 700; color: $t-main; }
	.eh__item-meta { margin-top: 16rpx; }
	.eh__meta-row { display: flex; align-items: center; margin-top: 8rpx; }
	.eh__meta-ico { width: 26rpx; height: 26rpx; opacity: 0.55; }
	.eh__meta-t { margin-left: 10rpx; font-size: 23rpx; color: $t-sub; }
	.eh__item-foot {
		display: flex; align-items: center; justify-content: space-between;
		margin-top: 20rpx; padding-top: 20rpx;
		border-top: 2rpx solid $c-line;
	}
	.eh__user { display: flex; align-items: center; }
	.eh__avatar { width: 56rpx; height: 56rpx; border-radius: 50%; background: $g-brand; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
	.eh__avatar-ch { font-size: 24rpx; color: $c-white; font-weight: 700; }
	.eh__user-t { margin-left: 12rpx; font-size: 22rpx; color: $t-sub; }
	.eh__status { background: $g-cta; border-radius: $r-pill; padding: 12rpx 28rpx; box-shadow: 0 8rpx 16rpx rgba(128, 92, 250, 0.24); }
	.eh__status-t { font-size: 23rpx; color: $c-white; font-weight: 700; }

	.eh__empty { display: flex; justify-content: center; padding: 100rpx 0; }
	.eh__empty-t { font-size: 26rpx; color: $t-tertiary; }

	.eh__bottom-space { height: 220rpx; }
</style>
