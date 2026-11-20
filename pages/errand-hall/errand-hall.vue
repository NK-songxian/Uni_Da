<template>
	<view class="eh unida-page unida-page--tab">
		<view class="eh__safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 顶栏 -->
		<view class="eh__top">
			<text class="eh__title">跑腿大厅</text>
			<unida-search placeholder="搜索跑腿需求（快递、外卖…）" @focus="onSearch" />
		</view>

		<!-- 快捷分类 -->
		<view class="eh__cats">
			<view class="eh__cat" v-for="(c, i) in cats" :key="i" @click="onCat(i)">
				<view class="eh__cat-icon" :class="'eh__cat-icon--' + c.tone">
					<image class="eh__cat-img" :src="c.icon" mode="aspectFit" />
				</view>
				<text class="eh__cat-label">{{ c.label }}</text>
			</view>
		</view>

		<!-- 发布跑腿 CTA -->
		<view class="eh__cta" @click="onPublish">
			<view class="eh__cta-info">
				<text class="eh__cta-title">需要帮忙？发布跑腿需求</text>
				<text class="eh__cta-sub">同学接单，快速搞定</text>
			</view>
			<image class="eh__cta-img" src="/static/unida/bubbles/catering-pin.webp" mode="aspectFit" />
			<view class="eh__cta-btn"><text class="eh__cta-btn-t">去发布</text></view>
		</view>

		<!-- 需求列表 -->
		<view class="eh__sect">
			<text class="eh__sect-t">附近需求</text>
			<text class="eh__sect-s">{{ orders.length }} 个待接单</text>
		</view>
		<view class="eh__item" v-for="(o, i) in orders" :key="i" @click="onOrder(i)">
			<view class="eh__item-head">
				<view class="eh__item-type"><text class="eh__item-type-t">{{ o.type }}</text></view>
				<view class="eh__item-reward"><text class="eh__item-reward-s">¥</text><text class="eh__item-reward-n">{{ o.reward }}</text></view>
			</view>
			<text class="eh__item-title">{{ o.title }}</text>
			<view class="eh__item-meta">
				<view class="eh__item-meta-row"><image class="eh__meta-ico" src="/static/icons-dark/pin.png" mode="aspectFit" /><text class="eh__meta-t">{{ o.from }} → {{ o.to }}</text></view>
				<view class="eh__item-meta-row"><image class="eh__meta-ico" src="/static/icons-dark/clock.png" mode="aspectFit" /><text class="eh__meta-t">{{ o.time }}</text></view>
			</view>
			<view class="eh__item-foot">
				<view class="eh__item-user">
					<view class="eh__item-avatar" :class="'eh__item-avatar--' + o.tone"><text class="eh__item-avatar-ch">{{ o.user[0] }}</text></view>
					<text class="eh__item-user-t">{{ o.user }} · {{ o.dorm }}</text>
				</view>
				<view class="eh__item-btn"><text class="eh__item-btn-t">立即接单</text></view>
			</view>
		</view>

		<view class="eh__bottom-space"></view>
		<unida-tabbar :current="1" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';
	import unidaSearch from '@/components/unida-search/unida-search.vue';

	export default {
		components: { unidaTabbar, unidaSearch },
		data() {
			return {
				statusBar: 0,
				cats: [
					{ label: '快递代取', icon: '/static/icons-dark/box.png', tone: 'purple' },
					{ label: '外卖代拿', icon: '/static/unida/bubbles/mini-food.webp', tone: 'orange' },
					{ label: '物品代送', icon: '/static/unida/bubbles/mark-purple.webp', tone: 'pink' },
					{ label: '其他互助', icon: '/static/icons-dark/buddy.png', tone: 'green' }
				],
				orders: [
					{ type: '快递代取', reward: '8', title: '帮忙取个快递（中通北区驿站）', from: '北区驿站', to: '东园3栋', time: '今天 18:00 前', user: '阿星', dorm: '东园3栋', tone: 'a' },
					{ type: '外卖代拿', reward: '5', title: '一楼拿外卖送到宿舍楼下', from: '东门', to: '西园1栋', time: '现在', user: '小林', dorm: '西园1栋', tone: 'b' },
					{ type: '物品代送', reward: '12', title: '帮忙送一份资料到教学楼', from: '图书馆', to: '3教201', time: '明天 8:00', user: 'Leo', dorm: '南园5栋', tone: 'c' }
				]
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			onSearch() { uni.showToast({ title: '搜索待接入', icon: 'none' }); },
			onCat(i) { uni.showToast({ title: this.cats[i].label + '分类', icon: 'none' }); },
			onPublish() { uni.navigateTo({ url: '/pages/publish/publish' }); },
			onOrder(i) { uni.navigateTo({ url: '/pages/errand-detail/errand-detail' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.eh { min-height: 100vh; }

	/* ---------- 顶栏 ---------- */
	.eh__top { padding: 24rpx $page-x 0; }
	.eh__title { display: block; font-size: 44rpx; font-weight: 800; color: $c-ink; margin-bottom: 24rpx; }

	/* ---------- 快捷分类 ---------- */
	.eh__cats { display: flex; margin-top: 30rpx; }
	.eh__cat { flex: 1; display: flex; flex-direction: column; align-items: center; }
	.eh__cat-icon {
		width: 96rpx; height: 96rpx;
		border-radius: 30rpx;
		display: flex; align-items: center; justify-content: center;
	}
	.eh__cat-icon--purple { background: rgba(128, 92, 250, 0.13); }
	.eh__cat-icon--orange { background: rgba(255, 155, 119, 0.16); }
	.eh__cat-icon--pink { background: rgba(244, 114, 182, 0.14); }
	.eh__cat-icon--green { background: rgba(41, 202, 131, 0.14); }
	.eh__cat-img { width: 46rpx; height: 46rpx; }
	.eh__cat-label { margin-top: 14rpx; font-size: 23rpx; color: $t-main; }

	/* ---------- 发布 CTA ---------- */
	.eh__cta {
		display: flex; align-items: center;
		margin: 32rpx $page-x 0;
		padding: 24rpx 26rpx;
		background: $g-brand;
		border-radius: $r-md;
		box-shadow: $sh-float;
	}
	.eh__cta-info { flex: 1; display: flex; flex-direction: column; }
	.eh__cta-title { font-size: 28rpx; font-weight: 700; color: $c-white; }
	.eh__cta-sub { margin-top: 8rpx; font-size: 21rpx; color: rgba(255, 255, 255, 0.85); }
	.eh__cta-img { width: 96rpx; height: 96rpx; margin-right: 8rpx; }
	.eh__cta-btn {
		background: rgba(255, 255, 255, 0.25);
		border-radius: $r-pill;
		padding: 14rpx 26rpx;
		flex-shrink: 0;
	}
	.eh__cta-btn-t { font-size: 24rpx; color: $c-white; font-weight: 600; }

	/* ---------- 需求列表 ---------- */
	.eh__sect { display: flex; align-items: baseline; margin: 36rpx $page-x 0; }
	.eh__sect-t { font-size: 32rpx; font-weight: 800; color: $c-ink; }
	.eh__sect-s { margin-left: auto; font-size: 22rpx; color: $t-tertiary; font-family: $ff-num; }
	.eh__item {
		margin: 16rpx $page-x 0;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 26rpx;
	}
	.eh__item-head { display: flex; align-items: center; justify-content: space-between; }
	.eh__item-type { background: rgba(128, 92, 250, 0.1); border-radius: $r-pill; padding: 8rpx 20rpx; }
	.eh__item-type-t { font-size: 21rpx; color: $c-primary; font-weight: 600; }
	.eh__item-reward { display: flex; align-items: baseline; }
	.eh__item-reward-s { font-family: $ff-num; font-size: 24rpx; color: $c-peach; font-weight: 700; }
	.eh__item-reward-n { font-family: $ff-num; font-size: 44rpx; color: $c-peach; font-weight: 800; margin-left: 2rpx; }
	.eh__item-title { display: block; margin-top: 16rpx; font-size: 29rpx; font-weight: 700; color: $t-main; }
	.eh__item-meta { margin-top: 16rpx; }
	.eh__item-meta-row { display: flex; align-items: center; margin-top: 10rpx; }
	.eh__meta-ico { width: 26rpx; height: 26rpx; opacity: 0.55; }
	.eh__meta-t { margin-left: 10rpx; font-size: 23rpx; color: $t-sub; }
	.eh__item-foot {
		display: flex; align-items: center; justify-content: space-between;
		margin-top: 22rpx; padding-top: 20rpx;
		border-top: 2rpx solid $c-line;
	}
	.eh__item-user { display: flex; align-items: center; }
	.eh__item-avatar {
		width: 52rpx; height: 52rpx;
		border-radius: 50%;
		display: flex; align-items: center; justify-content: center;
	}
	.eh__item-avatar--a { background: $g-brand; }
	.eh__item-avatar--b { background: linear-gradient(160deg, #FF9B77, #FFC94F); }
	.eh__item-avatar--c { background: linear-gradient(160deg, #69B9F5, #29CA83); }
	.eh__item-avatar-ch { font-size: 24rpx; font-weight: 800; color: $c-white; }
	.eh__item-user-t { margin-left: 12rpx; font-size: 23rpx; color: $t-sub; }
	.eh__item-btn {
		background: $g-cta;
		border-radius: $r-pill;
		padding: 14rpx 30rpx;
	}
	.eh__item-btn-t { font-size: 24rpx; color: $c-white; font-weight: 600; }

	.eh__bottom-space { height: 200rpx; }
</style>
