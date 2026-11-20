<template>
	<!-- UNIDA 专属底部导航 V6：图片镂空 U 型凹槽白栏（真机必渲染） + U 星球发布球嵌谷 -->
	<view class="unida-tabbar">
		<!-- 白栏顶部真挖 U 型谷（PNG 透明区），发布球坐进谷里；图片方案规避 mask 真机失效 -->
		<image class="tabbar-sheet" src="/static/unida/tabbar/tabbar-sheet.png" mode="widthFix" />

		<!-- 导航内容 -->
		<view class="tabbar-content">
			<!-- 首页 -->
			<view
				class="tab-item"
				:class="{ active: activeIndex === 0 }"
				@tap="onTabTap(0)"
			>
				<view class="icon-wrap"><image class="tab-ico" src="/static/unida/tabbar/tab-home.png" mode="aspectFit" /></view>
				<text class="tab-text">首页</text>
				<view v-if="activeIndex === 0" class="active-line"></view>
			</view>

			<!-- 发现 -->
			<view
				class="tab-item"
				:class="{ active: activeIndex === 1 }"
				@tap="onTabTap(1)"
			>
				<view class="icon-wrap"><image class="tab-ico" src="/static/unida/tabbar/tab-discover.png" mode="aspectFit" /></view>
				<text class="tab-text">发现</text>
				<view v-if="activeIndex === 1" class="active-line"></view>
			</view>

			<!-- 中间留白（凹口区，U 星球独立悬浮） -->
			<view class="tab-item publish-space"></view>

			<!-- 消息 -->
			<view
				class="tab-item"
				:class="{ active: activeIndex === 3 }"
				@tap="onTabTap(3)"
			>
				<view class="icon-wrap message-wrap">
					<image class="tab-ico" src="/static/unida/tabbar/tab-message.png" mode="aspectFit" />
					<view v-if="unreadCount > 0" class="message-badge">
						{{ unreadCount > 99 ? '99+' : unreadCount }}
					</view>
				</view>
				<text class="tab-text">消息</text>
				<view v-if="activeIndex === 3" class="active-line"></view>
			</view>

			<!-- 我的 -->
			<view
				class="tab-item"
				:class="{ active: activeIndex === 4 }"
				@tap="onTabTap(4)"
			>
				<view class="icon-wrap"><image class="tab-ico" src="/static/unida/tabbar/tab-mine.png" mode="aspectFit" /></view>
				<text class="tab-text">我的</text>
				<view v-if="activeIndex === 4" class="active-line"></view>
			</view>
		</view>

		<!-- 中央 U 星球发布球：坐进 U 型谷，谷是托盘，不再套圆盘 -->
		<view class="publish-center" @tap="onPublishTap">
			<image class="publish-logo" src="/static/unida/tabbar/publish-logo.png" mode="aspectFit" />
			<text class="publish-text">发布</text>
		</view>
	</view>
</template>

<script>
	// 项目真实页面路径（非原生 tabBar，故跳转用 reLaunch）
	const TAB_PAGES = [
		'/pages/home/home',
		'/pages/discover/discover',
		'/pages/publish/publish',
		'/pages/message/message',
		'/pages/mine/mine'
	];

	export default {
		name: 'unida-tabbar',
		props: {
			// 当前选中：0 首页 1 发现 3 消息 4 我的（selected 优先，current 兼容旧调用）
			selected: { type: Number, default: -1 },
			current: { type: Number, default: -1 },
			// 未读消息数
			unreadCount: { type: Number, default: 0 }
		},
		computed: {
			activeIndex() {
				return this.selected >= 0 ? this.selected : this.current;
			}
		},
		methods: {
			onTabTap(index) {
				this.navigateToTab(index);
			},
			onPublishTap() {
				this.navigateToTab(2);
			},
			navigateToTab(index) {
				const url = TAB_PAGES[index];
				if (!url || index === this.activeIndex) return;
				uni.reLaunch({
					url,
					fail(err) {
						console.error('Tab 跳转失败：', err);
					}
				});
			}
		}
	};
</script>

<style lang="scss" scoped>
	/* ==================== 容器：跟随白栏图片高度 200rpx ==================== */
	.unida-tabbar {
		position: fixed;
		left: 0;
		right: 0;
		bottom: 0;
		height: calc(200rpx + env(safe-area-inset-bottom));
		height: calc(200rpx + constant(safe-area-inset-bottom));
		z-index: 9999;
		box-sizing: border-box;
		padding-bottom: env(safe-area-inset-bottom);
		padding-bottom: constant(safe-area-inset-bottom);
	}

	/* ==================== U 型凹槽白栏（图片镂空，真机必渲染） ==================== */
	/* 图片 750×200@2x，满屏宽 750rpx → 高 200rpx；顶部两肩 13rpx、谷底 59rpx，
	   谷区透明露出页面背景；阴影已烘焙进 PNG，跟随凹槽曲线 */
	.tabbar-sheet {
		position: absolute;
		left: 0;
		bottom: 0;
		width: 100%;
		height: 200rpx;
	}

	/* ==================== 导航布局：图标+文字排在谷底以下白栏主体 ==================== */
	.tabbar-content {
		position: absolute;
		left: 0;
		right: 0;
		bottom: 0;
		height: 130rpx;
		display: grid;
		grid-template-columns: repeat(5, 1fr);
		align-items: center;
		z-index: 5;
	}
	.tab-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		position: relative;
		box-sizing: border-box;
	}
	.publish-space { pointer-events: none; }

	/* ==================== 3D 立体图标 ==================== */
	.icon-wrap {
		width: 56rpx;
		height: 56rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
		transition: transform 0.25s ease;
	}
	.tab-ico {
		width: 52rpx;
		height: 52rpx;
		opacity: 0.55;
		transition: opacity 0.25s ease, transform 0.25s ease;
	}
	.tab-item.active .tab-ico {
		opacity: 1;
		transform: translateY(-4rpx);
	}

	/* 消息角标 */
	.message-wrap { position: relative; }
	.message-badge {
		position: absolute;
		top: -6rpx;
		right: -10rpx;
		min-width: 30rpx;
		height: 30rpx;
		padding: 0 7rpx;
		border-radius: 30rpx;
		background: linear-gradient(135deg, #FF9B45, #FF702E);
		color: #FFFFFF;
		font-size: 19rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		border: 3rpx solid #FFFFFF;
		box-shadow: 0 4rpx 10rpx rgba(255, 112, 46, 0.25);
		z-index: 2;
	}

	/* ==================== 文字 ==================== */
	.tab-text {
		margin-top: 6rpx;
		font-size: 23rpx;
		color: #88809F;
		font-weight: 500;
		line-height: 34rpx;
	}
	.active .tab-text { color: #6C3FF2; font-weight: 700; }
	/* 激活指示线 */
	.active-line {
		width: 42rpx;
		height: 9rpx;
		margin-top: 4rpx;
		border-radius: 20rpx;
		background: linear-gradient(90deg, #B69AFF, #805CFA);
		box-shadow: 0 3rpx 10rpx rgba(128, 92, 250, 0.25);
	}

	/* ==================== 中央 U 星球发布球（坐进 U 型谷） ==================== */
	/* 谷两肩 13rpx、谷底 59rpx；球心落在谷底稍上，直径 108rpx，上沿露出谷口 */
	.publish-center {
		position: absolute;
		left: 50%;
		top: 14rpx;
		transform: translateX(-50%);
		width: 160rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		z-index: 20;
	}
	.publish-logo {
		width: 108rpx;
		height: 108rpx;
	}
	.publish-text {
		margin-top: 2rpx;
		font-size: 23rpx;
		color: #6C3FF2;
		font-weight: 700;
		line-height: 30rpx;
	}

	/* ==================== 点击反馈 ==================== */
	.tab-item:active .tab-ico { transform: scale(0.92); }
	.publish-center:active .publish-logo { transform: scale(0.92); }
</style>
