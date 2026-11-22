<template>
	<view class="me unida-page">
		<!-- ══════════ 自绘顶栏 ══════════ -->
		<view class="me__nav" :style="{ paddingTop: statusBar + 'px' }">
			<view class="me__nav-btn" @click="goBack">
				<image class="me__nav-ico" src="/static/icons-dark/back.png" mode="aspectFit" />
			</view>
			<text class="me__nav-title">我的订单</text>
			<view class="me__nav-btn" @click="goPublish">
				<image class="me__nav-ico" src="/static/icons-dark/bell.png" mode="aspectFit" />
			</view>
		</view>

		<!-- ══════════ 统计头 ══════════ -->
		<view class="me__hero">
			<image class="me__hero-img" src="/static/unida/planet/planet-cal.png" mode="aspectFit" />
			<view class="me__hero-info">
				<text class="me__hero-title">跑腿订单</text>
				<view class="me__hero-stats">
					<view class="me__stat">
						<text class="me__stat-n">{{ total }}</text>
						<text class="me__stat-k">全部</text>
					</view>
					<view class="me__stat-divider"></view>
					<view class="me__stat">
						<text class="me__stat-n">{{ countDoing }}</text>
						<text class="me__stat-k">进行中</text>
					</view>
					<view class="me__stat-divider"></view>
					<view class="me__stat">
						<text class="me__stat-n">{{ countDone }}</text>
						<text class="me__stat-k">已完成</text>
					</view>
				</view>
			</view>
		</view>

		<!-- ══════════ 角色 tab ══════════ -->
		<view class="me__tabs">
			<view
				v-for="(t, i) in tabs"
				:key="i"
				class="me__tab"
				:class="{ 'me__tab--on': role === t.key }"
				@click="onTab(t.key)"
			>
				<text class="me__tab-t">{{ t.label }}</text>
			</view>
		</view>

		<!-- ══════════ 订单列表 ══════════ -->
		<view class="me__list">
			<view class="me__card" v-for="(o, i) in listShow" :key="o.id" @click="onOpen(o)">
				<view class="me__head">
					<view class="me__type-chip"><text class="me__type-t">{{ o.type }}</text></view>
					<view class="me__status" :class="'me__status--' + statusKey(o.status)">
						<view class="me__status-dot"></view>
						<text class="me__status-t">{{ o.status }}</text>
					</view>
				</view>
				<view class="me__titlerow">
					<text class="me__title">{{ o.title }}</text>
					<text class="me__reward">¥{{ o.rewardText }}</text>
				</view>
				<view class="me__meta">
					<image class="me__meta-ico" src="/static/icons-dark/pin.png" mode="aspectFit" />
					<text class="me__meta-t">{{ o.pickup || '待沟通' }} → {{ o.delivery || '待沟通' }}</text>
				</view>
				<view class="me__meta">
					<text class="me__who">{{ o.role === 'publisher' ? '接单方' : '发布方' }}：{{ o.role === 'publisher' ? (o.acceptorName || '暂无人接单') : o.publisherName }}</text>
					<text class="me__time">{{ o.time }}</text>
				</view>
				<view class="me__foot">
					<text class="me__btn me__btn--ghost" @click.stop="onContact(o)">联系对方</text>
					<text v-if="o.role === 'publisher' && o.status === '待接单'" class="me__btn me__btn--danger" @click.stop="onCancel(o)">取消订单</text>
					<text v-if="o.role === 'publisher' && o.status === '进行中'" class="me__btn" @click.stop="onConfirm(o)">确认完成</text>
					<text class="me__btn me__btn--ghost" @click.stop="onOpen(o)">查看详情</text>
				</view>
			</view>

			<!-- ══════════ 空态 ══════════ -->
			<view class="me__empty" v-if="!loading && listShow.length === 0">
				<image class="me__empty-img" src="/static/unida/planet/planet-bubble.png" mode="aspectFit" />
				<text class="me__empty-t">这里还空空的</text>
				<text class="me__empty-sub">去跑腿大厅看看，或发一个需求</text>
				<view class="me__empty-btn" @click="goHall"><text class="me__empty-btn-t">去跑腿大厅</text></view>
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
				role: 'all',
				tabs: [
					{ label: '全部', key: 'all' },
					{ label: '我发布的', key: 'published' },
					{ label: '我接的', key: 'accepted' }
				],
				list: []
			};
		},
		computed: {
			listShow() {
				if (this.role === 'all') return this.list;
				return this.list.filter((x) => x.role === this.role);
			},
			total() { return this.list.length; },
			countDoing() { return this.list.filter((x) => x.status === '进行中').length; },
			countDone() { return this.list.filter((x) => x.status === '已完成').length; }
		},
		onLoad(q) {
			const sys = uni.getSystemInfoSync();
			this.statusBar = (sys && sys.statusBarHeight) || 0;
			if (q && q.role) this.role = q.role;
		},
		onShow() {
			this.loadList();
		},
		onPullDownRefresh() {
			this.loadList();
		},
		methods: {
			goBack() { uni.navigateBack(); },
			goPublish() { uni.navigateTo({ url: '/pages/errand-publish/errand-publish' }); },
			goHall() { uni.navigateTo({ url: '/pages/errand-hall/errand-hall' }); },
			onTab(key) { this.role = key; },
			statusKey(s) {
				if (s === '进行中') return 'ongoing';
				if (s === '已完成') return 'done';
				if (s === '已取消') return 'cancel';
				return 'wait';
			},
			async loadList() {
				if (this.loading) return;
				this.loading = true;
				try {
					const r = await callCloud('errand', { action: 'mine', token: getToken() });
					this.list = (r.list || []).map((x) => ({
						...x,
						role: x.myRole || (x.publisherOpenid === 'seed' ? 'accepted' : 'guest'),
						rewardText: (Number(x.reward) || 0) % 1 === 0 ? String(x.reward) : Number(x.reward).toFixed(2),
						time: timeAgo(x.updatedAt || x.createdAt)
					}));
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '获取订单失败', icon: 'none' });
				} finally {
					this.loading = false;
					uni.stopPullDownRefresh();
				}
			},
			onOpen(o) { uni.navigateTo({ url: '/pages/errand-detail/errand-detail?id=' + o.id }); },
			onContact(o) {
				// 详情接口返回对端信息；列表里用简化规则：种子单对端=官方助手
				const peer = o.publisherOpenid === 'seed' ? 'official' : (o.myRole === 'publisher' ? (o.acceptorOpenid || '') : o.publisherOpenid);
				const name = o.myRole === 'publisher' ? (o.acceptorName || '接单同学') : (o.publisherName || '同学');
				uni.navigateTo({ url: '/pages/chat/chat?peer=' + peer + '&name=' + encodeURIComponent(name) });
			},
			onCancel(o) {
				uni.showModal({
					title: '取消订单',
					content: '确定取消「' + o.title + '」吗？',
					confirmColor: '#FF5A4E',
					success: async (res) => {
						if (!res.confirm) return;
						try {
							await callCloud('errand', { action: 'cancel', token: getToken(), id: o.id });
							uni.showToast({ title: '已取消', icon: 'none' });
							this.loadList();
						} catch (e) {
							uni.showToast({ title: (e && e.message) || '操作失败', icon: 'none' });
						}
					}
				});
			},
			async onConfirm(o) {
				try {
					await callCloud('errand', { action: 'confirm', token: getToken(), id: o.id });
					uni.showToast({ title: '已确认完成', icon: 'success' });
					this.loadList();
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '操作失败', icon: 'none' });
				}
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.me { padding-bottom: calc(60rpx + env(safe-area-inset-bottom)); }

	/* ══════════ 顶栏 ══════════ */
	.me__nav {
		display: flex; align-items: center; justify-content: space-between;
		padding-left: $page-x; padding-right: $page-x; padding-bottom: 16rpx;
	}
	.me__nav-btn { width: 64rpx; height: 64rpx; display: flex; align-items: center; justify-content: center; }
	.me__nav-ico { width: 40rpx; height: 40rpx; }
	.me__nav-title { font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink; letter-spacing: 0.5rpx; }

	/* ══════════ 统计头 ══════════ */
	.me__hero {
		display: flex; align-items: center;
		margin: 8rpx $page-x 0; padding: 24rpx 28rpx;
		border-radius: $r-lg; background: #fff; box-shadow: $sh-card;
	}
	.me__hero-img { width: 150rpx; height: 150rpx; flex-shrink: 0; }
	.me__hero-info { flex: 1; margin-left: 20rpx; }
	.me__hero-title {
		display: block;
		font-size: $fs-h2; font-weight: $fw-bold; color: $c-ink; letter-spacing: -0.8rpx;
	}
	.me__hero-stats { display: flex; align-items: center; margin-top: 18rpx; }
	.me__stat { display: flex; flex-direction: column; align-items: center; margin-right: 28rpx; }
	.me__stat-n { font-family: $ff-num; font-size: $fs-h2; font-weight: $fw-bold; color: $c-primary; line-height: 1.1; }
	.me__stat-k { margin-top: 4rpx; font-size: $fs-micro; color: $t-sub; letter-spacing: 0.3rpx; }
	.me__stat-divider { width: 2rpx; height: 52rpx; background: $c-line; margin-right: 28rpx; }

	/* ══════════ tab ══════════ */
	.me__tabs { display: flex; margin: 24rpx $page-x 0; }
	.me__tab {
		padding: 12rpx 28rpx; border-radius: $r-pill; margin-right: 14rpx;
		background: #fff; box-shadow: $sh-card;
		transition: background 0.2s ease;
	}
	.me__tab--on { background: $g-brand; }
	.me__tab--on .me__tab-t { color: #fff; font-weight: $fw-bold; }
	.me__tab-t { font-size: $fs-caption; color: $t-sub; letter-spacing: 0.3rpx; }

	/* ══════════ 订单卡 ══════════ */
	.me__card {
		margin: 24rpx $page-x 0; padding: 26rpx 28rpx;
		border-radius: $r-lg; background: #fff; box-shadow: $sh-card;
	}
	.me__head { display: flex; align-items: center; justify-content: space-between; }
	.me__type-chip { padding: 8rpx 20rpx; border-radius: $r-pill; background: rgba(128, 92, 250, 0.10); }
	.me__type-t { font-size: $fs-micro; font-weight: $fw-semibold; color: $c-primary; }
	.me__status { display: flex; align-items: center; padding: 6rpx 16rpx; border-radius: $r-pill; }
	.me__status-dot { width: 10rpx; height: 10rpx; border-radius: 50%; margin-right: 8rpx; }
	.me__status-t { font-size: $fs-micro; font-weight: $fw-semibold; letter-spacing: 0.3rpx; }
	.me__status--wait { background: rgba(255, 155, 119, 0.14); }
	.me__status--wait .me__status-dot { background: $c-peach; }
	.me__status--wait .me__status-t { color: $c-peach; }
	.me__status--ongoing { background: rgba(128, 92, 250, 0.10); }
	.me__status--ongoing .me__status-dot { background: $c-primary; }
	.me__status--ongoing .me__status-t { color: $c-primary; }
	.me__status--done { background: rgba(41, 202, 131, 0.12); }
	.me__status--done .me__status-dot { background: $c-mint; }
	.me__status--done .me__status-t { color: $c-mint; }
	.me__status--cancel { background: rgba(232, 97, 84, 0.10); }
	.me__status--cancel .me__status-dot { background: #E86154; }
	.me__status--cancel .me__status-t { color: #E86154; }

	.me__titlerow { display: flex; align-items: baseline; margin-top: 18rpx; }
	.me__title {
		flex: 1; min-width: 0;
		font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink;
		letter-spacing: -0.3rpx; line-height: 1.4;
	}
	.me__reward { font-family: $ff-num; font-size: $fs-h3; font-weight: $fw-bold; color: $c-peach; margin-left: 16rpx; flex-shrink: 0; }
	.me__meta { display: flex; align-items: center; margin-top: 12rpx; }
	.me__meta-ico { width: 24rpx; height: 24rpx; opacity: 0.45; flex-shrink: 0; }
	.me__meta-t { margin-left: 8rpx; font-size: $fs-micro; color: $t-sub; letter-spacing: 0.2rpx; }
	.me__who { flex: 1; font-size: $fs-micro; color: $t-sub; }
	.me__time { font-size: $fs-micro; color: $t-tertiary; }
	.me__foot {
		display: flex; align-items: center; justify-content: flex-end;
		margin-top: 20rpx; padding-top: 20rpx; border-top: 2rpx solid $c-line;
	}
	.me__btn {
		font-size: $fs-caption; font-weight: $fw-semibold;
		color: #fff; background: $g-cta;
		padding: 12rpx 28rpx; border-radius: $r-pill;
		box-shadow: 0 6rpx 16rpx rgba(123, 97, 255, 0.22);
		margin-left: 16rpx;
	}
	.me__btn--ghost { background: rgba(128, 92, 250, 0.08); color: $c-primary; box-shadow: none; }
	.me__btn--danger { background: #FFF0EE; color: #E86154; box-shadow: none; }

	/* ══════════ 空态 ══════════ */
	.me__empty { display: flex; flex-direction: column; align-items: center; padding: 80rpx 0 40rpx; }
	.me__empty-img { width: 300rpx; height: 300rpx; }
	.me__empty-t { margin-top: 12rpx; font-size: $fs-body; font-weight: $fw-semibold; color: $t-sub; letter-spacing: 0.5rpx; }
	.me__empty-sub { margin-top: 10rpx; font-size: $fs-caption; color: $t-tertiary; letter-spacing: 0.3rpx; }
	.me__empty-btn {
		margin-top: 30rpx;
		padding: 18rpx 60rpx;
		border-radius: $r-pill;
		background: $g-cta;
		box-shadow: 0 8rpx 18rpx rgba(123, 97, 255, 0.22);
	}
	.me__empty-btn-t { font-size: $fs-body; font-weight: $fw-bold; color: #fff; letter-spacing: 1rpx; }
</style>
