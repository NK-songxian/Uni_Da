<template>
	<!-- UNIDA Campus Character System：全站唯一人物资产，纯 CSS 绘制，禁止 emoji/图片 -->
	<!-- 简版：头+身；full 全身版：头发+脖子+手臂动作+腿，用于登录页主视觉 -->
	<view class="uc" :class="['uc--' + body, full ? 'uc--full' : '']">
		<view class="uc__head">
			<!-- 头发（仅全身版） -->
			<view v-if="full" class="uc__hair" :class="'uc__hair--' + hair"></view>
			<view class="uc__face">
				<!-- 墨镜表情 -->
				<block v-if="mood === 'cool'">
					<view class="uc__glasses">
						<view class="uc__lens uc__lens--l"></view>
						<view class="uc__bridge"></view>
						<view class="uc__lens uc__lens--r"></view>
					</view>
					<view class="uc__smile"></view>
				</block>
				<!-- 星星眼表情 -->
				<block v-else-if="mood === 'star'">
					<view class="uc__star uc__star--l"></view>
					<view class="uc__star uc__star--r"></view>
					<view class="uc__laugh"></view>
				</block>
				<!-- 大笑表情（默认） -->
				<block v-else>
					<view class="uc__eye uc__eye--l"></view>
					<view class="uc__eye uc__eye--r"></view>
					<view class="uc__laugh"></view>
				</block>
				<!-- 腮红 -->
				<view class="uc__blush uc__blush--l"></view>
				<view class="uc__blush uc__blush--r"></view>
			</view>
		</view>
		<!-- 脖子（仅全身版） -->
		<view v-if="full" class="uc__neck"></view>
		<view class="uc__body">
			<!-- 手臂动作（仅全身版） -->
			<block v-if="full">
				<view class="uc__arm uc__arm--l" :class="'uc__arm--' + armL"></view>
				<view class="uc__arm uc__arm--r" :class="'uc__arm--' + armR"></view>
			</block>
		</view>
		<!-- 腿（仅全身版） -->
		<block v-if="full">
			<view class="uc__leg uc__leg--l"></view>
			<view class="uc__leg uc__leg--r"></view>
		</block>
	</view>
</template>

<script>
	export default {
		name: 'unida-character',
		props: {
			// 表情：happy 大笑 | cool 墨镜 | star 星星眼
			mood: { type: String, default: 'happy' },
			// 身体色（品牌色板）：orange | yellow | green | purple
			body: { type: String, default: 'orange' },
			// 全身版（头发/手臂/腿）
			full: { type: Boolean, default: false },
			// 发型：short 短发 | long 长发
			hair: { type: String, default: 'short' },
			// 左手臂动作：down 下垂 | up 举起 | wave 挥手
			armL: { type: String, default: 'down' },
			// 右手臂动作：down 下垂 | up 举起 | wave 挥手 | victory 比V
			armR: { type: String, default: 'down' }
		}
	};
</script>

<style lang="scss" scoped>
	/* 品牌色 → CSS 变量，供身体/手臂统一取色 */
	.uc--orange { --uc-body: #ff8a3d; }
	.uc--yellow { --uc-body: #ffd76a; }
	.uc--green  { --uc-body: #34d399; }
	.uc--purple { --uc-body: #7b61ff; }

	.uc {
		position: relative;
		width: 150rpx;
		height: 260rpx;
	}
	/* ============ 全身版尺寸 ============ */
	.uc--full {
		width: 210rpx;
		height: 470rpx;
	}

	/* ---- 头 ---- */
	.uc__head {
		position: absolute;
		top: 0;
		left: 50%;
		transform: translateX(-50%);
		width: 100rpx;
		height: 100rpx;
		border-radius: 50%;
		background: #ffffff;
		box-shadow: 0 10rpx 28rpx rgba(55, 32, 150, 0.15);
		z-index: 3;
	}
	.uc--full .uc__head {
		width: 138rpx;
		height: 138rpx;
		box-shadow: 0 14rpx 34rpx rgba(55, 32, 150, 0.18);
	}
	.uc__face {
		position: absolute;
		inset: 0;
		z-index: 2;
	}

	/* ---- 头发（全身版）：稍大于头并上移，露出边缘发丝 ---- */
	.uc__hair {
		position: absolute;
		left: -5%;
		right: -5%;
		top: -6%;
		height: 52%;
		background: #2b2340;
		border-radius: 50% 50% 42% 42%;
		z-index: 1;
	}
	.uc__hair--long {
		height: 96%;
		left: -9%;
		right: -9%;
		top: -8%;
		border-radius: 50% 50% 46% 46%;
	}
	/* 长发两缕垂到脸侧 */
	.uc__hair--long::before,
	.uc__hair--long::after {
		content: '';
		position: absolute;
		bottom: -6%;
		width: 22%;
		height: 62%;
		background: #2b2340;
		border-radius: 0 0 40rpx 40rpx;
	}
	.uc__hair--long::before { left: -2%; }
	.uc__hair--long::after { right: -2%; }

	/* ---- 眼睛（圆点，百分比定位以适配两种尺寸） ---- */
	.uc__eye {
		position: absolute;
		top: 32%;
		width: 10%;
		height: 13%;
		border-radius: 50%;
		background: #29243d;
	}
	.uc__eye--l { left: 30%; }
	.uc__eye--r { right: 30%; }
	/* ---- 大笑嘴：开口半圆 ---- */
	.uc__laugh {
		position: absolute;
		left: 50%;
		transform: translateX(-50%);
		top: 52%;
		width: 40%;
		height: 21%;
		background: #29243d;
		border-radius: 0 0 40rpx 40rpx;
	}
	/* ---- 墨镜 ---- */
	.uc__glasses {
		position: absolute;
		top: 27%;
		left: 50%;
		transform: translateX(-50%);
		display: flex;
		align-items: center;
	}
	.uc__lens {
		width: 24%;
		height: 17%;
		border-radius: 7rpx;
		background: #29243d;
	}
	.uc__bridge {
		width: 8rpx;
		height: 4rpx;
		background: #29243d;
	}
	.uc__smile {
		position: absolute;
		left: 50%;
		transform: translateX(-50%);
		top: 55%;
		width: 24%;
		height: 14%;
		border-bottom: 4rpx solid #29243d;
		border-radius: 50%;
	}
	/* ---- 星星眼：旋转菱形 ---- */
	.uc__star {
		position: absolute;
		top: 29%;
		width: 15%;
		height: 15%;
		background: #ff8a3d;
		transform: rotate(45deg);
		border-radius: 3rpx;
	}
	.uc__star--l { left: 27%; }
	.uc__star--r { right: 27%; }
	/* ---- 腮红 ---- */
	.uc__blush {
		position: absolute;
		top: 58%;
		width: 13%;
		height: 8%;
		border-radius: 50%;
		background: rgba(255, 138, 61, 0.35);
	}
	.uc__blush--l { left: 16%; }
	.uc__blush--r { right: 16%; }

	/* ---- 脖子（全身版） ---- */
	.uc__neck {
		position: absolute;
		top: 128rpx;
		left: 50%;
		transform: translateX(-50%);
		width: 34rpx;
		height: 40rpx;
		background: #ffe0c8;
		z-index: 1;
	}

	/* ---- 身体 ---- */
	.uc__body {
		position: absolute;
		left: 50%;
		transform: translateX(-50%);
		bottom: 0;
		width: 125rpx;
		height: 135rpx;
		border-radius: 60rpx 60rpx 28rpx 28rpx;
		background: var(--uc-body, #ff8a3d);
		z-index: 2;
	}
	.uc--full .uc__body {
		bottom: 96rpx;
		width: 168rpx;
		height: 190rpx;
		border-radius: 70rpx 70rpx 34rpx 34rpx;
	}

	/* ---- 手臂（全身版） ---- */
	.uc__arm {
		position: absolute;
		top: 12%;
		width: 26rpx;
		height: 130rpx;
		background: var(--uc-body, #ff8a3d);
		border-radius: 26rpx;
		transform-origin: 50% 12%;
	}
	.uc__arm--l { left: -6rpx; }
	.uc__arm--r { right: -6rpx; }
	/* 拳头 */
	.uc__arm::after {
		content: '';
		position: absolute;
		bottom: -10rpx;
		left: 50%;
		transform: translateX(-50%);
		width: 34rpx;
		height: 34rpx;
		border-radius: 50%;
		background: #ffe0c8;
	}
	/* 下垂 */
	.uc__arm--down.uc__arm--l { transform: rotate(10deg); }
	.uc__arm--down.uc__arm--r { transform: rotate(-10deg); }
	/* 举起 */
	.uc__arm--up.uc__arm--l { transform: rotate(155deg); }
	.uc__arm--up.uc__arm--r { transform: rotate(-155deg); }
	/* 挥手（举手 + 手掌张开） */
	.uc__arm--wave.uc__arm--l { transform: rotate(150deg); }
	.uc__arm--wave.uc__arm--r { transform: rotate(-150deg); }
	.uc__arm--wave::after { border-radius: 40% 40% 45% 45%; }
	/* 比 V：举手 */
	.uc__arm--victory.uc__arm--r { transform: rotate(-160deg); }

	/* ---- 腿（全身版） ---- */
	.uc__leg {
		position: absolute;
		bottom: 0;
		width: 46rpx;
		height: 100rpx;
		background: #4b3f70;
		border-radius: 22rpx 22rpx 18rpx 18rpx;
		z-index: 1;
	}
	.uc__leg--l { left: 50%; margin-left: -50rpx; }
	.uc__leg--r { left: 50%; margin-left: 4rpx; }
</style>
