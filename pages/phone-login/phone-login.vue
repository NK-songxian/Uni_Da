<template>
	<view class="pl unida-page">
		<navigator class="pl__back" open-type="navigateBack" delta="1">‹ 返回</navigator>
		<view class="pl__head">
			<text class="pl__title">手机号登录</text>
			<text class="pl__sub">输入手机号，快捷登录 UNIDA</text>
		</view>
		<view class="pl__form unida-card">
			<view class="pl__item">
				<text class="pl__prefix">+86 ▾</text>
				<input class="pl__input" v-model="phone" type="number" placeholder="请输入手机号" maxlength="11" />
			</view>
			<view class="pl__item">
				<input class="pl__input" v-model="code" type="number" placeholder="请输入验证码" maxlength="6" />
				<text class="pl__code" @click="getCode">{{ codeText }}</text>
			</view>
		</view>
		<view class="pl__btn unida-btn unida-btn--primary" @click="onLogin">登录</view>
		<text class="pl__tip">未注册手机号将自动创建账号</text>
	</view>
</template>

<script>
	export default {
		data() {
			return { phone: '', code: '', codeText: '获取验证码', counting: false };
		},
		methods: {
			getCode() {
				if (!/^1\d{10}$/.test(this.phone)) { uni.showToast({ title: '请输入正确手机号', icon: 'none' }); return; }
				if (this.counting) return;
				let n = 60;
				this.counting = true;
				this.codeText = n + 's';
				const t = setInterval(() => {
					n--;
					if (n <= 0) { clearInterval(t); this.counting = false; this.codeText = '重新获取'; }
					else this.codeText = n + 's';
				}, 1000);
				uni.showToast({ title: '验证码已发送（演示）', icon: 'none' });
			},
			onLogin() {
				if (!/^1\d{10}$/.test(this.phone)) { uni.showToast({ title: '请输入正确手机号', icon: 'none' }); return; }
				if (!this.code) { uni.showToast({ title: '请输入验证码', icon: 'none' }); return; }
				uni.reLaunch({ url: '/pages/profile-setup/profile-setup' });
			}
		},
		onUnload() { if (this.timer) clearInterval(this.timer); }
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.pl { min-height: 100vh; padding: 0 40rpx 60rpx; }
	.pl__back { font-size: 32rpx; color: $unida-text; padding-top: 70rpx; display: inline-block; }
	.pl__head { margin-top: 60rpx; }
	.pl__title { display: block; font-size: 46rpx; font-weight: 800; color: $unida-text; }
	.pl__sub { display: block; margin-top: 12rpx; font-size: 26rpx; color: $unida-text-sub; }
	.pl__form { margin-top: 60rpx; padding: 8rpx 28rpx; }
	.pl__item { display: flex; align-items: center; height: 100rpx; border-bottom: 2rpx solid $unida-divider; }
	.pl__item:last-child { border-bottom: none; }
	.pl__prefix { font-size: 28rpx; color: $unida-text; margin-right: 20rpx; }
	.pl__input { flex: 1; font-size: 28rpx; }
	.pl__code { font-size: 26rpx; color: $unida-primary; font-weight: 600; white-space: nowrap; }
	.pl__btn { margin-top: 60rpx; }
	.pl__tip { display: block; margin-top: 30rpx; text-align: center; font-size: 24rpx; color: $unida-text-sub; }
</style>
