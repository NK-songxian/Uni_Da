<template>
	<view class="pf unida-page">
		<view class="pf__safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 自绘顶栏 -->
		<view class="pf__nav">
			<view class="pf__back" @click="goBack"><image class="pf__back-img" src="/static/icons-dark/back.png" mode="aspectFit" /></view>
			<text class="pf__title">发布活动</text>
			<view class="pf__ph"></view>
		</view>

		<!-- banner -->
		<view class="pf__banner">
			<view class="pf__banner-txt">
				<text class="pf__banner-t">完善活动信息</text>
				<text class="pf__banner-s">让更多同频的同学看到你</text>
			</view>
			<image class="pf__banner-img" src="/static/unida/bubbles/cal-star-big.webp" mode="aspectFit" />
		</view>

		<!-- 表单卡 -->
		<view class="pf__form">
			<!-- 封面 -->
			<view class="pf__field">
				<text class="pf__label">活动封面</text>
				<view class="pf__upload" @click="onUpload">
					<image class="pf__upload-img" src="/static/icons-dark/plus.png" mode="aspectFit" />
					<text class="pf__upload-text">上传图片</text>
				</view>
			</view>
			<!-- 标题 -->
			<view class="pf__field">
				<text class="pf__label">活动标题 <text class="pf__req">*</text></text>
				<input class="pf__input" :value="title" @input="onTitle" placeholder="例如：周末一起看电影" maxlength="30" />
				<text class="pf__counter">{{ title.length }}/30</text>
			</view>
			<!-- 类型 -->
			<view class="pf__field">
				<text class="pf__label">活动类型 <text class="pf__req">*</text></text>
				<view class="pf__chips">
					<text v-for="(t, i) in typeList" :key="i" class="pf__chip" :class="{ 'pf__chip--on': type === t }" @click="onType(i)">{{ t }}</text>
				</view>
			</view>
			<!-- 描述 -->
			<view class="pf__field">
				<text class="pf__label">活动描述</text>
				<textarea class="pf__textarea" :value="desc" @input="onDesc" placeholder="介绍活动内容、参与要求…" maxlength="200"></textarea>
				<text class="pf__counter">{{ desc.length }}/200</text>
			</view>
			<!-- 快捷时间 -->
			<view class="pf__field">
				<text class="pf__label">开始时间 <text class="pf__req">*</text></text>
				<view class="pf__quick">
					<image v-for="(q, i) in quicks" :key="i" class="pf__quick-img" :src="q.icon" mode="heightFix" :class="{ 'pf__quick-img--on': quickIdx === i }" @click="onQuick(i)" />
				</view>
				<view class="pf__pick" @click="onPickTime">
					<text class="pf__pick-t">{{ time || '选一个具体时间' }}</text>
					<image class="pf__chev" src="/static/icons-dark/chevron.png" mode="aspectFit" />
				</view>
			</view>
			<!-- 地点 -->
			<view class="pf__field">
				<text class="pf__label">活动地点 <text class="pf__req">*</text></text>
				<view class="pf__chips">
					<text v-for="(p, i) in places" :key="i" class="pf__chip" :class="{ 'pf__chip--on': place === p }" @click="onPlace(i)">{{ p }}</text>
				</view>
			</view>
			<!-- 人数 -->
			<view class="pf__field pf__row">
				<text class="pf__label">参与人数</text>
				<view class="pf__num">
					<view class="pf__num-btn" :class="{ 'pf__num-btn--off': total === 2 }" @click="onMinus"><text class="pf__num-sym">−</text></view>
					<text class="pf__num-val">{{ total }}</text>
					<view class="pf__num-btn" :class="{ 'pf__num-btn--off': total === 100 }" @click="onPlus"><text class="pf__num-sym">＋</text></view>
				</view>
			</view>
			<!-- 费用 -->
			<view class="pf__field">
				<text class="pf__label">费用说明</text>
				<view class="pf__chips">
					<text v-for="(f, i) in fees" :key="i" class="pf__chip" :class="{ 'pf__chip--on': fee === f }" @click="onFee(i)">{{ f }}</text>
				</view>
				<input v-if="fee === '自定义'" class="pf__input pf__input--fee" :value="feeText" @input="onFeeText" placeholder="输入金额，如 ¥20" />
			</view>
		</view>

		<!-- 提交 -->
		<view class="pf__submit" @click="onSubmit">发布活动</view>
		<view class="pf__bottom-space"></view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				typeList: ['学习', '运动', '娱乐', '教学', '跑腿', '其他'],
				places: ['图书馆', '中心草坪', '北区驿站', '东门', '体育场'],
				fees: ['免费', 'AA', '自定义'],
				quicks: [
					{ icon: '/static/unida/bubbles/time-now.webp', text: '现在就开始' },
					{ icon: '/static/unida/bubbles/time-5m.webp', text: '5 分钟后' },
					{ icon: '/static/unida/bubbles/time-30m.webp', text: '30 分钟后' },
					{ icon: '/static/unida/bubbles/time-1h.webp', text: '1 小时后' }
				],
				quickIdx: -1,
				title: '',
				desc: '',
				type: '学习',
				time: '',
				place: '',
				total: 10,
				fee: '免费',
				feeText: ''
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onUpload() { uni.showToast({ title: '图片上传待接入', icon: 'none' }); },
			onTitle(e) { this.title = e.detail.value; },
			onDesc(e) { this.desc = e.detail.value; },
			onType(i) { this.type = this.typeList[i]; },
			onPlace(i) { this.place = this.places[i]; },
			onFee(i) { this.fee = this.fees[i]; },
			onFeeText(e) { this.feeText = e.detail.value; },
			onQuick(i) {
				this.quickIdx = i;
				this.time = this.quicks[i].text;
			},
			onPickTime() { uni.showToast({ title: '精确时间选择待接入', icon: 'none' }); },
			onMinus() { this.total = Math.max(2, this.total - 1); },
			onPlus() { this.total = Math.min(100, this.total + 1); },
			onSubmit() {
				if (!this.title) { uni.showToast({ title: '请填写活动标题', icon: 'none' }); return; }
				if (!this.time || !this.place) { uni.showToast({ title: '请选择时间和地点', icon: 'none' }); return; }
				uni.showToast({ title: '活动发布成功（演示）', icon: 'success' });
				setTimeout(() => uni.reLaunch({ url: '/pages/home/home' }), 1200);
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.pf { padding: 0 $page-x 80rpx; box-sizing: border-box; }

	/* ---------- 顶栏 ---------- */
	.pf__nav { height: 110rpx; display: flex; align-items: center; justify-content: space-between; }
	.pf__back {
		width: 68rpx; height: 68rpx;
		background: $c-white;
		border-radius: 50%;
		box-shadow: $sh-card;
		display: flex; align-items: center; justify-content: center;
	}
	.pf__back-img { width: 32rpx; height: 32rpx; }
	.pf__title { font-size: 34rpx; font-weight: 800; color: $c-ink; letter-spacing: 1rpx; }
	.pf__ph { width: 68rpx; }

	/* ---------- banner ---------- */
	.pf__banner {
		background: $g-brand;
		border-radius: $r-md;
		padding: 30rpx 32rpx;
		display: flex; align-items: center;
		box-shadow: $sh-float;
	}
	.pf__banner-txt { flex: 1; display: flex; flex-direction: column; }
	.pf__banner-t { font-size: 32rpx; font-weight: 800; color: $c-white; letter-spacing: 1rpx; }
	.pf__banner-s { margin-top: 10rpx; font-size: 22rpx; color: rgba(255, 255, 255, 0.85); }
	.pf__banner-img { width: 108rpx; height: 108rpx; flex-shrink: 0; }

	/* ---------- 表单卡 ---------- */
	.pf__form {
		margin-top: 24rpx;
		background: $c-white;
		border-radius: $r-lg;
		box-shadow: $sh-card;
		padding: 10rpx 28rpx;
	}
	.pf__field { padding: 26rpx 0; border-bottom: 2rpx solid $c-line; }
	.pf__field:last-child { border-bottom: none; }
	.pf__label { display: block; font-size: 27rpx; font-weight: 700; color: $t-main; }
	.pf__req { color: $c-peach; }

	.pf__input {
		margin-top: 16rpx;
		width: 100%;
		height: 76rpx;
		font-size: 26rpx;
		background: $c-mist;
		border-radius: $r-sm;
		padding: 0 22rpx;
		box-sizing: border-box;
	}
	.pf__input--fee { margin-top: 14rpx; }
	.pf__counter { display: block; text-align: right; margin-top: 8rpx; font-size: 20rpx; color: $t-tertiary; font-family: $ff-num; }
	.pf__textarea {
		margin-top: 16rpx;
		width: 100%;
		height: 170rpx;
		background: $c-mist;
		border-radius: $r-sm;
		padding: 20rpx 22rpx;
		font-size: 26rpx;
		line-height: 1.6;
		box-sizing: border-box;
	}

	.pf__upload {
		margin-top: 16rpx;
		width: 200rpx; height: 200rpx;
		border-radius: $r-sm;
		border: 3rpx dashed $c-purple-light;
		background: rgba(128, 92, 250, 0.05);
		display: flex; flex-direction: column; align-items: center; justify-content: center;
	}
	.pf__upload-img { width: 44rpx; height: 44rpx; opacity: 0.75; }
	.pf__upload-text { margin-top: 12rpx; font-size: 22rpx; color: $c-primary; }

	.pf__chips { display: flex; flex-wrap: wrap; margin-top: 16rpx; }
	.pf__chip {
		font-size: 24rpx;
		padding: 13rpx 28rpx;
		border-radius: $r-pill;
		background: $c-mist;
		color: $t-sub;
		margin: 0 14rpx 14rpx 0;
	}
	.pf__chip--on { background: $g-cta; color: $c-white; font-weight: 600; box-shadow: $sh-float; }

	.pf__quick { display: flex; justify-content: space-between; margin-top: 18rpx; }
	.pf__quick-img { height: 88rpx; width: 120rpx; border-radius: $r-sm; border: 4rpx solid transparent; box-sizing: border-box; }
	.pf__quick-img--on { border-color: $c-primary; background: rgba(128, 92, 250, 0.08); }
	.pf__pick {
		margin-top: 18rpx;
		height: 76rpx;
		background: $c-mist;
		border-radius: $r-sm;
		display: flex; align-items: center; justify-content: space-between;
		padding: 0 22rpx;
	}
	.pf__pick-t { font-size: 24rpx; color: $t-sub; }
	.pf__chev { width: 24rpx; height: 24rpx; opacity: 0.45; }

	.pf__row { display: flex; align-items: center; justify-content: space-between; }
	.pf__row .pf__label { flex-shrink: 0; }
	.pf__num { display: flex; align-items: center; }
	.pf__num-btn {
		width: 60rpx; height: 60rpx;
		border-radius: 50%;
		background: rgba(128, 92, 250, 0.1);
		display: flex; align-items: center; justify-content: center;
	}
	.pf__num-btn--off { opacity: 0.35; }
	.pf__num-sym { font-size: 34rpx; color: $c-primary; font-family: $ff-num; }
	.pf__num-val { font-family: $ff-num; font-size: 34rpx; font-weight: 800; color: $c-ink; min-width: 80rpx; text-align: center; }

	/* ---------- 提交 ---------- */
	.pf__submit {
		margin-top: 40rpx;
		height: 96rpx;
		border-radius: $r-pill;
		background: $g-cta;
		color: $c-white;
		font-size: 30rpx;
		font-weight: 700;
		letter-spacing: 2rpx;
		display: flex; align-items: center; justify-content: center;
		box-shadow: $sh-float;
	}
	.pf__submit:active { transform: scale(0.98); }

	.pf__bottom-space { height: 60rpx; }
</style>
