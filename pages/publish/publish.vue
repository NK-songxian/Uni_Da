<template>
	<view class="publish unida-page">
		<!-- 头部 -->
		<view class="publish__hero">
			<view class="publish__hero-deco">✦</view>
			<text class="publish__title">发布中心</text>
			<text class="publish__sub">选一种方式，开启你的校园故事 ✨</text>
		</view>

		<!-- 六大发布入口 -->
		<view class="publish__grid">
			<view
				class="publish__item"
				v-for="(item, i) in types"
				:key="i"
				@click="onPublish(item)"
			>
				<view class="publish__icon" :style="{ background: item.bg }">
					<text class="publish__emoji">{{ item.icon }}</text>
				</view>
				<text class="publish__label">{{ item.label }}</text>
				<text class="publish__desc">{{ item.desc }}</text>
			</view>
		</view>

		<!-- 发布提示卡 -->
		<view class="publish__tip unida-card">
			<text class="publish__tip-title">💡 发布小贴士</text>
			<text class="publish__tip-text">清晰的标题、真实的活动封面、明确的时间和地点，能帮你更快找到同频搭子哦～</text>
		</view>

		<unida-tabbar :current="2" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';

	export default {
		components: { unidaTabbar },
		data() {
			return {
				types: [
					{ label: '找搭子', desc: '找人一起做事', icon: '🤝', bg: 'linear-gradient(135deg,#7B61FF,#B59BFF)', form: '找搭子' },
					{ label: '发起活动', desc: '组局多人活动', icon: '🎪', bg: 'linear-gradient(135deg,#FF8A3D,#FFD76A)', form: '活动' },
					{ label: '技能教学', desc: '分享你的特长', icon: '🎸', bg: 'linear-gradient(135deg,#F472B6,#FBCFE8)', form: '教学' },
					{ label: '跑腿需求', desc: '发布互助任务', icon: '🛵', bg: 'linear-gradient(135deg,#34D399,#86EFAC)', form: '跑腿' },
					{ label: '校园动态', desc: '分享校园生活', icon: '📝', bg: 'linear-gradient(135deg,#5B8DEF,#93C5FD)', form: '动态' },
					{ label: '活动招募', desc: '为活动招人', icon: '📣', bg: 'linear-gradient(135deg,#A78BFA,#DDD6FE)', form: '招募' }
				]
			};
		},
		methods: {
			onPublish(item) {
				uni.showToast({ title: '「' + item.label + '」表单待开发', icon: 'none' });
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	.publish__hero {
		position: relative;
		padding: 70rpx 40rpx 50rpx;
		background: linear-gradient(135deg, #7B61FF, #B59BFF);
		border-radius: 0 0 44rpx 44rpx;
		overflow: hidden;
	}
	.publish__hero-deco { position: absolute; right: 60rpx; top: 50rpx; color: rgba(255,255,255,0.5); font-size: 56rpx; }
	.publish__title { display: block; font-size: 48rpx; font-weight: 800; color: #fff; }
	.publish__sub { display: block; margin-top: 12rpx; font-size: 26rpx; color: rgba(255,255,255,0.9); }

	.publish__grid {
		display: flex;
		flex-wrap: wrap;
		padding: 32rpx 16rpx 0;
	}
	.publish__item {
		width: 33.33%;
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 20rpx 8rpx 30rpx;
	}
	.publish__icon {
		width: 110rpx;
		height: 110rpx;
		border-radius: 32rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 0 10rpx 24rpx rgba(123,97,255,0.16);
	}
	.publish__emoji { font-size: 54rpx; }
	.publish__label { margin-top: 18rpx; font-size: 28rpx; font-weight: 700; color: $unida-text; }
	.publish__desc { margin-top: 6rpx; font-size: 22rpx; color: $unida-text-sub; }
	.publish__item:active .publish__icon { transform: scale(0.92); }

	.publish__tip { margin: 16rpx 24rpx; display: flex; flex-direction: column; }
	.publish__tip-title { font-size: 28rpx; font-weight: 700; color: $unida-primary; }
	.publish__tip-text { margin-top: 12rpx; font-size: 24rpx; color: $unida-text-sub; line-height: 1.6; }
</style>
