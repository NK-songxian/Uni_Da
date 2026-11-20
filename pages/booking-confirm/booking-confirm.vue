<template>
	<view class="bc unida-page">
		<!-- ══════════ 自绘顶栏（含状态栏安全区） ══════════ -->
		<view class="bc__nav" :style="{ paddingTop: statusBar + 'px' }">
			<view class="bc__nav-btn" @click="goBack">
				<image class="bc__nav-ico" src="/static/icons-dark/back.png" mode="aspectFit" />
			</view>
			<text class="bc__nav-title">报名确认</text>
			<view class="bc__nav-btn"></view>
		</view>

		<!-- ══════════ 活动卡（小封面 + 摘要） ══════════ -->
		<view class="bc__act">
			<image class="bc__act-cover" src="/static/art/art-guitar.jpg" mode="aspectFill" />
			<view class="bc__act-body">
				<text class="bc__act-title">校园草地音乐会 · 一起嗨翻周末</text>
				<view class="bc__act-meta">
					<image class="bc__act-ico" src="/static/icons-dark/clock.png" mode="aspectFit" />
					<text class="bc__act-t">本周六 19:00 - 21:00</text>
				</view>
				<view class="bc__act-meta">
					<image class="bc__act-ico" src="/static/icons-dark/pin.png" mode="aspectFit" />
					<text class="bc__act-t">中心草坪广场</text>
				</view>
			</view>
		</view>

		<!-- ══════════ 预约信息 ══════════ -->
		<view class="bc__card">
			<view class="bc__sec-title">预约信息</view>
			<view class="bc__row">
				<text class="bc__row-k">预约时间</text>
				<text class="bc__row-v">本周六 19:00</text>
			</view>
			<view class="bc__row">
				<text class="bc__row-k">参与人数</text>
				<view class="bc__stepper">
					<view class="bc__step" :class="{ 'bc__step--off': count === 1 }" @click="decCount">
						<view class="bc__step-bar"></view>
					</view>
					<text class="bc__step-num">{{ count }}</text>
					<view class="bc__step" :class="{ 'bc__step--off': count >= 6 }" @click="incCount">
						<image class="bc__step-plus" src="/static/icons-dark/plus.png" mode="aspectFit" />
					</view>
				</view>
			</view>
			<view class="bc__row">
				<text class="bc__row-k">联系电话</text>
				<text class="bc__row-v">138****8888</text>
			</view>
		</view>

		<!-- ══════════ 参与备注 ══════════ -->
		<view class="bc__card">
			<view class="bc__sec-title">参与备注<text class="bc__opt">（选填）</text></view>
			<textarea
				class="bc__ta"
				:value="remark"
				@input="onRemark"
				placeholder="想对发起人说什么？例如：我会弹吉他～"
				placeholder-class="bc__ta-ph"
				maxlength="100"
			/>
			<text class="bc__count">{{ remarkLen }}/100</text>
		</view>

		<!-- ══════════ 温馨提示 ══════════ -->
		<view class="bc__notice">
			<image class="bc__notice-ico" src="/static/icons-dark/bulb.png" mode="aspectFit" />
			<text class="bc__notice-t">本活动免费，现场零食饮料 AA 自愿参与。请准时到场，如需取消请提前 2 小时操作。</text>
		</view>

		<!-- ══════════ 底部提交 ══════════ -->
		<view class="bc__bottom">
			<view class="bc__agree" @click="toggleAgree">
				<view class="bc__cb" :class="{ 'bc__cb--on': agreed }">
					<view v-if="agreed" class="bc__cb-tick"></view>
				</view>
				<text class="bc__agree-t">我已阅读并同意活动参与须知</text>
			</view>
			<view class="bc__submit" :class="{ 'bc__submit--off': !agreed }" @click="onSubmit">
				<text class="bc__submit-t">提交报名</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				count: 1,
				remark: '',
				remarkLen: 0,
				agreed: true
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = (sys && sys.statusBarHeight) || 0;
		},
		methods: {
			goBack() { uni.navigateBack(); },
			incCount() {
				if (this.count < 6) this.count += 1;
			},
			decCount() {
				if (this.count > 1) this.count -= 1;
			},
			onRemark(e) {
				const v = e.detail.value || '';
				this.remark = v;
				this.remarkLen = v.length;
			},
			toggleAgree() { this.agreed = !this.agreed; },
			onSubmit() {
				if (!this.agreed) {
					uni.showToast({ title: '请先同意活动参与须知', icon: 'none' });
					return;
				}
				uni.navigateTo({ url: '/pages/booking-success/booking-success' });
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.bc { padding-bottom: calc(220rpx + env(safe-area-inset-bottom)); }

	/* ══════════ 顶栏 ══════════ */
	.bc__nav {
		display: flex; align-items: center; justify-content: space-between;
		padding-left: $page-x; padding-right: $page-x; padding-bottom: 16rpx;
		background: $c-mist;
	}
	.bc__nav-btn {
		width: 64rpx; height: 64rpx; border-radius: 50%;
		display: flex; align-items: center; justify-content: center;
	}
	.bc__nav-ico { width: 40rpx; height: 40rpx; }
	.bc__nav-title {
		font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink; letter-spacing: 0.5rpx;
	}

	/* ══════════ 活动卡 ══════════ */
	.bc__act {
		display: flex; margin: 8rpx $page-x 0;
		padding: 20rpx; border-radius: $r-lg;
		background: #fff; box-shadow: $sh-card;
	}
	.bc__act-cover {
		width: 180rpx; height: 180rpx; border-radius: $r-md; flex-shrink: 0;
		background: $c-ice;
	}
	.bc__act-body { flex: 1; margin-left: 22rpx; display: flex; flex-direction: column; }
	.bc__act-title {
		font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink;
		line-height: 1.42; letter-spacing: -0.5rpx;
	}
	.bc__act-meta { display: flex; align-items: center; margin-top: 12rpx; }
	.bc__act-ico { width: 26rpx; height: 26rpx; opacity: 0.5; flex-shrink: 0; }
	.bc__act-t { margin-left: 10rpx; font-size: $fs-caption; color: $t-sub; letter-spacing: 0.2rpx; }

	/* ══════════ 通用卡片 ══════════ */
	.bc__card { margin: 24rpx $page-x 0; padding: 28rpx; border-radius: $r-lg; background: #fff; box-shadow: $sh-card; }
	.bc__sec-title { font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink; letter-spacing: -0.3rpx; }
	.bc__opt { font-size: $fs-caption; font-weight: $fw-regular; color: $t-tertiary; }

	/* 信息行 */
	.bc__row {
		display: flex; align-items: center; justify-content: space-between;
		padding: 22rpx 0; border-bottom: 2rpx solid $c-line;
	}
	.bc__row:first-of-type { margin-top: 8rpx; }
	.bc__row:last-child { border-bottom: none; padding-bottom: 0; }
	.bc__row-k { font-size: $fs-body; color: $t-sub; letter-spacing: 0.2rpx; }
	.bc__row-v { font-size: $fs-body; font-weight: $fw-semibold; color: $c-ink; letter-spacing: -0.2rpx; }

	/* 人数步进器 */
	.bc__stepper { display: flex; align-items: center; }
	.bc__step {
		width: 52rpx; height: 52rpx; border-radius: 50%;
		background: rgba(128,92,250,0.10);
		display: flex; align-items: center; justify-content: center;
	}
	.bc__step--off { opacity: 0.32; }
	.bc__step-bar { width: 22rpx; height: 4rpx; border-radius: 4rpx; background: $c-primary; }
	.bc__step-plus { width: 24rpx; height: 24rpx; }
	.bc__step-num {
		min-width: 64rpx; text-align: center;
		font-family: $ff-num; font-size: $fs-h3; font-weight: $fw-bold; color: $c-ink;
	}

	/* 备注 */
	.bc__ta {
		display: block; width: 100%; height: 168rpx; margin-top: 20rpx;
		padding: 20rpx; border-radius: $r-md; box-sizing: border-box;
		background: $c-mist;
		font-size: $fs-body; color: $t-main; line-height: 1.6;
	}
	.bc__ta-ph { color: $t-tertiary; font-size: $fs-body; }
	.bc__count { display: block; text-align: right; margin-top: 10rpx; font-family: $ff-num; font-size: $fs-micro; color: $t-tertiary; }

	/* ══════════ 提示 ══════════ */
	.bc__notice {
		display: flex; align-items: flex-start; margin: 24rpx $page-x 0;
		padding: 22rpx 24rpx; border-radius: $r-md;
		background: rgba(255,201,79,0.14);
	}
	.bc__notice-ico { width: 32rpx; height: 32rpx; flex-shrink: 0; margin-top: 2rpx; }
	.bc__notice-t { flex: 1; margin-left: 14rpx; font-size: $fs-caption; color: #8A6A18; line-height: 1.62; letter-spacing: 0.2rpx; }

	/* ══════════ 底部 ══════════ */
	.bc__bottom {
		position: fixed; left: 0; right: 0; bottom: 0; z-index: 60;
		padding: 18rpx $page-x;
		padding-bottom: calc(18rpx + env(safe-area-inset-bottom));
		background: rgba(255,255,255,0.97);
		box-shadow: 0 -6rpx 24rpx rgba(123,97,255,0.08);
	}
	.bc__agree { display: flex; align-items: center; justify-content: center; margin-bottom: 16rpx; }
	.bc__cb {
		width: 32rpx; height: 32rpx; border-radius: 50%; flex-shrink: 0;
		border: 2rpx solid #C9C2DD; box-sizing: border-box;
		display: flex; align-items: center; justify-content: center;
		transition: background 0.2s ease, border-color 0.2s ease;
	}
	.bc__cb--on { background: $c-primary; border-color: $c-primary; }
	/* 对勾用两条旋转边框画，不用字符 */
	.bc__cb-tick {
		width: 18rpx; height: 10rpx; margin-top: -4rpx;
		border-left: 4rpx solid #fff; border-bottom: 4rpx solid #fff;
		transform: rotate(-45deg);
	}
	.bc__agree-t { margin-left: 10rpx; font-size: $fs-micro; color: $t-sub; letter-spacing: 0.2rpx; }
	.bc__submit {
		height: 92rpx; border-radius: $r-pill;
		background: $g-cta; box-shadow: $sh-float;
		display: flex; align-items: center; justify-content: center;
		transition: opacity 0.2s ease;
	}
	.bc__submit--off { opacity: 0.5; box-shadow: none; }
	.bc__submit-t { font-size: $fs-h3; font-weight: $fw-bold; color: #fff; letter-spacing: 2rpx; }
</style>
