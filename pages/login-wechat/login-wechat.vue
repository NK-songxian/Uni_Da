<template>
	<view class="lw unida-page">
		<view class="lw-safe" :style="{ paddingTop: statusBar + 'px' }"></view>
		<view class="lw__blob lw__blob--1"></view>
		<view class="lw__blob lw__blob--2"></view>

		<!-- 返回 -->
		<view class="lw__back" @click="goBack"><image class="lw__back-img" src="/static/icons-dark/back.png" mode="aspectFit" /><text class="lw__back-t">返回</text></view>

		<!-- hero -->
		<view class="lw__center">
			<view class="lw__wx">
				<image class="lw__wx-img" src="/static/unida/bubbles/brand-badge-u.webp" mode="aspectFit" />
				<image class="lw__wx-check" src="/static/unida/bubbles/check-green.webp" mode="aspectFit" />
			</view>
			<text class="lw__title">微信一键登录</text>
			<text class="lw__desc">使用微信登录 UNIDA
免注册，安全便捷</text>
		</view>

		<!-- 三个卖点 -->
		<view class="lw__features">
			<view class="lw__feature" v-for="(f, i) in features" :key="i">
				<view class="lw__feature-icon" :class="'lw__feature-icon--' + f.tone">
					<image class="lw__feature-img" :src="f.icon" mode="aspectFit" />
				</view>
				<text class="lw__feature-title">{{ f.title }}</text>
				<text class="lw__feature-sub">{{ f.sub }}</text>
			</view>
		</view>

		<!-- 操作区 -->
		<view class="lw__actions">
			<button class="lw__btn" open-type="getPhoneNumber" @getphonenumber="onLogin"><text class="lw__btn-t">微信一键登录</text></button>
			<view class="lw__switch" @click="onPhone"><text class="lw__switch-t">切换手机号登录</text></view>
			<view class="lw__agree">
				<view class="lw__checkbox" :class="{ 'lw__checkbox--on': agreed }" @click="onAgree">
					<image class="lw__checkbox-img" v-if="agreed" src="/static/unida/bubbles/check-purple.webp" mode="aspectFit" />
				</view>
				<text class="lw__agree-t">我已阅读并同意 </text><text class="lw__link" @click="onDoc('用户协议')">《用户协议》</text><text class="lw__link" @click="onDoc('隐私政策')">《隐私政策》</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				agreed: true,
				features: [
					{ icon: '/static/icons-dark/flame.png', title: '快速登录', sub: '一键进入，无需填写', tone: 'orange' },
					{ icon: '/static/icons-dark/buddy.png', title: '安全可信', sub: '微信官方授权保障', tone: 'green' },
					{ icon: '/static/icons-dark/calendar.png', title: '校园专属', sub: '仅限校园用户加入', tone: 'purple' }
				]
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onAgree() { this.agreed = !this.agreed; },
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
	@import '@/common/unida-tokens.scss';

	.lw { min-height: 100vh; padding: 0 $page-x 60rpx; position: relative; overflow: hidden; box-sizing: border-box; background: linear-gradient(180deg, #EFE8FF 0%, $c-mist 55%); }
	.lw__blob { position: absolute; border-radius: 50%; }
	.lw__blob--1 { width: 300rpx; height: 300rpx; background: $c-purple-light; top: -100rpx; right: -80rpx; opacity: 0.3; }
	.lw__blob--2 { width: 200rpx; height: 200rpx; background: $c-sun; top: 320rpx; left: -100rpx; opacity: 0.22; }

	.lw__back { position: relative; z-index: 2; display: flex; align-items: center; height: 80rpx; }
	.lw__back-img { width: 28rpx; height: 28rpx; }
	.lw__back-t { margin-left: 8rpx; font-size: 26rpx; color: $t-sub; }

	.lw__center { position: relative; z-index: 2; display: flex; flex-direction: column; align-items: center; margin-top: 72rpx; }
	.lw__wx {
		position: relative; width: 180rpx; height: 180rpx;
		border-radius: 48rpx;
		background: $g-brand;
		display: flex; align-items: center; justify-content: center;
		box-shadow: 0 20rpx 40rpx rgba(128, 92, 250, 0.32);
		transform: rotate(-8deg);
	}
	.lw__wx-img { width: 120rpx; height: 120rpx; }
	.lw__wx-check {
		position: absolute; right: -16rpx; bottom: -16rpx;
		width: 64rpx; height: 64rpx;
	}
	.lw__title { margin-top: 44rpx; font-size: 40rpx; font-weight: 800; color: $c-ink; letter-spacing: 1rpx; }
	.lw__desc { margin-top: 16rpx; font-size: 26rpx; color: $t-sub; text-align: center; line-height: 1.7; }

	.lw__features { position: relative; z-index: 2; display: flex; justify-content: space-between; margin-top: 64rpx; }
	.lw__feature {
		width: 32%;
		background: $c-white;
		border-radius: $r-md;
		padding: 28rpx 12rpx;
		display: flex; flex-direction: column; align-items: center;
		box-shadow: $sh-card;
		box-sizing: border-box;
	}
	.lw__feature-icon { width: 76rpx; height: 76rpx; border-radius: 22rpx; display: flex; align-items: center; justify-content: center; }
	.lw__feature-icon--orange { background: rgba(255, 155, 119, 0.16); }
	.lw__feature-icon--green { background: rgba(41, 202, 131, 0.14); }
	.lw__feature-icon--purple { background: rgba(128, 92, 250, 0.13); }
	.lw__feature-img { width: 38rpx; height: 38rpx; }
	.lw__feature-title { margin-top: 16rpx; font-size: 25rpx; font-weight: 700; color: $t-main; }
	.lw__feature-sub { margin-top: 8rpx; font-size: 20rpx; color: $t-tertiary; text-align: center; }

	.lw__actions { position: relative; z-index: 2; margin-top: 72rpx; }
	.lw__btn {
		width: 100%; height: 96rpx;
		border-radius: $r-pill;
		border: none;
		background: $g-brand;
		box-shadow: 0 12rpx 24rpx rgba(128, 92, 250, 0.3);
		display: flex; align-items: center; justify-content: center;
	}
	.lw__btn::after { border: none; }
	.lw__btn-t { font-size: 32rpx; color: $c-white; font-weight: 700; letter-spacing: 2rpx; }
	.lw__switch { margin-top: 28rpx; text-align: center; }
	.lw__switch-t { font-size: 27rpx; color: $c-primary; font-weight: 600; }

	.lw__agree { margin-top: 48rpx; display: flex; align-items: center; justify-content: center; }
	.lw__checkbox {
		width: 34rpx; height: 34rpx;
		border-radius: 50%;
		border: 2rpx solid $t-tertiary;
		margin-right: 10rpx;
		display: flex; align-items: center; justify-content: center;
		box-sizing: border-box;
		flex-shrink: 0;
	}
	.lw__checkbox--on { background: $c-primary; border-color: $c-primary; }
	.lw__checkbox-img { width: 28rpx; height: 28rpx; }
	.lw__agree-t { font-size: 21rpx; color: $t-sub; }
	.lw__link { font-size: 21rpx; color: $c-primary; }
</style>
