<template>
	<view class="pl unida-page">
		<view class="pl-safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 返回 -->
		<view class="pl__back" @click="goBack"><image class="pl__back-img" src="/static/icons-dark/back.png" mode="aspectFit" /><text class="pl__back-t">返回</text></view>

		<!-- 标题 -->
		<view class="pl__head">
			<image class="pl__head-badge" src="/static/unida/bubbles/pin-purple-u.webp" mode="heightFix" />
			<text class="pl__title">手机号登录</text>
			<text class="pl__sub">输入手机号，快捷登录 UNIDA</text>
		</view>

		<!-- 表单 -->
		<view class="pl__form">
			<view class="pl__item">
				<view class="pl__prefix"><text class="pl__prefix-t">+86</text><image class="pl__prefix-chev" src="/static/icons-dark/chevron.png" mode="aspectFit" /></view>
				<input class="pl__input" :value="phone" type="number" placeholder="请输入手机号" maxlength="11" @input="onPhone" />
			</view>
			<view class="pl__item">
				<input class="pl__input pl__input--code" :value="code" type="number" placeholder="请输入验证码" maxlength="6" @input="onCode" />
				<view class="pl__code" :class="{ 'pl__code--wait': counting }" @click="getCode"><text class="pl__code-t">{{ codeText }}</text></view>
			</view>
		</view>

		<!-- 协议 -->
		<view class="pl__agree">
			<view class="pl__checkbox" :class="{ 'pl__checkbox--on': agreed }" @click="onAgree">
				<image class="pl__checkbox-img" v-if="agreed" src="/static/unida/bubbles/check-purple.webp" mode="aspectFit" />
			</view>
			<text class="pl__agree-t">我已阅读并同意 </text><text class="pl__link" @click="onDoc('用户协议')">《用户协议》</text><text class="pl__link" @click="onDoc('隐私政策')">《隐私政策》</text>
		</view>

		<!-- 登录 -->
		<view class="pl__btn" @click="onLogin"><text class="pl__btn-t">登录</text></view>
		<text class="pl__tip">未注册手机号将自动创建账号</text>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				phone: '', code: '', codeText: '获取验证码', counting: false, agreed: true
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onPhone(e) { this.phone = e.detail.value; },
			onCode(e) { this.code = e.detail.value; },
			onAgree() { this.agreed = !this.agreed; },
			onDoc(name) { uni.navigateTo({ url: '/pages/agreement/agreement?type=' + name }); },
			getCode() {
				if (!/^1\d{10}$/.test(this.phone)) { uni.showToast({ title: '请输入正确手机号', icon: 'none' }); return; }
				if (this.counting) return;
				let n = 60;
				this.counting = true;
				this.codeText = n + 's';
				const t = setInterval(() => {
					n = n - 1;
					if (n === 0) { clearInterval(t); this.counting = false; this.codeText = '重新获取'; }
					else this.codeText = n + 's';
				}, 1000);
				uni.showToast({ title: '验证码已发送（演示）', icon: 'none' });
			},
			onLogin() {
				if (!/^1\d{10}$/.test(this.phone)) { uni.showToast({ title: '请输入正确手机号', icon: 'none' }); return; }
				if (!this.code) { uni.showToast({ title: '请输入验证码', icon: 'none' }); return; }
				if (!this.agreed) { uni.showToast({ title: '请先同意协议', icon: 'none' }); return; }
				uni.reLaunch({ url: '/pages/profile-setup/profile-setup' });
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.pl { min-height: 100vh; padding: 0 $page-x 60rpx; box-sizing: border-box; }
	.pl__back { display: flex; align-items: center; height: 80rpx; }
	.pl__back-img { width: 28rpx; height: 28rpx; }
	.pl__back-t { margin-left: 8rpx; font-size: 26rpx; color: $t-sub; }

	.pl__head { margin-top: 40rpx; display: flex; flex-direction: column; }
	.pl__head-badge { height: 72rpx; width: 84rpx; margin-bottom: 20rpx; }
	.pl__title { font-size: 46rpx; font-weight: 800; color: $c-ink; letter-spacing: 1rpx; }
	.pl__sub { margin-top: 12rpx; font-size: 26rpx; color: $t-sub; }

	.pl__form {
		margin-top: 48rpx;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 8rpx 28rpx;
	}
	.pl__item { display: flex; align-items: center; height: 104rpx; border-bottom: 2rpx solid $c-line; }
	.pl__item:last-child { border-bottom: none; }
	.pl__prefix { display: flex; align-items: center; margin-right: 20rpx; }
	.pl__prefix-t { font-size: 28rpx; color: $t-main; font-family: $ff-num; font-weight: 600; }
	.pl__prefix-chev { width: 24rpx; height: 24rpx; margin-left: 6rpx; transform: rotate(90deg); opacity: 0.5; }
	.pl__input { flex: 1; font-size: 28rpx; color: $t-main; min-width: 0; }
	.pl__input--code { margin-right: 16rpx; }
	.pl__code { background: $c-mist; border-radius: $r-pill; padding: 12rpx 22rpx; flex-shrink: 0; }
	.pl__code--wait { background: rgba(128, 92, 250, 0.08); }
	.pl__code-t { font-size: 24rpx; color: $c-primary; font-weight: 600; font-family: $ff-num; }

	.pl__agree { display: flex; align-items: center; margin-top: 32rpx; }
	.pl__checkbox {
		width: 34rpx; height: 34rpx;
		border-radius: 50%;
		border: 2rpx solid $t-tertiary;
		margin-right: 10rpx;
		display: flex; align-items: center; justify-content: center;
		box-sizing: border-box;
		flex-shrink: 0;
	}
	.pl__checkbox--on { background: $c-primary; border-color: $c-primary; }
	.pl__checkbox-img { width: 28rpx; height: 28rpx; }
	.pl__agree-t { font-size: 21rpx; color: $t-sub; }
	.pl__link { font-size: 21rpx; color: $c-primary; }

	.pl__btn {
		margin-top: 48rpx;
		height: 96rpx;
		border-radius: $r-pill;
		background: $g-cta;
		box-shadow: 0 12rpx 24rpx rgba(128, 92, 250, 0.28);
		display: flex; align-items: center; justify-content: center;
	}
	.pl__btn-t { font-size: 32rpx; color: $c-white; font-weight: 700; letter-spacing: 2rpx; }
	.pl__tip { display: block; margin-top: 30rpx; text-align: center; font-size: 23rpx; color: $t-tertiary; }
</style>
