<template>
	<view class="setup unida-page">
		<!-- 3步进度条 -->
		<view class="setup__top">
			<navigator class="setup__back" open-type="navigateBack" delta="1">‹</navigator>
			<view class="setup__steps">
				<view class="setup__step" :class="{ 'setup__step--active': step >= 1 }">
					<view class="setup__step-dot">1</view><text>校园验证</text>
				</view>
				<view class="setup__line" :class="{ 'setup__line--on': step >= 2 }"></view>
				<view class="setup__step" :class="{ 'setup__step--active': step >= 2 }">
					<view class="setup__step-dot">2</view><text>完善信息</text>
				</view>
				<view class="setup__line" :class="{ 'setup__line--on': step >= 3 }"></view>
				<view class="setup__step" :class="{ 'setup__step--active': step >= 3 }">
					<view class="setup__step-dot">3</view><text>完成</text>
				</view>
			</view>
		</view>

		<!-- 步骤1：学校 + 兴趣 -->
		<view v-if="step === 1" class="setup__body">
			<text class="setup__title">完善校园信息</text>
			<text class="setup__sub">开启你的 UNIDA 校园之旅 🎉</text>

			<view class="setup__field">
				<text class="setup__label">🎓 选择你的学校 <text class="setup__req">*</text></text>
				<view class="setup__select" @click="onSchool">
					<text>{{ school || '请选择所在学校' }}</text><text class="setup__select-arrow">▾</text>
				</view>
			</view>

			<view class="setup__field">
				<text class="setup__label">✨ 选择你的兴趣 <text class="setup__hint">（可多选）</text></text>
				<view class="setup__interests">
					<view
						class="setup__interest"
						v-for="(it, i) in interests"
						:key="i"
						:class="{ 'setup__interest--on': selected.includes(it.label) }"
						@click="toggleInterest(it.label)"
					>
						<text class="setup__interest-icon">{{ it.icon }}</text>
						<text class="setup__interest-label">{{ it.label }}</text>
					</view>
				</view>
			</view>

			<view class="setup__footer">
				<view class="setup__next" @click="onNext">下一步</view>
				<text class="setup__skip" @click="onSkip">先看看，稍后再完善 ›</text>
			</view>
		</view>

		<!-- 步骤2：昵称头像 -->
		<view v-else-if="step === 2" class="setup__body">
			<text class="setup__title">完善个人资料</text>
			<text class="setup__sub">让大家更快认识你 😊</text>
			<view class="setup__avatar-wrap" @click="onAvatar">
				<view class="setup__avatar">{{ avatar }}</view>
				<text class="setup__avatar-tip">点击更换头像</text>
			</view>
			<view class="setup__field">
				<text class="setup__label">昵称</text>
				<input class="setup__input" v-model="nickname" placeholder="给自己起个好听的名字" maxlength="16" />
			</view>
			<view class="setup__footer">
				<view class="setup__next" @click="step = 3">完成</view>
			</view>
		</view>

		<!-- 步骤3：完成 -->
		<view v-else class="setup__done">
			<text class="setup__done-emoji">🎉</text>
			<text class="setup__done-title">欢迎加入 UNIDA！</text>
			<text class="setup__done-sub">在校园，找到和你同频的人</text>
			<view class="setup__next setup__next--inline" @click="enterApp">开启校园之旅</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				step: 1,
				school: '',
				selected: [],
				avatar: '😄',
				nickname: '',
				interests: [
					{ icon: '📚', label: '学习' }, { icon: '🏃', label: '运动' }, { icon: '🎮', label: '娱乐' },
					{ icon: '📖', label: '教学' }, { icon: '🛵', label: '跑腿' }, { icon: '🎪', label: '活动' }
				]
			};
		},
		methods: {
			onSchool() {
				const schools = ['阳光大学', '阳光大学 · 主校区', '城市学院'];
				uni.showActionSheet({ itemList: schools, success: (res) => { this.school = schools[res.tapIndex]; } });
			},
			toggleInterest(label) {
				const i = this.selected.indexOf(label);
				if (i >= 0) this.selected.splice(i, 1);
				else this.selected.push(label);
			},
			onNext() {
				if (!this.school) { uni.showToast({ title: '请选择学校', icon: 'none' }); return; }
				if (!this.selected.length) { uni.showToast({ title: '至少选一个兴趣', icon: 'none' }); return; }
				this.step = 2;
			},
			onAvatar() { uni.showToast({ title: '头像上传待接入', icon: 'none' }); },
			onSkip() { this.enterApp(); },
			enterApp() { uni.reLaunch({ url: '/pages/home/home' }); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.setup { min-height: 100vh; padding: 0 40rpx 60rpx; }
	.setup__top { display: flex; align-items: center; padding-top: 70rpx; }
	.setup__back { font-size: 48rpx; color: $unida-text; width: 60rpx; }
	.setup__steps { flex: 1; display: flex; align-items: center; justify-content: center; margin-right: 60rpx; }
	.setup__step { display: flex; flex-direction: column; align-items: center; font-size: 20rpx; color: $unida-text-sub; }
	.setup__step-dot { width: 44rpx; height: 44rpx; border-radius: 50%; background: #e5dffa; color: #fff; font-size: 24rpx; display: flex; align-items: center; justify-content: center; margin-bottom: 8rpx; }
	.setup__step--active .setup__step-dot { background: linear-gradient(135deg,#7B61FF,#B59BFF); }
	.setup__step--active { color: $unida-primary; }
	.setup__line { width: 60rpx; height: 4rpx; background: #e5dffa; margin: 0 10rpx 28rpx; }
	.setup__line--on { background: $unida-primary; }
	.setup__body { margin-top: 70rpx; }
	.setup__title { display: block; font-size: 40rpx; font-weight: 800; color: $unida-text; }
	.setup__sub { display: block; margin-top: 12rpx; font-size: 26rpx; color: $unida-text-sub; }
	.setup__field { margin-top: 56rpx; }
	.setup__label { display: block; font-size: 28rpx; font-weight: 700; color: $unida-text; margin-bottom: 20rpx; }
	.setup__req { color: $unida-orange; }
	.setup__hint { font-size: 22rpx; color: $unida-text-sub; font-weight: 400; }
	.setup__select { height: 96rpx; background: #fff; border-radius: 20rpx; padding: 0 28rpx; display: flex; align-items: center; justify-content: space-between; font-size: 28rpx; color: $unida-text; box-shadow: 0 6rpx 20rpx rgba(123,97,255,0.06); }
	.setup__select-arrow { color: $unida-text-sub; }
	.setup__interests { display: flex; flex-wrap: wrap; gap: 20rpx; }
	.setup__interest { width: 30%; background: #fff; border-radius: 24rpx; padding: 30rpx 8rpx; display: flex; flex-direction: column; align-items: center; border: 4rpx solid transparent; box-shadow: 0 6rpx 20rpx rgba(123,97,255,0.06); }
	.setup__interest--on { border-color: $unida-primary; background: rgba(123,97,255,0.06); }
	.setup__interest-icon { font-size: 52rpx; }
	.setup__interest-label { margin-top: 14rpx; font-size: 24rpx; color: $unida-text; }
	.setup__footer { margin-top: 80rpx; }
	.setup__next { height: 96rpx; border-radius: 999rpx; background: linear-gradient(135deg,#7B61FF,#B59BFF); color: #fff; font-size: 32rpx; font-weight: 700; display: flex; align-items: center; justify-content: center; box-shadow: 0 12rpx 28rpx rgba(123,97,255,0.3); }
	.setup__next--inline { margin-top: 60rpx; padding: 0 60rpx; }
	.setup__skip { display: block; margin-top: 28rpx; text-align: center; font-size: 24rpx; color: $unida-text-sub; }
	.setup__avatar-wrap { display: flex; flex-direction: column; align-items: center; margin-top: 60rpx; }
	.setup__avatar { width: 180rpx; height: 180rpx; border-radius: 50%; background: linear-gradient(135deg,#B59BFF,#7B61FF); display: flex; align-items: center; justify-content: center; font-size: 96rpx; border: 8rpx solid #fff; box-shadow: 0 10rpx 30rpx rgba(123,97,255,0.2); }
	.setup__avatar-tip { margin-top: 16rpx; font-size: 24rpx; color: $unida-primary; }
	.setup__input { height: 96rpx; background: #fff; border-radius: 20rpx; padding: 0 28rpx; font-size: 28rpx; box-shadow: 0 6rpx 20rpx rgba(123,97,255,0.06); }
	.setup__done { display: flex; flex-direction: column; align-items: center; margin-top: 200rpx; }
	.setup__done-emoji { font-size: 160rpx; }
	.setup__done-title { margin-top: 30rpx; font-size: 40rpx; font-weight: 800; color: $unida-text; }
	.setup__done-sub { margin-top: 14rpx; font-size: 26rpx; color: $unida-text-sub; }
</style>
