<template>
	<view class="ad unida-page">
		<!-- ══════════ 沉浸式封面（统一插画，满幅铺底） ══════════ -->
		<view class="ad__cover">
			<image class="ad__cover-img" :src="cover" mode="aspectFill" />
			<view class="ad__cover-shade"></view>

			<!-- 透明浮层导航（无框无投影，白字+深描边保证可读） -->
			<view class="ad__nav" :style="{ paddingTop: statusBar + 'px' }">
				<view class="ad__nav-btn" @click="goBack">
					<image class="ad__nav-ico" src="/static/icons-dark/back.png" mode="aspectFit" />
				</view>
				<text class="ad__nav-title">活动详情</text>
				<view class="ad__nav-btn" @click="onShare">
					<image class="ad__nav-ico" src="/static/icons-dark/bell.png" mode="aspectFit" />
				</view>
			</view>

			<!-- 状态徽章（阳光黄，玻璃质感） -->
			<view class="ad__cover-status">
				<image class="ad__cover-status-ico" src="/static/icons-dark/flame.png" mode="aspectFit" />
				<text class="ad__cover-status-t">报名中</text>
			</view>
		</view>

		<!-- ══════════ 主体信息卡（叠压封面） ══════════ -->
		<view class="ad__main">
			<view class="ad__title-row">
				<text class="ad__title">{{ title || '加载中…' }}</text>
				<view class="ad__fav" @click="onFav">
					<image class="ad__fav-ico" :class="{ 'ad__fav-ico--on': faved }" src="/static/icons-dark/heart.png" mode="aspectFit" />
				</view>
			</view>
			<view class="ad__tags">
				<text class="ad__tag ad__tag--purple">{{ category }}</text>
				<text class="ad__tag ad__tag--orange">热门</text>
				<text class="ad__tag ad__tag--green">{{ price === '免费' ? '免费' : price }}</text>
			</view>

			<!-- 时间 / 地点：线性图标 + 墨紫数值 -->
			<view class="ad__meta">
				<view class="ad__meta-item">
					<view class="ad__meta-ico"><image src="/static/icons-dark/clock.png" mode="aspectFit" /></view>
					<view class="ad__meta-col">
						<text class="ad__meta-label">活动时间</text>
						<text class="ad__meta-value">{{ time || '待定' }}</text>
					</view>
				</view>
				<view class="ad__meta-item">
					<view class="ad__meta-ico"><image src="/static/icons-dark/pin.png" mode="aspectFit" /></view>
					<view class="ad__meta-col">
						<text class="ad__meta-label">活动地点</text>
						<text class="ad__meta-value">{{ place || '待定' }}</text>
					</view>
				</view>
			</view>

			<!-- 报名进度 -->
			<view class="ad__progress">
				<view class="ad__progress-head">
					<text class="ad__progress-t">报名进度</text>
					<text class="ad__progress-n">{{ joined }}<text class="ad__progress-slash"> / </text>{{ total }} 人</text>
				</view>
				<view class="ad__progress-track"><view class="ad__progress-fill" :style="{ width: pct + '%' }"></view></view>
			</view>
		</view>

		<!-- ══════════ 发起人 ══════════ -->
		<view class="ad__card ad__organizer" @click="goUser">
			<view class="ad__org-avatar">林</view>
			<view class="ad__org-info">
				<view class="ad__org-name-row">
					<text class="ad__org-name">音乐社 · 小林</text>
					<view class="ad__org-verified"><image src="/static/icons-dark/buddy.png" mode="aspectFit" /></view>
				</view>
				<text class="ad__org-sub">已认证 · 4.9 分</text>
			</view>
			<image class="ad__org-arrow" src="/static/icons-dark/chevron.png" mode="aspectFit" />
		</view>

		<!-- ══════════ 报名人员（几何头像，无 emoji） ══════════ -->
		<view class="ad__card">
			<view class="ad__subhead">
				<text class="ad__subhead-title">报名人员</text>
				<text class="ad__subhead-more">查看全部 ›</text>
			</view>
			<view class="ad__avatars">
				<view class="ad__avatar" v-for="(a, i) in members" :key="i" :style="{ background: a.bg }">{{ a.ch }}</view>
				<view class="ad__avatar-more">+{{ total - joined }}</view>
				<text class="ad__avatars-tip">已有 {{ joined }} 人加入</text>
			</view>
		</view>

		<!-- ══════════ 活动详情 ══════════ -->
		<view class="ad__card">
			<view class="ad__subhead"><text class="ad__subhead-title">活动详情</text></view>
			<text class="ad__desc-text">一起在草地上听歌、唱歌、认识新朋友！我们准备了音响、吉他和零食，欢迎会乐器或爱唱歌的同学加入，也欢迎来当观众。</text>
			<text class="ad__desc-text">请自带野餐垫，注意防蚊。活动结束后一起收拾场地哦～</text>
		</view>

		<!-- ══════════ 费用说明 ══════════ -->
		<view class="ad__card">
			<view class="ad__subhead"><text class="ad__subhead-title">费用说明</text></view>
			<view class="ad__cost">
				<text class="ad__cost-free">{{ price === '免费' ? '免费参与' : price }}</text>
				<text class="ad__cost-dot">·</text>
				<text class="ad__cost-text">零食饮料 AA（预计 ¥15/人）</text>
			</view>
		</view>

		<!-- ══════════ 底部报名栏 ══════════ -->
		<view class="ad__bottom">
			<view class="ad__bottom-left" @click="onContact">
				<view class="ad__bottom-ico"><image src="/static/icons-dark/message.png" mode="aspectFit" /></view>
				<text class="ad__bottom-label">联系</text>
			</view>
			<view class="ad__bottom-btn" @click="onBooking">立即报名</view>
		</view>
	</view>
</template>

<script>
	import { callCloud, getToken } from '@/common/cloud.js';

	export default {
		data() {
			return {
				statusBar: 0,
				itemId: '',
				title: '',
				cover: '/static/art/art-guitar.jpg',
				time: '',
				place: '',
				price: '免费',
				category: '校园活动',
				faved: false,
				favBusy: false,
				joined: 0,
				total: 50,
				members: [
					{ ch: '陈', bg: 'linear-gradient(135deg,#A98BFF,#805CFA)' },
					{ ch: '李', bg: 'linear-gradient(135deg,#FFC94F,#FF9B77)' },
					{ ch: '王', bg: 'linear-gradient(135deg,#29CA83,#93EDCF)' },
					{ ch: '周', bg: 'linear-gradient(135deg,#69B9F5,#A98BFF)' },
					{ ch: '吴', bg: 'linear-gradient(135deg,#805CFA,#542DAF)' }
				]
			};
		},
		computed: {
			pct() {
				const t = Math.max(1, Number(this.total) || 50);
				return Math.min(100, Math.round((Number(this.joined) || 0) / t * 100));
			}
		},
		onLoad(options) {
			const sys = uni.getSystemInfoSync();
			this.statusBar = (sys && (sys.statusBarHeight || 0)) || 0;
			this.itemId = (options && options.id) || '';
			this.loadDetail();
			this.checkFav();
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onShare() { uni.showToast({ title: '分享功能待接入', icon: 'none' }); },
			goUser() { uni.navigateTo({ url: '/pages/user-home/user-home' }); },
			onContact() { uni.navigateTo({ url: '/pages/chat/chat?peer=official&name=' + encodeURIComponent('UNIDA 小助手') }); },
			onBooking() { uni.navigateTo({ url: '/pages/booking-confirm/booking-confirm?id=' + this.itemId }); },
			async loadDetail() {
				if (!this.itemId) return;
				try {
					const r = await callCloud('itemDetail', { id: this.itemId });
					const it = r.item || {};
					this.title = it.title || '';
					this.cover = it.cover || this.cover;
					this.time = it.time || '';
					this.place = it.place || '';
					this.price = it.price || '免费';
					this.category = it.category || '校园活动';
					this.joined = Number(it.joined) || 0;
					this.total = Number(it.total) || 50;
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '获取详情失败', icon: 'none' });
				}
			},
			async checkFav() {
				if (!this.itemId) return;
				try {
					const r = await callCloud('favorite', {
						action: 'check',
						token: getToken(),
						type: 'item',
						targetId: this.itemId
					});
					this.faved = !!r.faved;
				} catch (e) {}
			},
			async onFav() {
				if (this.favBusy || !this.itemId) return;
				this.favBusy = true;
				try {
					const r = await callCloud('favorite', {
						action: 'toggle',
						token: getToken(),
						type: 'item',
						targetId: this.itemId,
						title: this.title,
						cover: this.cover,
						desc: (this.time + (this.place ? ' · ' + this.place : '')).slice(0, 80)
					});
					this.faved = !!r.faved;
					uni.showToast({ title: r.faved ? '已收藏' : '已取消收藏', icon: 'none' });
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '操作失败', icon: 'none' });
				} finally {
					this.favBusy = false;
				}
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.ad { padding-bottom: 180rpx; }

	/* ══════════ 封面 ══════════ */
	.ad__cover { position: relative; height: 720rpx; overflow: hidden; }
	.ad__cover-img { position: absolute; inset: 0; width: 100%; height: 100%; }
	.ad__cover-shade {
		position: absolute; left: 0; right: 0; bottom: 0; height: 260rpx;
		background: linear-gradient(180deg, rgba(57,0,126,0) 0%, rgba(57,0,126,0.28) 100%);
	}
	/* 透明浮层导航：白字 + 深描边，无框无投影 */
	.ad__nav {
		position: absolute; left: 0; right: 0; top: 0; z-index: 10;
		display: flex; align-items: center; justify-content: space-between;
		padding-left: $page-x; padding-right: $page-x; padding-bottom: 16rpx;
	}
	.ad__nav-btn {
		width: 64rpx; height: 64rpx; border-radius: 50%;
		display: flex; align-items: center; justify-content: center;
	}
	.ad__nav-ico { width: 40rpx; height: 40rpx; filter: brightness(0) invert(1); }
	.ad__nav-title {
		font-size: $fs-h3; font-weight: $fw-bold; color: #fff;
		text-shadow: 0 2rpx 10rpx rgba(57,0,126,0.55); letter-spacing: 0.5rpx;
	}
	.ad__cover-status {
		position: absolute; left: $page-x; bottom: 100rpx;
		display: flex; align-items: center; flex-direction: row;
		padding: 12rpx 26rpx; border-radius: $r-pill;
		background: $g-glass; box-shadow: $sh-float;
	}
	.ad__cover-status-ico { width: 28rpx; height: 28rpx; margin-right: 10rpx; }
	.ad__cover-status-t { font-size: $fs-caption; font-weight: $fw-bold; color: $c-ink; letter-spacing: 0.5rpx; }

	/* ══════════ 主体信息卡（叠压封面） ══════════ */
	.ad__main {
		position: relative; z-index: 5; margin: -76rpx $page-x 0;
		padding: 32rpx 28rpx; border-radius: $r-lg;
		background: #fff; box-shadow: $sh-card;
	}
	.ad__title-row { display: flex; align-items: flex-start; justify-content: space-between; }
	.ad__title {
		flex: 1; font-size: $fs-h2; font-weight: $fw-bold; color: $c-ink;
		line-height: 1.42; letter-spacing: -0.8rpx;
	}
	.ad__fav { width: 56rpx; height: 56rpx; display: flex; align-items: center; justify-content: center; margin-left: 12rpx; }
	.ad__fav-ico { width: 44rpx; height: 44rpx; opacity: 0.45; transition: opacity 0.2s ease; }
	.ad__fav-ico--on { opacity: 1; }
	.ad__tags { display: flex; flex-wrap: wrap; margin-top: 20rpx; }
	.ad__tag {
		font-size: $fs-micro; font-weight: $fw-semibold; letter-spacing: 0.3rpx;
		padding: 8rpx 18rpx; border-radius: $r-pill; margin-right: 12rpx; margin-bottom: 8rpx;
	}
	.ad__tag--purple { color: $c-primary; background: rgba(128,92,250,0.10); }
	.ad__tag--orange { color: $c-peach; background: rgba(255,155,119,0.14); }
	.ad__tag--green { color: $c-mint; background: rgba(41,202,131,0.13); }
	.ad__meta { margin-top: 28rpx; padding-top: 26rpx; border-top: 2rpx solid $c-line; }
	.ad__meta-item { display: flex; align-items: center; margin-bottom: 22rpx; }
	.ad__meta-item:last-child { margin-bottom: 0; }
	.ad__meta-ico {
		width: 64rpx; height: 64rpx; border-radius: 18rpx; flex-shrink: 0;
		background: linear-gradient(150deg, rgba(169,139,255,0.16), rgba(128,92,250,0.08));
		display: flex; align-items: center; justify-content: center; margin-right: 20rpx;
	}
	.ad__meta-ico image { width: 34rpx; height: 34rpx; }
	.ad__meta-col { display: flex; flex-direction: column; }
	.ad__meta-label { font-size: $fs-micro; color: $t-sub; letter-spacing: 0.3rpx; }
	.ad__meta-value { margin-top: 6rpx; font-size: $fs-body; font-weight: $fw-semibold; color: $c-ink; letter-spacing: -0.2rpx; }

	/* 报名进度 */
	.ad__progress { margin-top: 28rpx; padding-top: 26rpx; border-top: 2rpx solid $c-line; }
	.ad__progress-head { display: flex; align-items: baseline; justify-content: space-between; }
	.ad__progress-t { font-size: $fs-caption; color: $t-sub; letter-spacing: 0.3rpx; }
	.ad__progress-n { font-family: $ff-num; font-size: $fs-body; font-weight: $fw-bold; color: $c-primary; }
	.ad__progress-slash { font-size: $fs-micro; color: $t-tertiary; }
	.ad__progress-track { margin-top: 16rpx; height: 12rpx; border-radius: $r-pill; background: $c-line; overflow: hidden; }
	.ad__progress-fill {
		height: 100%; border-radius: $r-pill;
		background: linear-gradient(90deg, $c-purple-light, $c-primary);
		transition: width 0.4s $ease-out;
	}

	/* ══════════ 通用卡片区块 ══════════ */
	.ad__card { margin: 24rpx $page-x 0; padding: 28rpx; border-radius: $r-lg; background: #fff; box-shadow: $sh-card; }
	.ad__subhead { display: flex; align-items: center; justify-content: space-between; margin-bottom: 22rpx; }
	.ad__subhead-title { font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink; letter-spacing: -0.3rpx; }
	.ad__subhead-more { font-size: $fs-caption; color: $t-sub; }

	/* 发起人 */
	.ad__organizer { display: flex; align-items: center; }
	.ad__org-avatar {
		width: 92rpx; height: 92rpx; border-radius: 50%; flex-shrink: 0;
		background: linear-gradient(145deg, #A98BFF, #6C3FF2);
		display: flex; align-items: center; justify-content: center;
		font-size: 36rpx; font-weight: $fw-bold; color: #fff;
		box-shadow: 0 8rpx 20rpx rgba(108,63,242,0.28); margin-right: 20rpx;
	}
	.ad__org-info { flex: 1; display: flex; flex-direction: column; }
	.ad__org-name-row { display: flex; align-items: center; }
	.ad__org-name { font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink; letter-spacing: -0.3rpx; }
	.ad__org-verified {
		width: 30rpx; height: 30rpx; border-radius: 50%; margin-left: 10rpx;
		background: $c-mint; display: flex; align-items: center; justify-content: center;
	}
	.ad__org-verified image { width: 20rpx; height: 20rpx; filter: brightness(0) invert(1); }
	.ad__org-sub { margin-top: 8rpx; font-size: $fs-caption; color: $t-sub; letter-spacing: 0.2rpx; }
	.ad__org-arrow { width: 32rpx; height: 32rpx; opacity: 0.4; }

	/* 报名人员 */
	.ad__avatars { display: flex; align-items: center; }
	.ad__avatar {
		width: 68rpx; height: 68rpx; border-radius: 50%;
		display: flex; align-items: center; justify-content: center;
		font-size: 26rpx; font-weight: $fw-bold; color: #fff;
		border: 4rpx solid #fff; margin-right: -16rpx;
	}
	.ad__avatar-more {
		width: 68rpx; height: 68rpx; border-radius: 50%; flex-shrink: 0;
		display: flex; align-items: center; justify-content: center;
		font-family: $ff-num; font-size: 24rpx; font-weight: $fw-bold; color: $c-primary;
		background: rgba(128,92,250,0.10); border: 4rpx solid #fff; margin-left: 20rpx;
	}
	.ad__avatars-tip { margin-left: auto; font-size: $fs-micro; color: $t-tertiary; }

	/* 详情 / 费用 */
	.ad__desc-text { display: block; font-size: $fs-body; color: $t-main; line-height: 1.78; margin-bottom: 14rpx; letter-spacing: 0.2rpx; }
	.ad__desc-text:last-child { margin-bottom: 0; }
	.ad__cost { display: flex; align-items: center; }
	.ad__cost-free { font-size: $fs-body; font-weight: $fw-bold; color: $c-mint; }
	.ad__cost-dot { margin: 0 12rpx; color: $t-tertiary; }
	.ad__cost-text { font-size: $fs-body; color: $t-main; }

	/* ══════════ 底部报名栏 ══════════ */
	.ad__bottom {
		position: fixed; left: 0; right: 0; bottom: 0; z-index: 60;
		display: flex; align-items: center; padding: 18rpx $page-x;
		padding-bottom: calc(18rpx + env(safe-area-inset-bottom));
		background: rgba(255,255,255,0.96); box-shadow: 0 -6rpx 24rpx rgba(123,97,255,0.08);
	}
	.ad__bottom-left { width: 110rpx; display: flex; flex-direction: column; align-items: center; }
	.ad__bottom-ico {
		width: 64rpx; height: 64rpx; border-radius: 50%;
		background: rgba(128,92,250,0.10); display: flex; align-items: center; justify-content: center;
	}
	.ad__bottom-ico image { width: 36rpx; height: 36rpx; }
	.ad__bottom-label { margin-top: 6rpx; font-size: $fs-micro; color: $t-sub; }
	.ad__bottom-btn {
		flex: 1; height: 92rpx; border-radius: $r-pill;
		background: $g-cta; box-shadow: $sh-float;
		display: flex; align-items: center; justify-content: center;
		font-size: $fs-h3; font-weight: $fw-bold; color: #fff; letter-spacing: 2rpx;
	}
	.ad__bottom-btn:active { opacity: 0.9; }
</style>
