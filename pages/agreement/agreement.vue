<template>
	<view class="ag unida-page">
		<view class="ag-safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 顶栏 -->
		<view class="ag__nav">
			<view class="ag__back" @click="goBack"><image class="ag__back-img" src="/static/icons-dark/back.png" mode="aspectFit" /></view>
			<text class="ag__title">{{ title }}</text>
			<view class="ag__ph"></view>
		</view>

		<scroll-view scroll-y class="ag__scroll">
			<view class="ag__doc">
				<view class="ag__head">
					<image class="ag__head-badge" src="/static/unida/bubbles/brand-badge-u.webp" mode="heightFix" />
					<view class="ag__head-info">
						<text class="ag__h">UNIDA（有你搭）{{ title }}</text>
						<text class="ag__date">更新日期：2026年11月18日</text>
					</view>
				</view>

				<text class="ag__p">欢迎使用 UNIDA（有你搭）。本{{ title }}适用于由校园用户使用的 UNIDA 微信小程序服务。请在使用前仔细阅读并理解本协议的全部内容。</text>

				<view class="ag__clause" v-for="(c, i) in clauses" :key="i">
					<view class="ag__clause-head">
						<view class="ag__clause-no"><text class="ag__clause-no-t">{{ i + 1 }}</text></view>
						<text class="ag__h2">{{ c.title }}</text>
					</view>
					<text class="ag__p">{{ c.text }}</text>
				</view>

				<view class="ag__footer"><image class="ag__footer-ico" src="/static/unida/bubbles/shield-u.webp" mode="heightFix" /><text class="ag__footer-note">如有疑问，请通过「我的 - 举报与反馈」联系我们。</text></view>
			</view>
		</scroll-view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				title: '用户协议',
				clauses: [
					{ title: '服务说明', text: 'UNIDA 是面向大学生的校园社交与生活互助平台，提供找搭子、校园活动、技能教学、跑腿互助、校园社区等功能。用户须为在校大学生或经校园认证的用户。' },
					{ title: '用户账号', text: '使用微信一键登录或手机号登录即表示你同意创建 UNIDA 账号。你应妥善保管账号信息，因账号泄露产生的责任由用户自行承担。' },
					{ title: '信息收集与使用', text: '我们遵循最小必要原则收集信息，包括：微信开放标识、手机号（经授权）、学校信息、用户主动填写的资料与发布内容。我们不会在未经授权的情况下向第三方提供你的个人信息。' },
					{ title: '用户内容规范', text: '用户发布的内容须合法、真实、健康，不得包含违法违规、虚假、低俗、侵权信息。平台有权对违规内容进行处理，并提供举报渠道。' },
					{ title: '免责声明', text: '平台仅提供信息发布与撮合服务，线下活动的安全与责任由参与者自行承担。请在参与活动时注意人身与财产安全。' },
					{ title: '协议更新', text: '本协议可能随业务发展更新，更新后将在小程序内公示。继续使用服务即视为接受更新后的协议。' }
				]
			};
		},
		onLoad(options) {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
			if (options.type) this.title = options.type;
			uni.setNavigationBarTitle({ title: this.title });
		},
		methods: {
			goBack() { uni.navigateBack(); }
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.ag { height: 100vh; display: flex; flex-direction: column; box-sizing: border-box; padding: 0 $page-x; }
	.ag__nav { height: 110rpx; display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; }
	.ag__back {
		width: 68rpx; height: 68rpx;
		background: $c-white;
		border-radius: 50%;
		box-shadow: $sh-card;
		display: flex; align-items: center; justify-content: center;
	}
	.ag__back-img { width: 32rpx; height: 32rpx; }
	.ag__title { font-size: 34rpx; font-weight: 800; color: $c-ink; letter-spacing: 1rpx; }
	.ag__ph { width: 68rpx; }
	.ag__scroll { flex: 1; min-height: 0; }

	.ag__doc {
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 32rpx;
	}
	.ag__head { display: flex; align-items: center; }
	.ag__head-badge { height: 76rpx; width: 84rpx; flex-shrink: 0; }
	.ag__head-info { flex: 1; margin-left: 16rpx; display: flex; flex-direction: column; min-width: 0; }
	.ag__h { font-size: 32rpx; font-weight: 800; color: $c-ink; }
	.ag__date { margin-top: 8rpx; font-size: 21rpx; color: $t-tertiary; font-family: $ff-num; }

	.ag__p { display: block; margin-top: 16rpx; font-size: 26rpx; color: #4A4560; line-height: 1.8; text-align: justify; }
	.ag__clause { margin-top: 32rpx; }
	.ag__clause-head { display: flex; align-items: center; }
	.ag__clause-no {
		width: 44rpx; height: 44rpx;
		border-radius: 14rpx;
		background: rgba(128, 92, 250, 0.12);
		display: flex; align-items: center; justify-content: center;
		margin-right: 14rpx;
		flex-shrink: 0;
	}
	.ag__clause-no-t { font-size: 24rpx; color: $c-primary; font-weight: 700; font-family: $ff-num; }
	.ag__h2 { font-size: 28rpx; font-weight: 800; color: $c-primary; }

	.ag__footer {
		display: flex; align-items: center;
		margin-top: 48rpx; padding-top: 28rpx;
		border-top: 2rpx solid $c-line;
	}
	.ag__footer-ico { height: 40rpx; width: 48rpx; margin-right: 12rpx; flex-shrink: 0; }
	.ag__footer-note { flex: 1; font-size: 23rpx; color: $t-sub; line-height: 1.6; }
</style>
