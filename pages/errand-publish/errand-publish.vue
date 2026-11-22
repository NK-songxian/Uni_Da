<template>
	<view class="ep unida-page">
		<view class="ep__safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 导航 -->
		<view class="ep__nav">
			<view class="ep__back" @click="goBack"><image class="ep__back-img" src="/static/icons-dark/back.png" mode="aspectFit" /></view>
			<text class="ep__title">发布跑腿需求</text>
			<view class="ep__ph"></view>
		</view>

		<!-- 类型 -->
		<view class="ep__card">
			<text class="ep__label">需求类型</text>
			<view class="ep__types">
				<view
					class="ep__type"
					v-for="(t, i) in types"
					:key="i"
					:class="{ 'ep__type--on': type === t }"
					@click="type = t"
				>
					<text class="ep__type-t">{{ t }}</text>
				</view>
			</view>
		</view>

		<!-- 标题 -->
		<view class="ep__card">
			<text class="ep__label">需求标题 <text class="ep__must">*</text></text>
			<input class="ep__input" :value="title" :maxlength="40" placeholder="例如：帮忙取个快递（中通北区）" @input="onInput('title', $event)" />
		</view>

		<!-- 描述 -->
		<view class="ep__card">
			<text class="ep__label">需求描述</text>
			<textarea class="ep__area" :value="desc" :maxlength="300" placeholder="写清楚要求，接单同学做得更快（选填）" @input="onInput('desc', $event)" />
		</view>

		<!-- 地点 -->
		<view class="ep__card">
			<view class="ep__row">
				<view class="ep__col">
					<text class="ep__label">取件 / 争取地点</text>
					<input class="ep__input" :value="pickup" :maxlength="40" placeholder="例如：北区快递驿站" @input="onInput('pickup', $event)" />
				</view>
			</view>
			<view class="ep__row">
				<view class="ep__col">
					<text class="ep__label">送达地点</text>
					<input class="ep__input" :value="delivery" :maxlength="40" placeholder="例如：东园 6 栋 307" @input="onInput('delivery', $event)" />
				</view>
			</view>
		</view>

		<!-- 赏金 + 限时 -->
		<view class="ep__card">
			<view class="ep__row">
				<view class="ep__col">
					<text class="ep__label">赏金（元）<text class="ep__must">*</text></text>
					<input class="ep__input ep__input--num" type="digit" :value="reward" placeholder="8" @input="onInput('reward', $event)" />
				</view>
				<view class="ep__col">
					<text class="ep__label">期望完成时间</text>
					<input class="ep__input" :value="deadline" :maxlength="30" placeholder="例如：今天 18:00 前" @input="onInput('deadline', $event)" />
				</view>
			</view>
			<text class="ep__hint">第一版不接入在线支付，赏金为线下结算，请完成后当面支付</text>
		</view>

		<!-- 提交 -->
		<view class="ep__submit" :class="{ 'ep__submit--off': !canSubmit || busy }" @click="submit">
			<text class="ep__submit-t">{{ busy ? '发布中…' : '发布需求' }}</text>
		</view>
		<view class="ep__bottom-space"></view>
	</view>
</template>

<script>
	import { callCloud, getToken } from '@/common/cloud.js';

	export default {
		data() {
			return {
				statusBar: 0,
				types: ['快递代取', '外卖代拿', '物品代送', '其他互助'],
				type: '快递代取',
				title: '',
				desc: '',
				pickup: '',
				delivery: '',
				reward: '',
				deadline: '',
				busy: false
			};
		},
		computed: {
			canSubmit() {
				return !!(this.title.trim() && Number(this.reward) > 0);
			}
		},
		onLoad(q) {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
			if (q && q.type && this.types.indexOf(decodeURIComponent(q.type)) >= 0) {
				this.type = decodeURIComponent(q.type);
			}
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onInput(key, e) { this[key] = e.detail.value; },
			async submit() {
				if (!this.canSubmit || this.busy) return;
				this.busy = true;
				try {
					await callCloud('errand', {
						action: 'publish',
						token: getToken(),
						type: this.type,
						title: this.title.trim(),
						desc: this.desc.trim(),
						pickup: this.pickup.trim(),
						delivery: this.delivery.trim(),
						reward: Number(this.reward),
						deadline: this.deadline.trim()
					});
					uni.showToast({ title: '发布成功，等同学接单', icon: 'success' });
					setTimeout(() => {
						uni.redirectTo({ url: '/pages/my-errands/my-errands?role=published' });
					}, 900);
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '发布失败', icon: 'none' });
					this.busy = false;
				}
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.ep { padding: 0 $page-x 60rpx; box-sizing: border-box; }

	.ep__nav { height: 110rpx; display: flex; align-items: center; justify-content: space-between; }
	.ep__back {
		width: 68rpx; height: 68rpx;
		background: $c-white;
		border-radius: 50%;
		box-shadow: $sh-card;
		display: flex; align-items: center; justify-content: center;
	}
	.ep__back-img { width: 32rpx; height: 32rpx; }
	.ep__title { font-size: 34rpx; font-weight: 800; color: $c-ink; letter-spacing: 1rpx; }
	.ep__ph { width: 68rpx; }

	.ep__card {
		margin-top: 20rpx;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 26rpx 28rpx;
	}
	.ep__label { display: block; font-size: 26rpx; font-weight: 700; color: $t-main; }
	.ep__must { color: #E86154; }
	.ep__types { display: flex; flex-wrap: wrap; margin-top: 18rpx; }
	.ep__type {
		padding: 14rpx 30rpx;
		border-radius: $r-pill;
		background: $c-mist;
		margin: 0 16rpx 14rpx 0;
	}
	.ep__type--on { background: $g-brand; box-shadow: 0 8rpx 16rpx rgba(128, 92, 250, 0.28); }
	.ep__type-t { font-size: 24rpx; color: $t-sub; font-weight: 600; }
	.ep__type--on .ep__type-t { color: $c-white; font-weight: 700; }
	.ep__input {
		margin-top: 16rpx;
		width: 100%;
		box-sizing: border-box;
		height: 84rpx;
		background: $c-mist;
		border-radius: 18rpx;
		padding: 0 26rpx;
		font-size: 27rpx;
		color: $t-main;
	}
	.ep__input--num { font-family: $ff-num; }
	.ep__area {
		margin-top: 16rpx;
		width: 100%;
		box-sizing: border-box;
		height: 180rpx;
		background: $c-mist;
		border-radius: 18rpx;
		padding: 24rpx 26rpx;
		font-size: 27rpx;
		color: $t-main;
	}
	.ep__row { display: flex; margin-top: 16rpx; }
	.ep__row:first-of-type { margin-top: 0; }
	.ep__col { flex: 1; min-width: 0; }
	.ep__col + .ep__col { margin-left: 20rpx; }
	.ep__hint { display: block; margin-top: 16rpx; font-size: 21rpx; color: $t-tertiary; line-height: 1.6; }

	.ep__submit {
		margin-top: 36rpx;
		height: 96rpx;
		border-radius: $r-pill;
		background: $g-cta;
		display: flex; align-items: center; justify-content: center;
		box-shadow: $sh-float;
	}
	.ep__submit--off { opacity: 0.5; }
	.ep__submit-t { font-size: 30rpx; color: $c-white; font-weight: 700; letter-spacing: 2rpx; }

	.ep__bottom-space { height: 40rpx; }
</style>
