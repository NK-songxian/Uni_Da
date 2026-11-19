<template>
	<view class="pf unida-page">
		<view class="pf__nav"><text class="pf__back" @click="goBack">‹</text><text class="pf__title">发布活动</text><text class="pf__ph"></text></view>

		<view class="pf__banner">
			<text class="pf__banner-icon">🎪</text>
			<text class="pf__banner-title">完善活动信息</text>
			<text class="pf__banner-sub">让更多同学看到你的活动 ✨</text>
		</view>

		<view class="pf__form unida-card">
			<!-- 上传封面 -->
			<view class="pf__field">
				<text class="pf__label">活动封面</text>
				<view class="pf__upload" @click="onUpload"><text class="pf__upload-icon">＋</text><text class="pf__upload-text">上传图片</text></view>
			</view>
			<!-- 标题 -->
			<view class="pf__field">
				<text class="pf__label">活动标题 <text class="pf__req">*</text></text>
				<input class="pf__input" v-model="form.title" placeholder="例如：周末一起看电影" maxlength="30" />
				<text class="pf__counter">{{ form.title.length }}/30</text>
			</view>
			<!-- 类型 -->
			<view class="pf__field">
				<text class="pf__label">活动类型 <text class="pf__req">*</text></text>
				<view class="pf__types">
					<text v-for="(t, i) in types" :key="i" class="pf__type" :class="{ 'pf__type--on': form.type === t }" @click="form.type = t">{{ t }}</text>
				</view>
			</view>
			<!-- 描述 -->
			<view class="pf__field">
				<text class="pf__label">活动描述</text>
				<textarea class="pf__textarea" v-model="form.desc" placeholder="介绍活动内容、参与要求…" maxlength="200"></textarea>
			</view>
			<!-- 时间 -->
			<view class="pf__field pf__field--row" @click="onPickTime">
				<text class="pf__label">活动时间 <text class="pf__req">*</text></text>
				<view class="pf__picker"><text>{{ form.time || '请选择' }}</text><text>›</text></view>
			</view>
			<!-- 地点 -->
			<view class="pf__field pf__field--row" @click="onPickPlace">
				<text class="pf__label">活动地点 <text class="pf__req">*</text></text>
				<view class="pf__picker"><text>{{ form.place || '请选择' }}</text><text>›</text></view>
			</view>
			<!-- 人数 -->
			<view class="pf__field pf__field--row">
				<text class="pf__label">参与人数</text>
				<view class="pf__num">
					<text class="pf__num-btn" @click="form.total = Math.max(2, form.total - 1)">−</text>
					<text class="pf__num-val">{{ form.total }}</text>
					<text class="pf__num-btn" @click="form.total = Math.min(100, form.total + 1)">＋</text>
				</view>
			</view>
			<!-- 费用 -->
			<view class="pf__field">
				<text class="pf__label">费用说明</text>
				<input class="pf__input" v-model="form.fee" placeholder="例如：免费 / AA / ¥20" />
			</view>
		</view>

		<view class="pf__submit" @click="onSubmit">发布活动</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				types: ['学习', '运动', '娱乐', '教学', '跑腿', '活动'],
				form: { title: '', type: '活动', desc: '', time: '', place: '', total: 10, fee: '免费' }
			};
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onUpload() { uni.showToast({ title: '图片上传待接入', icon: 'none' }); },
			onPickTime() { uni.navigateTo({ url: '/pages/pick-time/pick-time' }); },
			onPickPlace() { uni.navigateTo({ url: '/pages/pick-place/pick-place' }); },
			onSubmit() {
				if (!this.form.title) { uni.showToast({ title: '请填写活动标题', icon: 'none' }); return; }
				if (!this.form.time || !this.form.place) { uni.showToast({ title: '请选择时间和地点', icon: 'none' }); return; }
				uni.showToast({ title: '活动发布成功（演示）', icon: 'success' });
				setTimeout(() => uni.reLaunch({ url: '/pages/home/home' }), 1200);
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.pf { padding: 0 24rpx 80rpx; }
	.pf__nav { height: 120rpx; padding-top: 60rpx; display: flex; align-items: center; justify-content: space-between; }
	.pf__back { font-size: 48rpx; width: 60rpx; }
	.pf__title { font-size: 32rpx; font-weight: 700; }
	.pf__ph { width: 60rpx; }
	.pf__banner { border-radius: 24rpx; background: linear-gradient(135deg,#7B61FF,#B59BFF); padding: 32rpx; display: flex; flex-direction: column; color: #fff; }
	.pf__banner-icon { font-size: 56rpx; }
	.pf__banner-title { margin-top: 12rpx; font-size: 34rpx; font-weight: 800; }
	.pf__banner-sub { margin-top: 8rpx; font-size: 24rpx; opacity: 0.9; }
	.pf__form { margin-top: 20rpx; padding: 12rpx 28rpx; }
	.pf__field { padding: 24rpx 0; border-bottom: 2rpx solid $unida-divider; }
	.pf__field:last-child { border-bottom: none; }
	.pf__label { display: block; font-size: 28rpx; font-weight: 700; color: $unida-text; }
	.pf__req { color: $unida-orange; }
	.pf__input { margin-top: 16rpx; width: 100%; height: 72rpx; font-size: 26rpx; background: $unida-bg; border-radius: 14rpx; padding: 0 20rpx; }
	.pf__counter { display: block; text-align: right; margin-top: 8rpx; font-size: 20rpx; color: $unida-text-sub; }
	.pf__upload { margin-top: 16rpx; width: 200rpx; height: 200rpx; border-radius: 20rpx; border: 4rpx dashed #c9bdf5; background: rgba(123,97,255,0.04); display: flex; flex-direction: column; align-items: center; justify-content: center; }
	.pf__upload-icon { font-size: 64rpx; color: $unida-primary; line-height: 1; }
	.pf__upload-text { margin-top: 12rpx; font-size: 24rpx; color: $unida-primary; }
	.pf__types { display: flex; flex-wrap: wrap; gap: 14rpx; margin-top: 16rpx; }
	.pf__type { font-size: 24rpx; padding: 12rpx 26rpx; border-radius: 999rpx; background: $unida-bg; color: $unida-text-sub; }
	.pf__type--on { background: linear-gradient(135deg,#7B61FF,#B59BFF); color: #fff; }
	.pf__textarea { margin-top: 16rpx; width: 100%; height: 180rpx; background: $unida-bg; border-radius: 14rpx; padding: 20rpx; font-size: 26rpx; line-height: 1.6; }
	.pf__field--row { display: flex; align-items: center; justify-content: space-between; }
	.pf__field--row .pf__label { flex-shrink: 0; }
	.pf__picker { display: flex; align-items: center; gap: 12rpx; font-size: 26rpx; color: $unida-text-sub; }
	.pf__num { display: flex; align-items: center; gap: 24rpx; }
	.pf__num-btn { width: 56rpx; height: 56rpx; border-radius: 50%; background: rgba(123,97,255,0.1); color: $unida-primary; font-size: 32rpx; display: flex; align-items: center; justify-content: center; }
	.pf__num-val { font-size: 30rpx; font-weight: 700; color: $unida-text; min-width: 40rpx; text-align: center; }
	.pf__submit { margin-top: 40rpx; height: 92rpx; border-radius: 999rpx; background: linear-gradient(135deg,#7B61FF,#B59BFF); color: #fff; font-size: 30rpx; font-weight: 700; display: flex; align-items: center; justify-content: center; box-shadow: 0 10rpx 24rpx rgba(123,97,255,0.28); }
</style>
