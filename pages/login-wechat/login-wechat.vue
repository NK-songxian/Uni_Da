<template>
	<view class="lw unida-page">
		<view class="lw__blob lw__blob--1"></view>
		<view class="lw__blob lw__blob--2"></view>
		<navigator class="lw__back" open-type="navigateBack" delta="1">‹ 返回</navigator>

		<view class="lw__center">
			<!-- 微信图标 + 对勾，还原展板 -->
			<view class="lw__wx">
				<text class="lw__wx-icon">💬</text>
				<view class="lw__wx-check">✓</view>
			</view>
			<text class="lw__title">微信一键登录</text>
			<text class="lw__desc">使用微信登录 UNIDA<br />免注册，安全便捷</text>
		</view>

		<!-- 三个卖点 -->
		<view class="lw__features">
			<view class="lw__feature" v-for="(f, i) in features" :key="i">
				<view class="lw__feature-icon" :style="{ background: f.bg }">{{ f.icon }}</view>
				<text class="lw__feature-title">{{ f.title }}</text>
				<text class="lw__feature-sub">{{ f.sub }}</text>
			</view>
		</view>

		<!-- 主按钮 -->
		<view class="lw__actions">
			<button class="lw__btn" open-type="getPhoneNumber" @getphonenumber="onLogin">
				<text class="lw__btn-icon">💬</text> 微信一键登录
			</button>
			<view class="lw__switch" @click="onPhone">切换手机号登录</view>
			<view class="lw__agree">
				<view class="lw__checkbox" :class="{ 'lw__checkbox--on': agreed }" @click="agreed = !agreed">
					<text v-if="agreed">✓</text>
				</view>
				<text>我已阅读并同意 <text class="lw__link" @click.stop="onDoc('用户协议')">《用户协议》</text><text class="lw__link" @click.stop="onDoc('隐私政策')">《隐私政策》</text></text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				agreed: true,
				features: [
					{ icon: '⚡', title: '快速登录', sub: '一键进入，无需填写', bg: 'linear-gradient(135deg,#FF8A3D,#FFD76A)' },
					{ icon: '🛡️', title: '安全可信', sub: '微信官方授权保障', bg: 'linear-gradient(135deg,#34D399,#86EFAC)' },
					{ icon: '🎓', title: '校园专属', sub: '仅限校园用户加入', bg: 'linear-gradient(135deg,#7B61FF,#B59BFF)' }
				]
			};
		},
		methods: {
			check() {
				if (!this.agreed) {
					uni.showToast({ title: '请先同意协议', icon: 'none' });
					return false;
				}
				return true;
			},
			onLogin(e) {
				if (!this.check()) return;
				console.log('getPhoneNumber code:', e.detail && e.detail.code);
				uni.reLaunch({ url: '/pages/profile-setup/profile-setup' });
			},
			onPhone() { uni.navigateTo({ url: '/pages/phone-login/phone-login' }); },
			onDoc(name) { uni.navigateTo({ url: '/pages/agreement/agreement?type=' + name }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.lw { min-height: 100vh; padding: 0 40rpx 60rpx; position: relative; overflow: hidden; background: linear-gradient(180deg,#F3EDFF 0%, $unida-bg 45%); }
	.lw__blob { position: absolute; border-radius: 50%; opacity: 0.4; }
	.lw__blob--1 { width: 300rpx; height: 300rpx; background: #B59BFF; top: -100rpx; right: -80rpx; }
	.lw__blob--2 { width: 200rpx; height: 200rpx; background: #FFD76A; top: 300rpx; left: -100rpx; opacity: 0.3; }
	.lw__back { position: relative; z-index: 2; padding-top: 70rpx; font-size: 30rpx; color: $unida-text; }
	.lw__center { position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; margin-top: 100rpx; }
	.lw__wx { position: relative; width: 180rpx; height: 180rpx; border-radius: 50rpx; background: linear-gradient(135deg,#7B61FF,#B59BFF); display: flex; align-items: center; justify-content: center; box-shadow: 0 20rpx 44rpx rgba(123,97,255,0.35); transform: rotate(-8deg); }
	.lw__wx-icon { font-size: 96rpx; }
	.lw__wx-check { position: absolute; right: -16rpx; bottom: -16rpx; width: 64rpx; height: 64rpx; border-radius: 50%; background: #07C160; color: #fff; font-size: 36rpx; display: flex; align-items: center; justify-content: center; border: 6rpx solid #fff; }
	.lw__title { margin-top: 48rpx; font-size: 40rpx; font-weight: 800; color: $unida-text; }
	.lw__desc { margin-top: 16rpx; font-size: 26rpx; color: $unida-text-sub; text-align: center; line-height: 1.7; }
	.lw__features { position: relative; z-index: 2; display: flex; justify-content: space-between; margin-top: 80rpx; }
	.lw__feature { width: 32%; background: #fff; border-radius: 24rpx; padding: 28rpx 12rpx; display: flex; flex-direction: column; align-items: center; box-shadow: 0 8rpx 24rpx rgba(123,97,255,0.08); }
	.lw__feature-icon { width: 80rpx; height: 80rpx; border-radius: 24rpx; display: flex; align-items: center; justify-content: center; font-size: 42rpx; }
	.lw__feature-title { margin-top: 16rpx; font-size: 26rpx; font-weight: 700; color: $unida-text; }
	.lw__feature-sub { margin-top: 8rpx; font-size: 20rpx; color: $unida-text-sub; text-align: center; }
	.lw__actions { position: relative; z-index: 2; margin-top: auto; padding-top: 80rpx; }
	.lw__btn { width: 100%; height: 96rpx; border-radius: 999rpx; border: none; background: linear-gradient(135deg,#7B61FF,#B59BFF); color: #fff; font-size: 32rpx; font-weight: 700; display: flex; align-items: center; justify-content: center; box-shadow: 0 12rpx 28rpx rgba(123,97,255,0.3); }
	.lw__btn::after { border: none; }
	.lw__btn-icon { font-size: 36rpx; margin-right: 12rpx; }
	.lw__switch { margin-top: 28rpx; text-align: center; font-size: 28rpx; color: $unida-primary; font-weight: 600; }
	.lw__agree { margin-top: 40rpx; display: flex; align-items: center; justify-content: center; font-size: 22rpx; color: $unida-text-sub; }
	.lw__checkbox { width: 32rpx; height: 32rpx; border-radius: 50%; border: 2rpx solid #c9c2dd; margin-right: 10rpx; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 20rpx; }
	.lw__checkbox--on { background: $unida-primary; border-color: $unida-primary; }
	.lw__link { color: $unida-primary; }
</style>
