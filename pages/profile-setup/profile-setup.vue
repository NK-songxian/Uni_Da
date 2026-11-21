<template>
	<view class="st unida-page">
		<view class="st-safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 顶部步骤 -->
		<view class="st__top">
			<view class="st__back" @click="goBack"><image class="st__back-img" src="/static/icons-dark/back.png" mode="aspectFit" /></view>
			<view class="st__steps">
				<view class="st__step {{step === 1 ? 'st__step--on' : ''}} {{step !== 1 ? 'st__step--done' : ''}}">
					<view class="st__dot"><text class="st__dot-t">1</text></view>
					<text class="st__step-t">校园验证</text>
				</view>
				<view class="st__line {{step !== 1 ? 'st__line--on' : ''}}"></view>
				<view class="st__step {{step === 2 ? 'st__step--on' : ''}} {{step === 3 ? 'st__step--done' : ''}}">
					<view class="st__dot"><text class="st__dot-t">2</text></view>
					<text class="st__step-t">完善信息</text>
				</view>
				<view class="st__line {{step === 3 ? 'st__line--on' : ''}}"></view>
				<view class="st__step" :class="{ 'st__step--on': step === 3 }">
					<view class="st__dot"><text class="st__dot-t">3</text></view>
					<text class="st__step-t">完成</text>
				</view>
			</view>
		</view>

		<!-- 步骤1：学校 + 兴趣 -->
		<view v-if="step === 1" class="st__body">
			<text class="st__title">完善校园信息</text>
			<text class="st__sub">开启你的 UNIDA 校园之旅</text>

			<view class="st__field">
				<view class="st__label-row">
					<image class="st__label-ico" src="/static/icons-dark/calendar.png" mode="aspectFit" />
					<text class="st__label">选择你的学校</text>
					<text class="st__req">*</text>
				</view>
				<view class="st__select" @click="onSchool">
					<text class="st__select-t" :class="{ 'st__select-t--ph': !school }">{{ school || '请选择所在学校' }}</text>
					<image class="st__select-arrow" src="/static/icons-dark/chevron.png" mode="aspectFit" />
				</view>
			</view>

			<view class="st__field">
				<view class="st__label-row">
					<image class="st__label-ico" src="/static/icons-dark/bulb.png" mode="aspectFit" />
					<text class="st__label">选择你的兴趣</text>
					<text class="st__label-sub">（可多选）</text>
				</view>
				<view class="st__interests">
					<view class="st__interest" v-for="(it, i) in interests" :key="i" :class="{ 'st__interest--on': it.on }" @click="onInterest(i)">
						<view class="st__interest-icon" :class="'st__interest-icon--' + it.tone">
							<image class="st__interest-img" :src="it.icon" mode="aspectFit" />
						</view>
						<text class="st__interest-label">{{ it.label }}</text>
					</view>
				</view>
			</view>

			<view class="st__footer">
				<view class="st__next" @click="onNext"><text class="st__next-t">下一步</text></view>
				<text class="st__skip" @click="onSkip">先看看，稍后再完善 ›</text>
			</view>
		</view>

		<!-- 步骤2：昵称头像 -->
		<view v-else-if="step === 2" class="st__body">
			<text class="st__title">完善个人资料</text>
			<text class="st__sub">让大家更快认识你</text>
			<view class="st__avatar-wrap" @click="onAvatar">
				<view class="st__avatar"><text class="st__avatar-ch">{{ nickFirst }}</text></view>
				<view class="st__avatar-tip"><image class="st__avatar-pen" src="/static/icons-dark/bulb.png" mode="aspectFit" /><text class="st__avatar-tip-t">点击更换头像</text></view>
			</view>
			<view class="st__field">
				<text class="st__label">昵称</text>
				<input class="st__input" :value="nickname" placeholder="给自己起个好听的名字" maxlength="16" @input="onNickname" />
				<text class="st__input-count">{{ nickname.length }}/16</text>
			</view>
			<view class="st__footer">
				<view class="st__next" @click="onFinish"><text class="st__next-t">完成</text></view>
			</view>
		</view>

		<!-- 步骤3：完成 -->
		<view v-else class="st__done">
			<image class="st__done-badge" src="/static/unida/bubbles/check-cap.webp" mode="aspectFit" />
			<text class="st__done-title">欢迎加入 UNIDA！</text>
			<text class="st__done-sub">在校园，找到和你同频的人</text>
			<view class="st__next st__next--inline" @click="enterApp"><text class="st__next-t">开启校园之旅</text></view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				step: 1,
				school: '',
				nickname: '',
				nickFirst: '我',
				interests: [
					{ label: '学习', icon: '/static/icons-dark/heart.png', tone: 'purple', on: false },
					{ label: '运动', icon: '/static/icons-dark/flame.png', tone: 'orange', on: false },
					{ label: '娱乐', icon: '/static/icons-dark/music.png', tone: 'pink', on: false },
					{ label: '教学', icon: '/static/icons-dark/bulb.png', tone: 'sky', on: false },
					{ label: '跑腿', icon: '/static/icons-dark/box.png', tone: 'green', on: false },
					{ label: '活动', icon: '/static/icons-dark/calendar.png', tone: 'sun', on: false }
				]
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onSchool() {
				const schools = ['阳光大学', '阳光大学 · 主校区', '城市学院'];
				uni.showActionSheet({ itemList: schools, success: (res) => { this.school = schools[res.tapIndex]; } });
			},
			onInterest(i) {
				this.interests = this.interests.map((x, j) => j === i ? { label: x.label, icon: x.icon, tone: x.tone, on: !x.on } : x);
			},
			onNext() {
				if (!this.school) { uni.showToast({ title: '请选择学校', icon: 'none' }); return; }
				const count = this.interests.filter((x) => x.on).length;
				if (count === 0) { uni.showToast({ title: '至少选一个兴趣', icon: 'none' }); return; }
				this.step = 2;
			},
			onNickname(e) {
				this.nickname = e.detail.value;
				this.nickFirst = e.detail.value ? e.detail.value.slice(0, 1) : '我';
			},
			onAvatar() { uni.showToast({ title: '头像上传待接入', icon: 'none' }); },
			onFinish() {
				if (!this.nickname.trim()) { uni.showToast({ title: '给自己起个昵称吧', icon: 'none' }); return; }
				this.step = 3;
			},
			onSkip() { this.enterApp(); },
			enterApp() { uni.reLaunch({ url: '/pages/home/home' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.st { min-height: 100vh; padding: 0 40rpx 60rpx; box-sizing: border-box; }

	.st__top { display: flex; align-items: center; }
	.st__back {
		width: 68rpx; height: 68rpx;
		background: $c-white;
		border-radius: 50%;
		box-shadow: $sh-card;
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.st__back-img { width: 32rpx; height: 32rpx; }
	.st__steps { flex: 1; display: flex; align-items: center; justify-content: center; margin-left: -68rpx; }
	.st__step { display: flex; flex-direction: column; align-items: center; }
	.st__dot {
		width: 48rpx; height: 48rpx;
		border-radius: 50%;
		background: $c-ice;
		display: flex; align-items: center; justify-content: center;
	}
	.st__dot-t { font-size: 24rpx; color: $c-white; font-family: $ff-num; font-weight: 700; }
	.st__step--on .st__dot, .st__step--done .st__dot { background: $g-cta; box-shadow: 0 6rpx 12rpx rgba(128, 92, 250, 0.26); }
	.st__step-t { margin-top: 8rpx; font-size: 20rpx; color: $t-tertiary; }
	.st__step--on .st__step-t, .st__step--done .st__step-t { color: $c-primary; font-weight: 600; }
	.st__line { width: 56rpx; height: 4rpx; background: $c-ice; margin: 0 10rpx 28rpx; }
	.st__line--on { background: $c-primary; }

	.st__body { margin-top: 56rpx; }
	.st__title { display: block; font-size: 40rpx; font-weight: 800; color: $c-ink; letter-spacing: 1rpx; }
	.st__sub { display: block; margin-top: 12rpx; font-size: 25rpx; color: $t-sub; }
	.st__field { margin-top: 48rpx; }
	.st__label-row { display: flex; align-items: center; margin-bottom: 20rpx; }
	.st__label-ico { width: 32rpx; height: 32rpx; margin-right: 10rpx; }
	.st__label { font-size: 28rpx; font-weight: 700; color: $c-ink; }
	.st__label-sub { margin-left: 10rpx; font-size: 22rpx; color: $t-tertiary; font-weight: 400; }
	.st__req { margin-left: 8rpx; font-size: 26rpx; color: $c-peach; }

	.st__select {
		height: 96rpx;
		background: $c-white;
		border-radius: $r-sm;
		padding: 0 28rpx;
		display: flex; align-items: center; justify-content: space-between;
		box-shadow: $sh-card;
		box-sizing: border-box;
	}
	.st__select-t { font-size: 28rpx; color: $t-main; }
	.st__select-t--ph { color: $t-tertiary; }
	.st__select-arrow { width: 30rpx; height: 30rpx; transform: rotate(90deg); opacity: 0.5; }

	.st__interests { display: flex; flex-wrap: wrap; }
	.st__interest {
		width: 30%;
		background: $c-white;
		border-radius: $r-sm;
		padding: 26rpx 8rpx;
		display: flex; flex-direction: column; align-items: center;
		border: 4rpx solid transparent;
		box-shadow: $sh-card;
		box-sizing: border-box;
		margin: 0 3.33% 20rpx 0;
	}
	.st__interest:nth-child(3n) { margin-right: 0; }
	.st__interest--on { border-color: $c-primary; background: rgba(128, 92, 250, 0.06); }
	.st__interest-icon { width: 72rpx; height: 72rpx; border-radius: 22rpx; display: flex; align-items: center; justify-content: center; }
	.st__interest-icon--purple { background: rgba(128, 92, 250, 0.13); }
	.st__interest-icon--orange { background: rgba(255, 155, 119, 0.16); }
	.st__interest-icon--pink { background: rgba(244, 114, 182, 0.14); }
	.st__interest-icon--sky { background: rgba(105, 185, 245, 0.14); }
	.st__interest-icon--green { background: rgba(41, 202, 131, 0.14); }
	.st__interest-icon--sun { background: rgba(255, 201, 79, 0.2); }
	.st__interest-img { width: 38rpx; height: 38rpx; }
	.st__interest-label { margin-top: 14rpx; font-size: 24rpx; color: $t-main; }
	.st__interest--on .st__interest-label { color: $c-primary; font-weight: 700; }

	.st__footer { margin-top: 56rpx; }
	.st__next {
		height: 96rpx;
		border-radius: $r-pill;
		background: $g-cta;
		box-shadow: 0 12rpx 24rpx rgba(128, 92, 250, 0.3);
		display: flex; align-items: center; justify-content: center;
	}
	.st__next--inline { margin-top: 60rpx; padding: 0 60rpx; }
	.st__next-t { font-size: 32rpx; color: $c-white; font-weight: 700; letter-spacing: 2rpx; }
	.st__skip { display: block; margin-top: 28rpx; text-align: center; font-size: 24rpx; color: $t-tertiary; }

	.st__avatar-wrap { display: flex; flex-direction: column; align-items: center; margin-top: 60rpx; }
	.st__avatar {
		width: 180rpx; height: 180rpx;
		border-radius: 50%;
		background: $g-brand;
		display: flex; align-items: center; justify-content: center;
		border: 8rpx solid $c-white;
		box-shadow: 0 10rpx 30rpx rgba(128, 92, 250, 0.24);
	}
	.st__avatar-ch { font-size: 72rpx; color: $c-white; font-weight: 800; }
	.st__avatar-tip { display: flex; align-items: center; margin-top: 16rpx; }
	.st__avatar-pen { width: 28rpx; height: 28rpx; margin-right: 8rpx; }
	.st__avatar-tip-t { font-size: 24rpx; color: $c-primary; }
	.st__input {
		width: 100%; height: 96rpx;
		background: $c-white;
		border-radius: $r-sm;
		padding: 0 28rpx;
		font-size: 28rpx;
		color: $t-main;
		box-shadow: $sh-card;
		box-sizing: border-box;
	}
	.st__input-count { display: block; margin-top: 10rpx; text-align: right; font-size: 21rpx; color: $t-tertiary; font-family: $ff-num; }

	.st__done { display: flex; flex-direction: column; align-items: center; margin-top: 120rpx; }
	.st__done-badge { width: 240rpx; height: 240rpx; }
	.st__done-title { margin-top: 32rpx; font-size: 40rpx; font-weight: 800; color: $c-ink; }
	.st__done-sub { margin-top: 14rpx; font-size: 26rpx; color: $t-sub; }
</style>
