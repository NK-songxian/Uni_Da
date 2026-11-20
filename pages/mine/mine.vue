<template>
	<view class="mn">
		<view class="mn__safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 个人名片卡（UNIDA 元素整卡，置顶） -->
		<view class="mn__hero">
			<image class="mn__hero-img" src="/static/unida/mine/hero-card.webp" mode="widthFix" />
			<view class="mn__tap mn__tap--edit" @click="onEdit"></view>
			<view class="mn__tap mn__tap--s1" data-stat="0" @click="onStatTap"></view>
			<view class="mn__tap mn__tap--s2" data-stat="1" @click="onStatTap"></view>
			<view class="mn__tap mn__tap--s3" data-stat="2" @click="onStatTap"></view>
			<view class="mn__tap mn__tap--s4" data-stat="3" @click="onStatTap"></view>
		</view>

		<!-- 我的校园生活 -->
		<view class="mn__card">
			<view class="mn__cardhead">
				<view class="mn__cardtitle">
					<text class="mn__ct">我的校园生活</text>
					<view class="mn__uline"></view>
				</view>
				<text class="mn__cardsub">一站式管理我的校园体验</text>
			</view>
			<view class="mn__liferow">
				<view class="mn__life" v-for="(it, i) in lifeItems" :key="i" @click="onLife(i)">
					<image class="mn__life-ico" :src="it.icon" mode="aspectFit" />
					<text class="mn__life-t">{{ it.label }}</text>
				</view>
			</view>
		</view>

		<!-- 我的小组件 -->
		<view class="mn__sect">
			<view class="mn__sect-l">
				<view class="mn__spark mn__spark--a"></view>
				<view class="mn__spark mn__spark--b"></view>
				<text class="mn__sect-t">我的小组件</text>
				<text class="mn__sect-sub">我的成长 · 我的节奏 · 我的小宇宙</text>
			</view>
			<view class="mn__manage" @click="onManage">管理组件</view>
		</view>
		<view class="mn__grid">
			<!-- 本周目标 -->
			<view class="mn__widget" @click="onGoal">
				<view class="mn__whead">
					<view class="mn__wbadge"><image class="mn__wbadge-ico" src="/static/icons-dark/flame.png" mode="aspectFit" /></view>
					<text class="mn__wt">本周目标</text>
					<image class="mn__chev" src="/static/icons-dark/chevron.png" mode="aspectFit" />
				</view>
				<view class="mn__wbody">
					<view class="mn__wmain">
						<view class="mn__goalnum"><text class="mn__goal-big">3</text><text class="mn__goal-sub">/5</text><text class="mn__goal-tip">项已完成</text></view>
						<view class="mn__bar"><view class="mn__bar-fill mn__bar-fill--60"></view></view>
					</view>
					<image class="mn__wdeco mn__wdeco--clip" src="/static/unida/mine/w-clip.png" mode="aspectFit" />
				</view>
			</view>
			<!-- 连续签到 -->
			<view class="mn__widget" @click="onCheckin">
				<view class="mn__whead">
					<view class="mn__wbadge"><image class="mn__wbadge-ico" src="/static/icons-dark/calendar.png" mode="aspectFit" /></view>
					<text class="mn__wt">连续签到</text>
					<image class="mn__chev" src="/static/icons-dark/chevron.png" mode="aspectFit" />
				</view>
				<view class="mn__wbody">
					<view class="mn__wmain">
						<view class="mn__streak"><text class="mn__streak-big">7</text><text class="mn__streak-day">天</text></view>
						<text class="mn__streak-tip">再签 3 天得成长徽章！</text>
					</view>
					<image class="mn__wdeco mn__wdeco--mascot" src="/static/unida/mine/w-mascot.png" mode="aspectFit" />
				</view>
			</view>
			<!-- 活动日历 -->
			<view class="mn__widget" @click="onCal">
				<view class="mn__whead">
					<view class="mn__wbadge"><image class="mn__wbadge-ico" src="/static/icons-dark/clock.png" mode="aspectFit" /></view>
					<text class="mn__wt">活动日历</text>
					<view class="mn__mon"><text class="mn__mon-t">1月</text></view>
					<image class="mn__chev" src="/static/icons-dark/chevron.png" mode="aspectFit" />
				</view>
				<view class="mn__wbody">
					<view class="mn__cal">
						<view class="mn__cal-week"><text v-for="(w, i) in weekHead" :key="i" class="mn__cal-w">{{ w }}</text></view>
						<view class="mn__cal-dates">
							<view v-for="(d, i) in dateArr" :key="i" class="mn__cal-cell" :class="{ 'mn__cal-cell--on': d === 22 }">
								<text class="mn__cal-d">{{ d }}</text>
								<view class="mn__cal-dots" v-if="d === 22"><view class="mn__dot mn__dot--y"></view><view class="mn__dot mn__dot--p"></view></view>
							</view>
						</view>
					</view>
					<image class="mn__wdeco mn__wdeco--cal" src="/static/unida/mine/w-cal.png" mode="aspectFit" />
				</view>
			</view>
			<!-- 成长徽章 -->
			<view class="mn__widget" @click="onBadge">
				<view class="mn__whead">
					<view class="mn__wbadge"><image class="mn__wbadge-ico" src="/static/icons-dark/heart.png" mode="aspectFit" /></view>
					<text class="mn__wt">成长徽章</text>
					<image class="mn__chev" src="/static/icons-dark/chevron.png" mode="aspectFit" />
				</view>
				<view class="mn__wbody">
					<view class="mn__wmain">
						<view class="mn__lvrow"><text class="mn__lv">Lv.4</text><text class="mn__lv-name">活跃成长者</text></view>
						<view class="mn__bar"><view class="mn__bar-fill mn__bar-fill--68"></view></view>
						<view class="mn__growth"><text class="mn__growth-l">成长值</text><text class="mn__growth-v">680</text><text class="mn__growth-s">/ 1,000</text></view>
					</view>
					<image class="mn__wdeco mn__wdeco--badge" src="/static/unida/mine/w-badge.png" mode="aspectFit" />
				</view>
			</view>
		</view>

		<!-- 快捷列表 -->
		<view class="mn__card mn__list">
			<view class="mn__lrow" v-for="(r, i) in listRows" :key="i" @click="onListRow(i)">
				<image class="mn__lrow-ico" :src="r.icon" mode="aspectFit" />
				<text class="mn__lrow-t">{{ r.label }}</text>
				<view class="mn__count"><text class="mn__count-n">{{ r.count }}</text></view>
				<image class="mn__chev mn__chev--row" src="/static/icons-dark/chevron.png" mode="aspectFit" />
			</view>
		</view>

		<!-- 设置 -->
		<view class="mn__card mn__list">
			<view class="mn__lrow" v-for="(r, i) in setRows" :key="i" @click="onSetRow(i)">
				<image class="mn__lrow-ico" :src="r.icon" mode="aspectFit" />
				<text class="mn__lrow-t">{{ r.label }}</text>
				<image class="mn__chev mn__chev--row" src="/static/icons-dark/chevron.png" mode="aspectFit" />
			</view>
		</view>

		<view class="mn__bottom-space"></view>
		<unida-tabbar :current="4" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';

	export default {
		components: { unidaTabbar },
		data() {
			return {
				statusBar: 0,
				lifeItems: [
					{ icon: '/static/unida/mine/life-act.png', label: '我的活动' },
					{ icon: '/static/unida/mine/life-team.png', label: '我的组队' },
					{ icon: '/static/unida/mine/life-fav.png', label: '我的收藏' },
					{ icon: '/static/unida/mine/life-pub.png', label: '我的发布' },
					{ icon: '/static/unida/mine/life-sign.png', label: '我的报名' }
				],
				weekHead: ['一', '二', '三', '四', '五', '六', '日'],
				dateArr: [20, 21, 22, 23, 24, 25, 26],
				listRows: [
					{ icon: '/static/unida/mine/row-pub.png', label: '我的发布', count: 36 },
					{ icon: '/static/unida/mine/row-buddy.png', label: '我的搭子', count: 128 },
					{ icon: '/static/unida/mine/row-fav.png', label: '我的收藏', count: 42 },
					{ icon: '/static/unida/mine/row-order.png', label: '我的报名', count: 12 }
				],
				setRows: [
					{ icon: '/static/unida/mine/row-set.png', label: '设置' },
					{ icon: '/static/unida/mine/row-help.png', label: '帮助与反馈' }
				]
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			onToast(name) { uni.showToast({ title: name + '待开发', icon: 'none' }); },
			onEdit() { uni.showToast({ title: '编辑资料待开发', icon: 'none' }); },
			onStatTap(e) {
				const i = Number(e.currentTarget.dataset.stat);
				const map = ['我的发布', '我的搭子', '关注', '粉丝'];
				uni.showToast({ title: map[i] + '待开发', icon: 'none' });
			},
			onLife(i) {
				if (i === 0 || i === 4) { uni.navigateTo({ url: '/pages/my-orders/my-orders' }); return; }
				this.onToast(this.lifeItems[i].label);
			},
			onListRow(i) {
				if (i === 3) { uni.navigateTo({ url: '/pages/my-orders/my-orders' }); return; }
				this.onToast(this.listRows[i].label);
			},
			onSetRow(i) { this.onToast(this.setRows[i].label); },
			onCheckin() { uni.showToast({ title: '签到日历待开发', icon: 'none' }); },
			onGoal() { this.onToast('本周目标'); },
			onCal() { this.onToast('活动日历'); },
			onBadge() { this.onToast('成长徽章'); },
			onManage() { this.onToast('组件管理'); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.mn { min-height: 100vh; background: $c-mist; }

	/* ---------- 头部 ---------- */
	.mn__hero { position: relative; width: 706rpx; margin: 20rpx auto 0; }
	.mn__hero-img { display: block; width: 706rpx; height: 322rpx; }
	.mn__tap { position: absolute; }
	.mn__tap--edit { left: 76%; top: 37%; width: 23%; height: 13%; }
	.mn__tap--s1 { left: 3%; top: 60%; width: 23%; height: 26%; }
	.mn__tap--s2 { left: 27%; top: 60%; width: 23%; height: 26%; }
	.mn__tap--s3 { left: 51%; top: 60%; width: 23%; height: 26%; }
	.mn__tap--s4 { left: 75%; top: 60%; width: 23%; height: 26%; }

	/* ---------- 通用卡片 ---------- */
	.mn__card {
		margin: 24rpx $page-x 0;
		background: $c-white;
		border-radius: $r-lg;
		box-shadow: $sh-card;
		padding: 28rpx 28rpx;
	}
	.mn__cardhead { display: flex; align-items: flex-end; justify-content: space-between; }
	.mn__cardtitle { position: relative; }
	.mn__ct { font-size: 34rpx; font-weight: 800; color: $t-main; }
	.mn__uline {
		position: absolute; left: 2rpx; bottom: -8rpx;
		width: 88rpx; height: 10rpx; border-radius: $r-pill;
		background: $c-ice; opacity: 0.9;
	}
	.mn__cardsub { font-size: 20rpx; color: $t-tertiary; letter-spacing: 2rpx; white-space: nowrap; }

	/* ---------- 我的校园生活 ---------- */
	.mn__liferow { display: flex; margin-top: 34rpx; }
	.mn__life { flex: 1; display: flex; flex-direction: column; align-items: center; }
	.mn__life-ico { width: 72rpx; height: 70rpx; }
	.mn__life-t { margin-top: 14rpx; font-size: 24rpx; color: $t-main; font-weight: 500; }

	/* ---------- 小组件标题行 ---------- */
	.mn__sect { display: flex; align-items: center; margin: 36rpx $page-x 0; position: relative; }
	.mn__sect-l { display: flex; align-items: baseline; position: relative; }
	.mn__spark {
		position: absolute; border-radius: 3rpx;
	}
	.mn__spark--a { left: -20rpx; top: -14rpx; width: 14rpx; height: 14rpx; background: $c-sun; transform: rotate(45deg); }
	.mn__spark--b { left: -30rpx; top: 4rpx; width: 8rpx; height: 8rpx; background: $c-primary; transform: rotate(45deg); opacity: 0.7; }
	.mn__sect-t { font-size: 34rpx; font-weight: 800; color: $c-ink; white-space: nowrap; }
	.mn__sect-sub { margin-left: 14rpx; font-size: 20rpx; color: $t-tertiary; letter-spacing: 1rpx; white-space: nowrap; }
	.mn__manage {
		margin-left: auto;
		padding: 12rpx 22rpx;
		background: $g-cta;
		border-radius: $r-pill;
		color: $c-white;
		font-size: 22rpx;
		font-weight: 600;
		letter-spacing: 1rpx;
		white-space: nowrap;
		box-shadow: $sh-float;
	}

	/* ---------- 小组件网格 ---------- */
	.mn__grid { display: flex; flex-wrap: wrap; justify-content: space-between; margin: 20rpx $page-x 0; }
	.mn__widget {
		width: 335rpx;
		box-sizing: border-box;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 24rpx 24rpx 20rpx;
		margin-bottom: 16rpx;
	}
	.mn__whead { display: flex; align-items: center; }
	.mn__wbadge {
		width: 44rpx; height: 44rpx; border-radius: 14rpx;
		background: rgba(128, 92, 250, 0.12);
		display: flex; align-items: center; justify-content: center;
	}
	.mn__wbadge-ico { width: 26rpx; height: 26rpx; }
	.mn__wt { margin-left: 12rpx; font-size: 26rpx; font-weight: 700; color: $t-main; flex: 1; }
	.mn__mon { margin-right: 8rpx; }
	.mn__mon-t { font-size: 22rpx; color: $t-sub; font-family: $ff-num; font-weight: 600; }
	.mn__chev { width: 24rpx; height: 24rpx; opacity: 0.5; }
	.mn__wbody { display: flex; align-items: flex-end; margin-top: 20rpx; position: relative; }
	.mn__wmain { flex: 1; min-width: 0; }

	.mn__goalnum { display: flex; align-items: baseline; }
	.mn__goal-big { font-family: $ff-num; font-size: 56rpx; font-weight: 800; color: $c-ink; }
	.mn__goal-sub { font-family: $ff-num; font-size: 28rpx; color: $t-sub; margin-left: 2rpx; }
	.mn__goal-tip { margin-left: 14rpx; font-size: 22rpx; color: $t-sub; }
	.mn__bar { margin-top: 18rpx; height: 14rpx; border-radius: $r-pill; background: $c-ice; overflow: hidden; }
	.mn__bar-fill { height: 100%; border-radius: $r-pill; background: $g-brand; }
	.mn__bar-fill--60 { width: 60%; }
	.mn__bar-fill--68 { width: 68%; }
	.mn__wdeco--clip { width: 104rpx; height: 118rpx; margin-left: 6rpx; }

	.mn__streak { display: flex; align-items: baseline; }
	.mn__streak-big { font-family: $ff-num; font-size: 56rpx; font-weight: 800; color: $c-ink; }
	.mn__streak-day { font-size: 26rpx; color: $t-main; font-weight: 600; margin-left: 6rpx; }
	.mn__streak-tip { display: block; margin-top: 14rpx; font-size: 19rpx; color: $c-peach; font-weight: 600; white-space: nowrap; }
	.mn__wdeco--mascot { width: 100rpx; height: 106rpx; margin-left: 4rpx; flex-shrink: 0; }

	.mn__cal { flex: 1; min-width: 0; }
	.mn__cal-week { display: flex; justify-content: space-between; }
	.mn__cal-w { width: 26rpx; flex-shrink: 0; text-align: center; font-size: 19rpx; color: $t-tertiary; }
	.mn__cal-dates { display: flex; justify-content: space-between; margin-top: 10rpx; }
	.mn__cal-cell { width: 26rpx; height: 42rpx; flex-shrink: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
	.mn__cal-cell--on { background: $g-cta; border-radius: 10rpx; }
	.mn__cal-d { font-size: 20rpx; color: $t-main; font-family: $ff-num; }
	.mn__cal-cell--on .mn__cal-d { color: $c-white; font-weight: 700; }
	.mn__cal-dots { display: flex; margin-top: 3rpx; }
	.mn__dot { width: 8rpx; height: 8rpx; border-radius: 50%; margin: 0 2rpx; }
	.mn__dot--y { background: $c-sun; }
	.mn__dot--p { background: $c-purple-light; }
	.mn__wdeco--cal { width: 84rpx; height: 84rpx; margin-left: 8rpx; }

	.mn__lvrow { display: flex; align-items: baseline; white-space: nowrap; }
	.mn__lv { font-family: $ff-num; font-size: 38rpx; font-weight: 800; color: $c-ink; }
	.mn__lv-name { margin-left: 10rpx; font-size: 20rpx; color: $t-main; font-weight: 600; }
	.mn__growth { display: flex; align-items: baseline; margin-top: 10rpx; }
	.mn__growth-l { font-size: 20rpx; color: $t-tertiary; }
	.mn__growth-v { font-family: $ff-num; font-size: 26rpx; font-weight: 700; color: $c-primary; margin-left: 8rpx; }
	.mn__growth-s { font-family: $ff-num; font-size: 20rpx; color: $t-tertiary; margin-left: 2rpx; }
	.mn__wdeco--badge { width: 82rpx; height: 88rpx; margin-left: 6rpx; flex-shrink: 0; }

	/* ---------- 快捷列表 / 设置 ---------- */
	.mn__list { padding: 6rpx 28rpx; }
	.mn__lrow { display: flex; align-items: center; padding: 26rpx 0; border-bottom: 2rpx solid $c-line; }
	.mn__lrow:last-child { border-bottom: none; }
	.mn__lrow-ico { width: 44rpx; height: 40rpx; }
	.mn__lrow-t { flex: 1; margin-left: 22rpx; font-size: 28rpx; color: $t-main; font-weight: 500; }
	.mn__count {
		min-width: 56rpx; padding: 4rpx 16rpx;
		background: $c-mist; border-radius: $r-pill;
		display: flex; justify-content: center;
	}
	.mn__count-n { font-family: $ff-num; font-size: 24rpx; font-weight: 700; color: $c-primary; }
	.mn__chev--row { width: 28rpx; height: 28rpx; opacity: 0.35; margin-left: 16rpx; }

	.mn__bottom-space { height: 200rpx; }
</style>
