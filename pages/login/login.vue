<template>
	<view class="page">
		<!-- ============ 用户定稿设计图：顶部补天空避灵动岛，底部补草坪铺满屏幕 ============ -->
		<view class="art-wrap">
			<image class="art" src="/static/login-design-fill.jpg" mode="widthFix" />

			<!-- ============ 完全透明的登录控件（无毛玻璃/无框） ============ -->
			<view class="dock">
				<button
					class="wechat-btn"
					open-type="getPhoneNumber"
					@getphonenumber="onGetPhone"
					:loading="loading"
					:disabled="loading"
				>
					<view class="wechat-icon">
						<view class="bubble bubble-main"></view>
						<view class="bubble bubble-small"></view>
					</view>
					<text>{{ loading ? '正在登录...' : '微信一键登录' }}</text>
				</button>

				<view class="guest" @click="onGuest">游客先逛逛 <text class="guest-arrow">›</text></view>

				<view class="agreement-row">
					<view class="checkbox" :class="{ checked: agreed }" @click="agreed = !agreed">
						<view v-if="agreed" class="checkbox-tick"></view>
					</view>
					<view class="agreement-text">
						<text>我已阅读并同意</text>
						<text class="agreement-link" @click.stop="openDoc('用户协议')">《用户协议》</text>
						<text class="agreement-separator">和</text>
						<text class="agreement-link" @click.stop="openDoc('隐私政策')">《隐私政策》</text>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import { CLOUD_MODE, callCloud, saveSession } from '@/common/cloud.js';

	export default {
		data() {
			return {
				agreed: false,
				loading: false
			};
		},
		methods: {
			onGetPhone(e) {
				if (!this.agreed) {
					uni.showToast({ title: '请先同意用户协议和隐私政策', icon: 'none' });
					return;
				}
				const phoneCode = e.detail && e.detail.code;
				const doLogin = (loginCode) => {
					if (!CLOUD_MODE.enabled) {
						// mock 模式：直接进资料设置（保持原有体验）
						this.loading = false;
						uni.reLaunch({ url: '/pages/profile-setup/profile-setup' });
						return;
					}
					callCloud('login', { code: loginCode, phoneCode }).then((r) => {
						this.loading = false;
						saveSession(r.token, r.user);
						uni.reLaunch({ url: r.isNew ? '/pages/profile-setup/profile-setup' : '/pages/home/home' });
					}).catch((err) => {
						this.loading = false;
						uni.showToast({ title: err.message || '登录失败，请重试', icon: 'none' });
					});
				};

				this.loading = true;
				if (CLOUD_MODE.enabled) {
					uni.login({
						provider: 'weixin',
						success: (res) => doLogin(res.code),
						fail: () => {
							this.loading = false;
							uni.showToast({ title: '获取登录凭证失败', icon: 'none' });
						}
					});
				} else {
					setTimeout(() => doLogin('mock'), 800);
				}
			},
			onGuest() {
				uni.reLaunch({ url: '/pages/home/home' });
			},
			openDoc(name) {
				uni.navigateTo({ url: '/pages/agreement/agreement?type=' + name });
			}
		}
	};
</script>

<style lang="scss" scoped>
	page { background: #a9b56d; }
	.page {
		width: 100%;
		min-height: 100vh;
		/* 与扩展图顶部天空/底部草坪同色，全面屏多余区域无缝衔接 */
		background: linear-gradient(180deg, #d0d1fc 0%, #a9b56d 100%);
		overflow: hidden;
	}

	/* ====== 图片容器：宽 750rpx，高度由图 1:1 决定 ====== */
	.art-wrap {
		position: relative;
		width: 750rpx;
		margin: 0 auto;
	}
	.art {
		width: 100%;
		display: block;
	}

	/* ====== 完全透明的登录控件：无框、无毛玻璃、无投影 ====== */
	.dock {
		position: fixed;
		left: 48rpx;
		right: 48rpx;
		bottom: 24rpx;
		bottom: calc(24rpx + env(safe-area-inset-bottom));
		z-index: 30;
		padding: 0;
		box-sizing: border-box;
		background: transparent;
		border: none;
		box-shadow: none;
		backdrop-filter: none;
		-webkit-backdrop-filter: none;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	/* ---- 微信主按钮（绿渐变 + 光泽扫过动效） ---- */
	.wechat-btn {
		position: relative;
		width: 100%;
		height: 98rpx;
		padding: 0;
		border: none;
		border-radius: 56rpx;
		overflow: hidden;
		background: linear-gradient(100deg, #12c76a 0%, #05a854 100%);
		color: #fff;
		font-size: 34rpx;
		font-weight: 700;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow:
			0 12rpx 26rpx rgba(9, 180, 90, 0.32),
			inset 0 2rpx 0 rgba(255, 255, 255, 0.3);
		transition: transform 0.15s ease, opacity 0.15s ease;
	}
	.wechat-btn::after { border: none; }
	.wechat-btn:active { transform: scale(0.98); opacity: 0.92; }
	/* 光泽扫过 */
	.wechat-btn::before {
		content: '';
		position: absolute;
		top: 0; left: -60%;
		width: 45%; height: 100%;
		background: linear-gradient(100deg, transparent, rgba(255,255,255,0.35), transparent);
		transform: skewX(-20deg);
		animation: shineSweep 3.2s ease-in-out infinite;
	}
	@keyframes shineSweep {
		0%, 62% { left: -60%; }
		85%, 100% { left: 130%; }
	}
	/* 微信双气泡图标 */
	.wechat-icon { position: relative; width: 50rpx; height: 46rpx; margin-right: 14rpx; }
	.bubble { position: absolute; border-radius: 50%; background: #fff; }
	.bubble-main { width: 38rpx; height: 31rpx; left: 0; top: 2rpx; }
	.bubble-main::after { content: ''; position: absolute; left: 8rpx; bottom: -7rpx; width: 12rpx; height: 12rpx; background: #fff; transform: rotate(25deg); }
	.bubble-small { width: 28rpx; height: 24rpx; right: 0; bottom: 2rpx; }

	/* ---- 游客入口（白字 + 深紫描边影，透明背景下依然清晰） ---- */
	.guest {
		margin-top: 24rpx;
		color: #fff;
		font-size: 28rpx;
		font-weight: 700;
		text-shadow: 0 2rpx 10rpx rgba(54, 34, 118, 0.75);
	}
	.guest-arrow { font-size: 36rpx; margin-left: 4rpx; }

	/* ---- 协议 ---- */
	.agreement-row {
		margin-top: 18rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		color: rgba(255, 255, 255, 0.96);
		font-size: 21rpx;
		line-height: 1.5;
		text-shadow: 0 2rpx 8rpx rgba(45, 35, 20, 0.7);
	}
	.checkbox {
		flex-shrink: 0;
		width: 32rpx; height: 32rpx;
		margin-right: 10rpx;
		border-radius: 50%;
		border: 2rpx solid rgba(255, 255, 255, 0.95);
		box-shadow: 0 2rpx 8rpx rgba(45, 35, 20, 0.35);
		box-sizing: border-box;
		display: flex; align-items: center; justify-content: center;
	}
	.checkbox.checked { border-color: #7b61ff; background: #7b61ff; }
	.checkbox-tick {
		width: 15rpx; height: 8rpx;
		border-left: 3rpx solid #fff;
		border-bottom: 3rpx solid #fff;
		transform: rotate(-45deg) translate(1rpx, -2rpx);
	}
	.agreement-text { text-align: left; }
	.agreement-link { color: #ffd76a; margin-left: 4rpx; font-weight: 700; }
	.agreement-separator { margin-left: 4rpx; }
</style>
