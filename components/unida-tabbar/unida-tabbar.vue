<template>
	<!-- UNIDA 专属底部导航 V4：纯 CSS 凹槽底座（开源通用做法，零图片） + U 星球发布键 + 3D 立体图标 -->
	<view class="unida-tabbar">
		<!-- 白色圆角底座：mask 径向渐变在中上真挖穿一个圆凹口，U 星球悬浮其中 -->
		<view class="tabbar-sheet"></view>

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

		<!-- 中央 U 星球发布键（悬浮凹口，呼吸光晕） -->
		<view class="publish-center" @tap="onPublishTap">
			<view class="publish-glow"></view>
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
	/* ==================== 容器 ==================== */
	.unida-tabbar {
		position: fixed;
		left: 0;
		right: 0;
		bottom: 0;
		height: calc(156rpx + env(safe-area-inset-bottom));
		height: calc(156rpx + constant(safe-area-inset-bottom));
		z-index: 9999;
		box-sizing: border-box;
		padding-bottom: env(safe-area-inset-bottom);
		padding-bottom: constant(safe-area-inset-bottom);
	}

	/* ==================== 凹槽底座（纯 CSS，开源通用做法） ==================== */
	.tabbar-sheet {
		position: absolute;
		left: 0;
		right: 0;
		bottom: 0;
		height: 132rpx;
		background: linear-gradient(180deg, #FFFFFF 0%, #FBF8FF 100%);
		border-radius: 44rpx 44rpx 0 0;
		box-shadow: 0 -8rpx 30rpx rgba(123, 97, 255, 0.10);
		/* 中上挖穿一个圆凹口（圆心在顶边中线，半径 66rpx），U 星球悬浮其中；
		   mask 是 uview 等开源凹槽 tabbar 的标准实现，小程序双内核均支持 */
		-webkit-mask: radial-gradient(circle at 50% 0, transparent 0 66rpx, #000 74rpx);
		mask: radial-gradient(circle at 50% 0, transparent 0 66rpx, #000 74rpx);
	}

	/* ==================== 导航布局 ==================== */
	.tabbar-content {
		position: absolute;
		left: 0;
		right: 0;
		top: 40rpx;
		height: 112rpx;
		display: grid;
		grid-template-columns: repeat(5, 1fr);
		align-items: start;
		z-index: 5;
	}
	.tab-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: flex-start;
		position: relative;
		padding-top: 8rpx;
		box-sizing: border-box;
	}
	.publish-space { pointer-events: none; }

	/* ==================== 3D 立体图标 ==================== */
	.icon-wrap {
		width: 66rpx;
		height: 66rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
		transition: transform 0.25s ease;
	}
	.tab-ico {
		width: 62rpx;
		height: 62rpx;
		opacity: 0.55;
		transition: opacity 0.25s ease, transform 0.25s ease;
	}
	/* 选中：图标弹起 + 底部紫色光晕 */
	.tab-item.active .tab-ico {
		opacity: 1;
		transform: translateY(-6rpx);
	}
	.tab-item.active .icon-wrap::after {
		content: '';
		position: absolute;
		left: 50%;
		bottom: -8rpx;
		transform: translateX(-50%);
		width: 84rpx;
		height: 24rpx;
		border-radius: 50%;
		background: radial-gradient(ellipse, rgba(128, 92, 250, 0.30) 0%, rgba(128, 92, 250, 0) 72%);
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

	/* ==================== 中央 U 星球发布键 ==================== */
	/* 凹口圆心在 sheet 顶边中线（距 tabbar 顶 24rpx），球心与其重合 */
	.publish-center {
		position: absolute;
		left: 50%;
		top: -32rpx;
		transform: translateX(-50%);
		width: 160rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		z-index: 20;
	}
	/* 呼吸光晕（径向渐变，不用 filter，性能友好） */
	.publish-glow {
		position: absolute;
		top: 44rpx;
		left: 50%;
		transform: translateX(-50%);
		width: 168rpx;
		height: 168rpx;
		border-radius: 50%;
		background: radial-gradient(circle, rgba(154, 120, 255, 0.32) 0%, rgba(154, 120, 255, 0.12) 46%, rgba(154, 120, 255, 0) 70%);
		animation: glowPulse 3.2s ease-in-out infinite;
	}
	@keyframes glowPulse {
		0%, 100% { opacity: 0.75; transform: translateX(-50%) scale(1); }
		50% { opacity: 1; transform: translateX(-50%) scale(1.06); }
	}
	.publish-logo {
		position: relative;
		width: 112rpx;
		height: 112rpx;
		z-index: 2;
	}
	.publish-text {
		margin-top: 4rpx;
		font-size: 23rpx;
		color: #6C3FF2;
		font-weight: 700;
		z-index: 2;
	}

	/* ==================== 点击反馈 ==================== */
	.tab-item:active .tab-ico { transform: scale(0.92); }
	.publish-center:active .publish-logo { transform: scale(0.92); }
</style>
