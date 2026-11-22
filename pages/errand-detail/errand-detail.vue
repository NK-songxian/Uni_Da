<template>
	<view class="ed unida-page">
		<view class="ed__safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 导航 -->
		<view class="ed__nav">
			<view class="ed__back" @click="goBack"><image class="ed__back-img" src="/static/icons-dark/back.png" mode="aspectFit" /></view>
			<text class="ed__title">跑腿订单详情</text>
			<view class="ed__ph"></view>
		</view>

		<!-- 状态卡 -->
		<view class="ed__status">
			<image class="ed__status-img" src="/static/unida/bubbles/catering-pin.webp" mode="aspectFit" />
			<view class="ed__status-info">
				<text class="ed__status-title">{{ order.title || '加载中…' }}</text>
				<text class="ed__status-sub">{{ order.type }} · 赏金 <text class="ed__status-num">¥{{ rewardText }}</text></text>
			</view>
			<view class="ed__status-badge"><text class="ed__status-badge-t">{{ order.status }}</text></view>
		</view>

		<!-- 进度 -->
		<view class="ed__progress">
			<view class="ed__step" v-for="(s, i) in steps" :key="i">
				<view class="ed__step-dot" :class="{ 'ed__step-dot--on': i <= activeStep }">
					<text class="ed__step-dot-t">{{ i <= activeStep ? '✓' : i + 1 }}</text>
				</view>
				<text class="ed__step-label" :class="{ 'ed__step-label--on': i <= activeStep }">{{ s }}</text>
				<view v-if="i < steps.length - 1" class="ed__step-line" :class="{ 'ed__step-line--on': i < activeStep }"></view>
			</view>
		</view>

		<!-- 需求详情 -->
		<view class="ed__card">
			<text class="ed__card-title">需求详情</text>
			<view class="ed__line"><text class="ed__line-k">需求描述</text><text class="ed__line-v">{{ order.desc || '无' }}</text></view>
			<view class="ed__line"><text class="ed__line-k">取件地点</text><text class="ed__line-v">{{ order.pickup || '待沟通' }}</text></view>
			<view class="ed__line"><text class="ed__line-k">送达地点</text><text class="ed__line-v">{{ order.delivery || '待沟通' }}</text></view>
			<view class="ed__line"><text class="ed__line-k">期望时间</text><text class="ed__line-v">{{ order.deadline || '时间灵活' }}</text></view>
			<view class="ed__line"><text class="ed__line-k">订单编号</text><text class="ed__line-v ed__line-v--num">{{ order.id }}</text></view>
			<view class="ed__line" v-if="order.acceptorName"><text class="ed__line-k">接单同学</text><text class="ed__line-v">{{ order.acceptorName }}</text></view>
		</view>

		<!-- 发布者 -->
		<view class="ed__card ed__user" @click="onContact">
			<view class="ed__user-avatar"><text class="ed__user-ch">{{ (order.publisherName || '同')[0] }}</text></view>
			<view class="ed__user-info">
				<text class="ed__user-name">{{ order.publisherName }}</text>
				<view class="ed__user-sub">
					<image class="ed__user-shield" src="/static/unida/bubbles/shield-check.webp" mode="aspectFit" />
					<text class="ed__user-sub-t">已认证 · 点击联系</text>
				</view>
			</view>
			<image class="ed__chev" src="/static/icons-dark/chevron.png" mode="aspectFit" />
		</view>

		<view class="ed__tip" v-if="order.status === '进行中'">
			<text class="ed__tip-t">接单后请及时联系发布者确认细节，完成后由发布者确认交付</text>
		</view>

		<!-- 底部操作 -->
		<view class="ed__bottom">
			<view class="ed__btn ed__btn--ghost" @click="onContact">
				<image class="ed__btn-img" src="/static/unida/bubbles/chat-purple.webp" mode="aspectFit" />
				<text class="ed__btn-ghost-t">联系TA</text>
			</view>
			<!-- 待接单：非发布者 → 接单；发布者 → 取消 -->
			<view v-if="order.status === '待接单' && !isPublisher" class="ed__btn ed__btn--primary" @click="onAccept"><text class="ed__btn-t">立即接单</text></view>
			<view v-else-if="order.status === '待接单' && isPublisher" class="ed__btn ed__btn--cancel" @click="onCancel"><text class="ed__btn-t">取消订单</text></view>
			<!-- 进行中：发布者 → 确认完成；接单者 → 等待确认 -->
			<view v-else-if="order.status === '进行中' && isPublisher" class="ed__btn ed__btn--primary" @click="onConfirm"><text class="ed__btn-t">确认完成</text></view>
			<view v-else-if="order.status === '进行中'" class="ed__btn ed__btn--wait"><text class="ed__btn-t">已接单 · 待发布者确认</text></view>
			<!-- 已完成 -->
			<view v-else-if="order.status === '已完成'" class="ed__btn ed__btn--wait"><text class="ed__btn-t">订单已完成</text></view>
			<view v-else class="ed__btn ed__btn--wait"><text class="ed__btn-t">订单已取消</text></view>
		</view>
		<view class="ed__bottom-space"></view>
	</view>
</template>

<script>
	import { callCloud, getToken } from '@/common/cloud.js';

	export default {
		data() {
			return {
				statusBar: 0,
				orderId: '',
				order: {},
				steps: ['发布需求', '接单', '执行中', '已交付', '评价'],
				busy: false
			};
		},
		computed: {
			rewardText() {
				const r = Number(this.order.reward) || 0;
				return r % 1 === 0 ? String(r) : r.toFixed(2);
			},
			activeStep() {
				const s = this.order.status;
				if (s === '进行中') return 2;
				if (s === '已完成') return 3;
				return 0;
			},
			isPublisher() {
				return this.order.myRole === 'publisher';
			}
		},
		onLoad(q) {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
			this.orderId = (q && q.id) || '';
			this.loadDetail();
		},
		methods: {
			goBack() { uni.navigateBack(); },
			async loadDetail() {
				if (!this.orderId) return;
				try {
					const r = await callCloud('errand', { action: 'detail', token: getToken(), id: this.orderId });
					this.order = r.order || {};
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '加载订单失败', icon: 'none' });
				}
			},
			onContact() {
				const o = this.order;
				const peer = o.peerOpenid || 'official';
				const name = o.peerName || '同学';
				uni.navigateTo({ url: '/pages/chat/chat?peer=' + peer + '&name=' + encodeURIComponent(name) });
			},
			async onAccept() {
				if (this.busy) return;
				this.busy = true;
				try {
					await callCloud('errand', { action: 'accept', token: getToken(), id: this.orderId });
					uni.showToast({ title: '接单成功', icon: 'success' });
					this.loadDetail();
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '接单失败', icon: 'none' });
				} finally {
					this.busy = false;
				}
			},
			async onConfirm() {
				if (this.busy) return;
				this.busy = true;
				try {
					await callCloud('errand', { action: 'confirm', token: getToken(), id: this.orderId });
					uni.showToast({ title: '已确认完成', icon: 'success' });
					this.loadDetail();
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '操作失败', icon: 'none' });
				} finally {
					this.busy = false;
				}
			},
			onCancel() {
				uni.showModal({
					title: '取消订单',
					content: '确定取消这个跑腿需求吗？',
					confirmColor: '#FF5A4E',
					success: async (res) => {
						if (!res.confirm) return;
						try {
							await callCloud('errand', { action: 'cancel', token: getToken(), id: this.orderId });
							uni.showToast({ title: '已取消', icon: 'none' });
							this.loadDetail();
						} catch (e) {
							uni.showToast({ title: (e && e.message) || '操作失败', icon: 'none' });
						}
					}
				});
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.ed { padding: 0 $page-x 80rpx; box-sizing: border-box; }

	/* ---------- 导航 ---------- */
	.ed__nav { height: 110rpx; display: flex; align-items: center; justify-content: space-between; }
	.ed__back {
		width: 68rpx; height: 68rpx;
		background: $c-white;
		border-radius: 50%;
		box-shadow: $sh-card;
		display: flex; align-items: center; justify-content: center;
	}
	.ed__back-img { width: 32rpx; height: 32rpx; }
	.ed__title { font-size: 34rpx; font-weight: 800; color: $c-ink; letter-spacing: 1rpx; }
	.ed__ph { width: 68rpx; }

	/* ---------- 状态卡 ---------- */
	.ed__status {
		background: $g-brand;
		border-radius: $r-md;
		padding: 28rpx 30rpx;
		display: flex; align-items: center;
		box-shadow: $sh-float;
	}
	.ed__status-img { width: 100rpx; height: 100rpx; flex-shrink: 0; }
	.ed__status-info { flex: 1; margin-left: 22rpx; display: flex; flex-direction: column; min-width: 0; }
	.ed__status-title { font-size: 30rpx; font-weight: 800; color: $c-white; }
	.ed__status-sub { margin-top: 10rpx; font-size: 23rpx; color: rgba(255, 255, 255, 0.85); }
	.ed__status-num { font-family: $ff-num; font-weight: 800; font-size: 26rpx; color: $c-white; }
	.ed__status-badge {
		background: rgba(255, 255, 255, 0.25);
		border-radius: $r-pill;
		padding: 12rpx 24rpx;
		flex-shrink: 0;
	}
	.ed__status-badge-t { font-size: 23rpx; color: $c-white; font-weight: 600; }

	/* ---------- 进度 ---------- */
	.ed__progress {
		margin-top: 20rpx;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 30rpx 24rpx 26rpx;
		display: flex; align-items: flex-start;
	}
	.ed__step { flex: 1; display: flex; flex-direction: column; align-items: center; position: relative; }
	.ed__step-dot {
		width: 52rpx; height: 52rpx;
		border-radius: 50%;
		background: $c-mist;
		display: flex; align-items: center; justify-content: center;
	}
	.ed__step-dot--on { background: $g-cta; box-shadow: 0 8rpx 18rpx rgba(137, 100, 252, 0.35); }
	.ed__step-dot-t { font-size: 22rpx; color: $t-tertiary; font-family: $ff-num; font-weight: 700; }
	.ed__step-dot--on .ed__step-dot-t { color: $c-white; }
	.ed__step-label { margin-top: 12rpx; font-size: 20rpx; color: $t-tertiary; white-space: nowrap; }
	.ed__step-label--on { color: $c-primary; font-weight: 600; }
	.ed__step-line {
		position: absolute;
		top: 26rpx; left: calc(50% + 30rpx);
		width: calc(100% - 60rpx);
		height: 4rpx;
		background: $c-line;
		border-radius: $r-pill;
	}
	.ed__step-line--on { background: $c-primary; }

	/* ---------- 卡片 ---------- */
	.ed__card {
		margin-top: 20rpx;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 26rpx 28rpx;
	}
	.ed__card-title { display: block; font-size: 28rpx; font-weight: 700; color: $t-main; }
	.ed__line { display: flex; margin-top: 20rpx; }
	.ed__line-k { width: 140rpx; flex-shrink: 0; font-size: 24rpx; color: $t-tertiary; }
	.ed__line-v { flex: 1; font-size: 24rpx; color: $t-main; line-height: 1.6; }
	.ed__line-v--num { font-family: $ff-num; font-weight: 600; }

	/* ---------- 发布者 ---------- */
	.ed__user { display: flex; align-items: center; }
	.ed__user-avatar {
		width: 84rpx; height: 84rpx;
		border-radius: 50%;
		background: $g-brand;
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.ed__user-ch { font-size: 34rpx; font-weight: 800; color: $c-white; }
	.ed__user-info { flex: 1; margin-left: 20rpx; }
	.ed__user-name { font-size: 28rpx; font-weight: 700; color: $t-main; }
	.ed__user-sub { display: flex; align-items: center; margin-top: 8rpx; }
	.ed__user-shield { width: 30rpx; height: 30rpx; }
	.ed__user-sub-t { margin-left: 8rpx; font-size: 22rpx; color: $t-sub; }
	.ed__chev { width: 26rpx; height: 26rpx; opacity: 0.35; }

	/* ---------- 温馨提示 ---------- */
	.ed__tip {
		margin-top: 20rpx;
		background: rgba(255, 201, 79, 0.16);
		border-radius: $r-md;
		padding: 20rpx 26rpx;
	}
	.ed__tip-t { font-size: 22rpx; color: #B8860B; line-height: 1.6; }

	/* ---------- 底部操作 ---------- */
	.ed__bottom {
		position: fixed;
		left: 0; right: 0; bottom: 0;
		display: flex;
		padding: 20rpx $page-x calc(20rpx + env(safe-area-inset-bottom));
		background: $c-white;
		box-shadow: 0 -8rpx 24rpx rgba(123, 97, 255, 0.08);
	}
	.ed__btn {
		flex: 1;
		height: 92rpx;
		border-radius: $r-pill;
		display: flex; align-items: center; justify-content: center;
	}
	.ed__btn--ghost {
		background: $c-mist;
		margin-right: 20rpx;
	}
	.ed__btn-img { width: 40rpx; height: 40rpx; }
	.ed__btn-ghost-t { margin-left: 12rpx; font-size: 27rpx; color: $c-primary; font-weight: 600; }
	.ed__btn--primary { background: $g-cta; box-shadow: $sh-float; }
	.ed__btn--cancel { background: #FFF0EE; box-shadow: none; }
	.ed__btn--cancel .ed__btn-t { color: #E86154; }
	.ed__btn--wait { background: $c-ice; box-shadow: none; }
	.ed__btn--wait .ed__btn-t { color: $t-sub; font-size: 24rpx; }
	.ed__btn-t { font-size: 28rpx; color: $c-white; font-weight: 700; letter-spacing: 1rpx; }

	.ed__bottom-space { height: 180rpx; }
</style>
