<template>
	<view class="nt unida-page">
		<!-- ══════════ 自绘顶栏 ══════════ -->
		<view class="nt__nav" :style="{ paddingTop: statusBar + 'px' }">
			<view class="nt__nav-btn" @click="goBack">
				<image class="nt__nav-ico" src="/static/icons-dark/back.png" mode="aspectFit" />
			</view>
			<text class="nt__nav-title">消息中心</text>
			<text class="nt__readall" @click="onReadAll">全部已读</text>
		</view>

		<!-- ══════════ 分类入口卡 ══════════ -->
		<view class="nt__cats">
			<view class="nt__cat" v-for="(c, i) in cats" :key="c.key" @click="onCat(i)">
				<view class="nt__cat-ico" :class="'nt__cat-ico--' + c.key">
					<image class="nt__cat-img" :src="c.icon" mode="aspectFit" />
					<view class="nt__cat-badge" v-if="counts[c.key] > 0"><text class="nt__cat-badge-t">{{ counts[c.key] > 9 ? '9+' : counts[c.key] }}</text></view>
				</view>
				<text class="nt__cat-label">{{ c.label }}</text>
			</view>
		</view>

		<!-- ══════════ 通知列表 ══════════ -->
		<view class="nt__list">
			<view class="nt__item" v-for="(n, i) in listShow" :key="n.id" :class="{ 'nt__item--unread': !n.read }" @click="onOpen(i)">
				<view class="nt__ico" :class="'nt__ico--' + n.type">
					<image class="nt__ico-img" :src="iconOf(n.type)" mode="aspectFit" />
				</view>
				<view class="nt__body">
					<view class="nt__row">
						<text class="nt__title">{{ n.title }}</text>
						<text class="nt__time">{{ n.time }}</text>
					</view>
					<text class="nt__text">{{ n.text }}</text>
				</view>
				<view class="nt__dot" v-if="!n.read"></view>
			</view>

			<view class="nt__empty" v-if="!loading && listShow.length === 0">
				<text class="nt__empty-t">暂无通知</text>
			</view>
		</view>
	</view>
</template>

<script>
	import { callCloud, getToken } from '@/common/cloud.js';

	export default {
		data() {
			return {
				statusBar: 0,
				loading: false,
				active: 'all',
				cats: [
					{ key: 'system', label: '系统通知', icon: '/static/icons-dark/bell.png' },
					{ key: 'activity', label: '活动通知', icon: '/static/icons-dark/calendar.png' },
					{ key: 'order', label: '订单通知', icon: '/static/icons-dark/box.png' },
					{ key: 'booking', label: '预约通知', icon: '/static/icons-dark/clock.png' },
					{ key: 'interact', label: '互动消息', icon: '/static/icons-dark/message.png' }
				],
				counts: { system: 0, activity: 0, order: 0, booking: 0, interact: 0 },
				list: []
			};
		},
		computed: {
			listShow() {
				if (this.active === 'all') return this.list;
				return this.list.filter((x) => x.type === this.active);
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
			iconOf(type) {
				const c = this.cats.find((x) => x.key === type);
				return c ? c.icon : '/static/icons-dark/bell.png';
			},
			onCat(i) {
				this.active = this.active === this.cats[i].key ? 'all' : this.cats[i].key;
			},
			async loadList() {
				if (this.loading) return;
				this.loading = true;
				try {
					const r = await callCloud('notify', { action: 'list', token: getToken() });
					this.list = r.list || [];
					this.counts = r.counts || this.counts;
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '加载通知失败', icon: 'none' });
				} finally {
					this.loading = false;
				}
			},
			async onOpen(i) {
				const n = this.listShow[i];
				if (!n) return;
				try {
					if (!n.read) await callCloud('notify', { action: 'read', token: getToken(), id: n.id });
				} catch (e) {}
				if (n.link) {
					uni.navigateTo({ url: n.link });
				} else {
					this.loadList();
				}
			},
			async onReadAll() {
				try {
					await callCloud('notify', { action: 'read', token: getToken() });
					this.loadList();
					uni.showToast({ title: '已全部标记为已读', icon: 'none' });
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '操作失败', icon: 'none' });
				}
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.nt { padding-bottom: calc(60rpx + env(safe-area-inset-bottom)); }

	/* ══════════ 顶栏 ══════════ */
	.nt__nav {
		display: flex; align-items: center; justify-content: space-between;
		padding-left: $page-x; padding-right: $page-x; padding-bottom: 16rpx;
	}
	.nt__nav-btn { width: 64rpx; height: 64rpx; display: flex; align-items: center; justify-content: center; }
	.nt__nav-ico { width: 40rpx; height: 40rpx; }
	.nt__nav-title { font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink; letter-spacing: 0.5rpx; }
	.nt__readall { font-size: $fs-caption; color: $c-primary; font-weight: $fw-semibold; }

	/* ══════════ 分类入口 ══════════ */
	.nt__cats {
		display: flex; align-items: center;
		margin: 8rpx $page-x 0; padding: 26rpx 10rpx;
		border-radius: $r-lg; background: #fff; box-shadow: $sh-card;
	}
	.nt__cat { flex: 1; display: flex; flex-direction: column; align-items: center; }
	.nt__cat-ico {
		position: relative;
		width: 84rpx; height: 84rpx;
		border-radius: 26rpx;
		background: rgba(128, 92, 250, 0.10);
		display: flex; align-items: center; justify-content: center;
	}
	.nt__cat-ico--system { background: rgba(128, 92, 250, 0.12); }
	.nt__cat-ico--activity { background: rgba(255, 155, 119, 0.16); }
	.nt__cat-ico--order { background: rgba(255, 201, 79, 0.18); }
	.nt__cat-ico--booking { background: rgba(41, 202, 131, 0.14); }
	.nt__cat-ico--interact { background: rgba(105, 185, 245, 0.16); }
	.nt__cat-img { width: 44rpx; height: 44rpx; }
	.nt__cat-badge {
		position: absolute; right: -10rpx; top: -10rpx;
		min-width: 34rpx; height: 34rpx;
		box-sizing: border-box;
		padding: 0 8rpx;
		background: #FF5A4E;
		border-radius: $r-pill;
		border: 3rpx solid #fff;
		display: flex; align-items: center; justify-content: center;
	}
	.nt__cat-badge-t { font-size: 18rpx; color: #fff; font-weight: 700; font-family: $ff-num; }
	.nt__cat-label { margin-top: 12rpx; font-size: $fs-micro; color: $t-sub; }

	/* ══════════ 通知列表 ══════════ */
	.nt__list { margin: 20rpx $page-x 0; }
	.nt__item {
		display: flex; align-items: flex-start;
		background: #fff; border-radius: $r-md; box-shadow: $sh-card;
		padding: 26rpx 24rpx;
		margin-top: 16rpx;
		opacity: 0.82;
	}
	.nt__item--unread { opacity: 1; }
	.nt__ico {
		width: 76rpx; height: 76rpx;
		border-radius: 24rpx;
		background: rgba(128, 92, 250, 0.12);
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.nt__ico--order { background: rgba(255, 201, 79, 0.20); }
	.nt__ico--activity, .nt__ico--booking { background: rgba(255, 155, 119, 0.16); }
	.nt__ico--interact { background: rgba(105, 185, 245, 0.18); }
	.nt__ico-img { width: 40rpx; height: 40rpx; }
	.nt__body { flex: 1; min-width: 0; margin: 0 12rpx 0 20rpx; }
	.nt__row { display: flex; align-items: baseline; }
	.nt__title { font-size: $fs-body; font-weight: $fw-bold; color: $c-ink; flex: 1; min-width: 0; }
	.nt__time { font-size: $fs-micro; color: $t-tertiary; flex-shrink: 0; margin-left: 12rpx; }
	.nt__text { display: block; margin-top: 8rpx; font-size: $fs-caption; color: $t-sub; line-height: 1.55; }
	.nt__dot { width: 14rpx; height: 14rpx; border-radius: 50%; background: #FF5A4E; flex-shrink: 0; margin-top: 14rpx; }

	.nt__empty { display: flex; justify-content: center; padding: 100rpx 0; }
	.nt__empty-t { font-size: $fs-caption; color: $t-tertiary; }
</style>
