<template>
	<view class="ag unida-page">
		<view class="ag__nav">
			<navigator open-type="navigateBack" delta="1" class="ag__back">‹</navigator>
			<text class="ag__title">{{ title }}</text>
			<text class="ag__ph"></text>
		</view>
		<scroll-view scroll-y class="ag__scroll">
			<view class="ag__doc unida-card">
				<text class="ag__h">UNIDA（有你搭）{{ title }}</text>
				<text class="ag__date">更新日期：2026年11月18日</text>

				<text class="ag__p">欢迎使用 UNIDA（有你搭）。本{{ title }}适用于由校园用户使用的 UNIDA 微信小程序服务。请在使用前仔细阅读并理解本协议的全部内容。</text>

				<text class="ag__h2">一、服务说明</text>
				<text class="ag__p">UNIDA 是面向大学生的校园社交与生活互助平台，提供找搭子、校园活动、技能教学、跑腿互助、校园社区等功能。用户须为在校大学生或经校园认证的用户。</text>

				<text class="ag__h2">二、用户账号</text>
				<text class="ag__p">使用微信一键登录或手机号登录即表示你同意创建 UNIDA 账号。你应妥善保管账号信息，因账号泄露产生的责任由用户自行承担。</text>

				<text class="ag__h2">三、信息收集与使用</text>
				<text class="ag__p">我们遵循最小必要原则收集信息，包括：微信开放标识、手机号（经授权）、学校信息、用户主动填写的资料与发布内容。我们不会在未经授权的情况下向第三方提供你的个人信息。</text>

				<text class="ag__h2">四、用户内容规范</text>
				<text class="ag__p">用户发布的内容须合法、真实、健康，不得包含违法违规、虚假、低俗、侵权信息。平台有权对违规内容进行处理，并提供举报渠道。</text>

				<text class="ag__h2">五、免责声明</text>
				<text class="ag__p">平台仅提供信息发布与撮合服务，线下活动的安全与责任由参与者自行承担。请在参与活动时注意人身与财产安全。</text>

				<text class="ag__h2">六、协议更新</text>
				<text class="ag__p">本协议可能随业务发展更新，更新后将在小程序内公示。继续使用服务即视为接受更新后的协议。</text>

				<text class="ag__footer-note">如有疑问，请通过「我的 - 举报与反馈」联系我们。</text>
			</view>
		</scroll-view>
	</view>
</template>

<script>
	export default {
		data() {
			return { title: '用户协议' };
		},
		onLoad(options) {
			if (options.type) this.title = options.type;
			uni.setNavigationBarTitle({ title: this.title });
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.ag { height: 100vh; display: flex; flex-direction: column; }
	.ag__nav { height: 120rpx; padding: 60rpx 32rpx 0; display: flex; align-items: center; justify-content: space-between; background: #fff; }
	.ag__back { font-size: 48rpx; color: $unida-text; width: 60rpx; }
	.ag__title { font-size: 32rpx; font-weight: 700; }
	.ag__ph { width: 60rpx; }
	.ag__scroll { flex: 1; }
	.ag__doc { margin: 24rpx; padding: 36rpx 32rpx; }
	.ag__h { display: block; font-size: 36rpx; font-weight: 800; color: $unida-text; }
	.ag__date { display: block; margin-top: 12rpx; font-size: 22rpx; color: $unida-text-sub; }
	.ag__h2 { display: block; margin-top: 36rpx; font-size: 30rpx; font-weight: 700; color: $unida-primary; }
	.ag__p { display: block; margin-top: 16rpx; font-size: 26rpx; color: #4a4560; line-height: 1.8; text-align: justify; }
	.ag__footer-note { display: block; margin-top: 48rpx; padding-top: 24rpx; border-top: 2rpx solid $unida-divider; font-size: 24rpx; color: $unida-text-sub; }
</style>
