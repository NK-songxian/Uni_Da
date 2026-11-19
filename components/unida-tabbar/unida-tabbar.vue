<template>
	<!-- UNIDA 专属底部导航：波浪半透明底座 + 悬浮发布键 + 发光选中态 + 消息角标 -->
	<view class="unida-tabbar">
		<!-- 波浪底座：必须用 image 标签，小程序 background-image 引用本地图不生效 -->
		<view class="wave-solid"></view>
		<image class="wave-bg" src="/static/art/wave-bg.png" mode="scaleToFill" />
		<view class="wave-highlight"></view>

		<!-- 导航内容 -->
		<view class="tabbar-content">
			<!-- 首页 -->
			<view
				class="tab-item"
				:class="{ active: activeIndex === 0 }"
				@tap="onTabTap(0)"
			>
				<view class="icon-wrap"><view class="icon-home"></view></view>
				<text class="tab-text">首页</text>
				<view v-if="activeIndex === 0" class="active-line"></view>
			</view>

			<!-- 发现 -->
			<view
				class="tab-item"
				:class="{ active: activeIndex === 1 }"
				@tap="onTabTap(1)"
			>
				<view class="icon-wrap"><view class="icon-compass"></view></view>
				<text class="tab-text">发现</text>
				<view v-if="activeIndex === 1" class="active-line"></view>
			</view>

			<!-- 中间留白 -->
			<view class="tab-item publish-space"></view>

			<!-- 消息 -->
			<view
				class="tab-item"
				:class="{ active: activeIndex === 3 }"
				@tap="onTabTap(3)"
			>
				<view class="icon-wrap message-wrap">
					<view class="icon-message"></view>
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
				<view class="icon-wrap"><view class="icon-user"></view></view>
				<text class="tab-text">我的</text>
				<view v-if="activeIndex === 4" class="active-line"></view>
			</view>
		</view>

		<!-- 中央悬浮发布按钮 -->
		<view class="publish-center" @tap="onPublishTap">
			<view class="publish-orbit"></view>
			<view class="publish-button">
				<text class="plus-icon">+</text>
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
	/* ==================== 设计令牌 ==================== */
	.unida-tabbar {
		--purple: #805CFA;
		--purple-deep: #6941E8;
		--purple-light: #B69AFF;
		--text-main: #41365E;
		--text-muted: #88809F;

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

	/* ==================== 波浪底座（image 标签，S形起伏+立体渐变+高光） ==================== */
	.wave-bg {
		position: absolute;
		left: 0;
		top: 14rpx;
		width: 100%;
		height: 300rpx;
		/* 无 filter：小程序 image 上加 drop-shadow 会整片变暗/失效，立体感由图内渐变提供 */
		z-index: 1;
	}
	/* 波浪图下方的实心白底，从图的白色区接缝处铺到屏幕底，防止内容透上来 */
	.wave-solid {
		position: absolute;
		left: 0; right: 0;
		top: 150rpx;
		bottom: 0;
		background: #FFFFFF;
		z-index: 0;
	}
	.wave-highlight {
		position: absolute;
		left: 4%;
		right: 4%;
		top: -8rpx;
		height: 40rpx;
		border-radius: 50%;
		border-top: 2rpx solid rgba(255, 255, 255, 0.5);
		opacity: 0.6;
	}

	/* ==================== 导航布局 ==================== */
	.tabbar-content {
		position: absolute;
		left: 0;
		right: 0;
		top: 48rpx;
		height: 140rpx;
		display: grid;
		grid-template-columns: repeat(5, 1fr);
		align-items: start;
		z-index: 5;
	}
	.tab-item {
		height: 125rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: flex-start;
		position: relative;
		padding-top: 12rpx;
		box-sizing: border-box;
	}
	.publish-space { pointer-events: none; }

	/* ==================== ICON WRAP ==================== */
	.icon-wrap {
		width: 68rpx;
		height: 68rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
		border-radius: 23rpx;
		transition: all 0.25s ease;
	}
	/* 选中：发光背景 */
	.tab-item.active .icon-wrap {
		background: linear-gradient(145deg, #A88BFF, #7951F4);
		box-shadow:
			0 10rpx 25rpx rgba(126, 83, 244, 0.35),
			inset 0 2rpx 5rpx rgba(255, 255, 255, 0.45);
	}

	/* ==================== HOME ICON ==================== */
	.icon-home {
		position: relative;
		width: 27rpx;
		height: 25rpx;
		border: 4rpx solid var(--text-muted);
		border-top: none;
		border-radius: 3rpx 3rpx 6rpx 6rpx;
		box-sizing: border-box;
		margin-top: 12rpx;
	}
	.icon-home::before {
		content: '';
		position: absolute;
		width: 19rpx;
		height: 19rpx;
		left: 0;
		top: -10rpx;
		border-top: 4rpx solid var(--text-muted);
		border-left: 4rpx solid var(--text-muted);
		transform: rotate(45deg);
		border-radius: 3rpx;
	}
	.icon-home::after {
		content: '';
		position: absolute;
		width: 8rpx;
		height: 12rpx;
		bottom: 0;
		left: 6rpx;
		border: 3rpx solid var(--text-muted);
		border-bottom: none;
		border-radius: 5rpx 5rpx 0 0;
	}
	.active .icon-home,
	.active .icon-home::before,
	.active .icon-home::after { border-color: #FFFFFF; }

	/* ==================== COMPASS ICON ==================== */
	.icon-compass {
		position: relative;
		width: 36rpx;
		height: 36rpx;
		border: 4rpx solid var(--text-muted);
		border-radius: 50%;
		box-sizing: border-box;
	}
	.icon-compass::before {
		content: '';
		position: absolute;
		left: 10rpx;
		top: 4rpx;
		width: 0;
		height: 0;
		border-left: 6rpx solid transparent;
		border-right: 6rpx solid transparent;
		border-bottom: 17rpx solid #9679E9;
		transform: rotate(35deg);
	}
	.icon-compass::after {
		content: '';
		position: absolute;
		left: 10rpx;
		bottom: 4rpx;
		width: 0;
		height: 0;
		border-left: 6rpx solid transparent;
		border-right: 6rpx solid transparent;
		border-top: 13rpx solid #B6A5EF;
		transform: rotate(35deg);
	}

	/* ==================== MESSAGE ICON ==================== */
	.icon-message {
		position: relative;
		width: 38rpx;
		height: 29rpx;
		border: 4rpx solid var(--text-muted);
		border-radius: 50%;
		box-sizing: border-box;
	}
	.icon-message::after {
		content: '';
		position: absolute;
		left: 3rpx;
		bottom: -8rpx;
		width: 10rpx;
		height: 10rpx;
		border-left: 4rpx solid var(--text-muted);
		transform: skew(-25deg);
	}
	/* 消息角标 */
	.message-wrap { position: relative; }
	.message-badge {
		position: absolute;
		top: -5rpx;
		right: -12rpx;
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
	}

	/* ==================== USER ICON ==================== */
	.icon-user {
		position: relative;
		width: 20rpx;
		height: 20rpx;
		border: 4rpx solid var(--text-muted);
		border-radius: 50%;
		margin-top: -12rpx;
	}
	.icon-user::after {
		content: '';
		position: absolute;
		width: 32rpx;
		height: 18rpx;
		left: -10rpx;
		top: 26rpx;
		border: 4rpx solid var(--text-muted);
		border-radius: 20rpx 20rpx 8rpx 8rpx;
		border-bottom: none;
		box-sizing: border-box;
	}

	/* ==================== 选中态图标变白 ==================== */
	.active .icon-compass,
	.active .icon-message,
	.active .icon-user { border-color: #FFFFFF; }
	.active .icon-message::after { border-color: #FFFFFF; }
	.active .icon-user::after { border-color: #FFFFFF; }
	.active .icon-compass::before { border-bottom-color: #FFFFFF; }
	.active .icon-compass::after { border-top-color: #FFFFFF; }

	/* ==================== 文字 ==================== */
	.tab-text {
		margin-top: 5rpx;
		font-size: 23rpx;
		color: var(--text-muted);
		font-weight: 500;
		line-height: 34rpx;
	}
	.active .tab-text { color: #7951F4; font-weight: 700; }
	/* 激活指示线 */
	.active-line {
		width: 42rpx;
		height: 9rpx;
		margin-top: 4rpx;
		border-radius: 20rpx;
		background: linear-gradient(90deg, #B69AFF, #805CFA);
		box-shadow: 0 3rpx 10rpx rgba(128, 92, 250, 0.25);
	}

	/* ==================== 中央悬浮发布按钮 ==================== */
	.publish-center {
		position: absolute;
		left: 50%;
		top: 40rpx;
		transform: translateX(-50%);
		width: 120rpx;
		height: 150rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
		z-index: 20;
	}
	.publish-orbit {
		position: absolute;
		top: -6rpx;
		left: 50%;
		transform: translateX(-50%);
		width: 104rpx;
		height: 104rpx;
		border-radius: 50%;
		border: 2rpx solid rgba(178, 151, 255, 0.35);
		box-shadow:
			0 0 0 8rpx rgba(180, 154, 255, 0.10),
			0 6rpx 20rpx rgba(132, 91, 250, 0.16);
	}
	.publish-button {
		position: relative;
		width: 80rpx;
		height: 80rpx;
		border-radius: 50%;
		background: linear-gradient(145deg, #A98BFF 0%, #8964FC 55%, #754AF0 100%);
		box-shadow:
			0 12rpx 26rpx rgba(114, 73, 231, 0.4),
			inset 0 3rpx 6rpx rgba(255, 255, 255, 0.45);
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.plus-icon {
		color: #FFFFFF;
		font-size: 56rpx;
		font-weight: 300;
		line-height: 1;
		margin-top: -5rpx;
	}
	.publish-text {
		margin-top: 8rpx;
		font-size: 23rpx;
		color: #7951F4;
		font-weight: 700;
	}

	/* ==================== 点击反馈 ==================== */
	.tab-item:active .icon-wrap { transform: scale(0.92); }
	.publish-center:active .publish-button { transform: scale(0.92); }
</style>
