<template>
	<!-- UNIDA 专属底部导航 V5：完整白栏 + 悬浮圆形发布键（无波浪、无光晕脏斑、无 mask 兼容坑） -->
	<view class="unida-tabbar">
		<!-- 白色圆角底座：完整无挖洞，视觉干净统一 -->
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

		<!-- 中央 U 星球发布键：悬浮圆形实体底盘，无光晕脏斑 -->
		<view class="publish-center" @tap="onPublishTap">
			<view class="publish-disc">
				<image class="publish-logo" src="/static/unida/tabbar/publish-logo.png" mode="aspectFit" />
			</view>
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
		height: calc(132rpx + env(safe-area-inset-bottom));
		height: calc(132rpx + constant(safe-area-inset-bottom));
		z-index: 9999;
		box-sizing: border-box;
		padding-bottom: env(safe-area-inset-bottom);
		padding-bottom: constant(safe-area-inset-bottom);
	}

	/* ==================== 完整白栏（无挖洞、无遮罩，干净统一） ==================== */
	.tabbar-sheet {
		position: absolute;
		left: 0;
		right: 0;
		bottom: 0;
		height: 132rpx;
		background: linear-gradient(180deg, #FFFFFF 0%, #FCFAFF 100%);
		border-radius: 40rpx 40rpx 0 0;
		box-shadow: 0 -6rpx 24rpx rgba(123, 97, 255, 0.08);
	}

	/* ==================== 导航布局：图标+文字全部在白栏内 ==================== */
	.tabbar-content {
		position: absolute;
		left: 0;
		right: 0;
		bottom: 0;
		height: 132rpx;
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
		width: 58rpx;
		height: 58rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
		transition: transform 0.25s ease;
	}
	.tab-ico {
		width: 54rpx;
		height: 54rpx;
		opacity: 0.55;
		transition: opacity 0.25s ease, transform 0.25s ease;
	}
	/* 选中：仅图标上浮+高亮，不再加光斑（光斑在白底上成脏椭圆） */
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

	/* ==================== 中央 U 星球发布键（悬浮实体圆，无光晕） ==================== */
	.publish-center {
		position: absolute;
		left: 50%;
		top: -40rpx;
		transform: translateX(-50%);
		width: 160rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		z-index: 20;
	}
	/* 白色实体圆盘：清晰边界 + 品牌紫描边 + 轻投影，不弥散不脏 */
	.publish-disc {
		width: 108rpx;
		height: 108rpx;
		border-radius: 50%;
		background: #FFFFFF;
		box-sizing: border-box;
		border: 5rpx solid #7B61FF;
		box-shadow: 0 8rpx 22rpx rgba(123, 97, 255, 0.28);
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.publish-logo {
		width: 88rpx;
		height: 88rpx;
	}
	.publish-text {
		margin-top: 6rpx;
		font-size: 23rpx;
		color: #6C3FF2;
		font-weight: 700;
		line-height: 32rpx;
	}

	/* ==================== 点击反馈 ==================== */
	.tab-item:active .tab-ico { transform: scale(0.92); }
	.publish-center:active .publish-logo { transform: scale(0.92); }
</style>
