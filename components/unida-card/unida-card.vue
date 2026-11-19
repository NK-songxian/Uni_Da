<template>
	<!-- 活动/搭子卡片：封面 + 标题 + 标签 + 时间地点 + 人数费用 —— 线性图标，无 emoji -->
	<view class="acard" @click="onTap">
		<view class="acard__cover" :style="{ background: coverBg }">
			<image v-if="item.cover" class="acard__cover-img" :src="item.cover" mode="aspectFill" lazy-load></image>
			<image v-else class="acard__cover-icon" :src="coverIcon" mode="aspectFit"></image>
			<view v-if="item.hot" class="acard__hot">
				<image class="acard__hot-icon" src="/static/icons/flame.png" mode="aspectFit" />
				<text>热门</text>
			</view>
		</view>
		<view class="acard__body">
			<view class="acard__title-row">
				<text class="acard__title">{{ item.title }}</text>
			</view>
			<view class="acard__tags">
				<text class="unida-tag unida-tag--purple">{{ item.category }}</text>
				<text class="unida-tag" :class="item.genderTag === '女生优先' ? 'unida-tag--orange' : 'unida-tag--green'">{{ item.genderTag }}</text>
			</view>
			<view class="acard__meta">
				<view class="acard__meta-item">
					<image class="acard__meta-icon" src="/static/icons/clock.png" mode="aspectFit" />
					<text>{{ item.time }}</text>
				</view>
				<view class="acard__meta-item">
					<image class="acard__meta-icon" src="/static/icons/pin.png" mode="aspectFit" />
					<text>{{ item.place }}</text>
				</view>
			</view>
			<view class="acard__footer">
				<view class="acard__people">
					<view class="acard__avatars">
						<view
							v-for="(a, i) in avatarList"
							:key="i"
							class="acard__avatar"
							:style="{ background: a.bg }"
						>{{ a.text }}</view>
					</view>
					<text class="acard__count">{{ item.joined }}/{{ item.total }}人</text>
				</view>
				<text class="acard__price" :class="{ 'acard__price--free': item.price === '免费' }">{{ item.price }}</text>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		name: 'unida-card',
		props: {
			item: { type: Object, default: () => ({}) }
		},
		computed: {
			coverBg() {
				const map = {
					'运动': 'linear-gradient(135deg,#34D399,#86EFAC)',
					'娱乐': 'linear-gradient(135deg,#F472B6,#FBCFE8)',
					'学习': 'linear-gradient(135deg,#5B8DEF,#93C5FD)',
					'教学': 'linear-gradient(135deg,#A78BFA,#DDD6FE)',
					'跑腿': 'linear-gradient(135deg,#FF8A3D,#FFD76A)',
					'找搭子': 'linear-gradient(135deg,#7B61FF,#B59BFF)',
					'校园活动': 'linear-gradient(135deg,#FF8A3D,#FFD76A)'
				};
				return map[this.item.category] || 'linear-gradient(135deg,#B59BFF,#7B61FF)';
			},
			coverIcon() {
				const map = {
					'运动': 'racket', '娱乐': 'music', '学习': 'book', '教学': 'bulb',
					'跑腿': 'box', '找搭子': 'buddy', '校园活动': 'calendar'
				};
				return '/static/icons/' + (map[this.item.category] || 'grid') + '.png';
			},
			avatarList() {
				const n = Math.min(Math.max(this.item.joined || 0, 1), 3);
				const colors = ['#7B61FF', '#34D399', '#FF8A3D'];
				const chars = ['U', 'N', 'I'];
				return Array.from({ length: n }, (_, i) => ({ text: chars[i], bg: colors[i] }));
			}
		},
		methods: {
			onTap() {
				this.$emit('tap', this.item);
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-global.scss';
	/* 水晶玻璃卡：半透明 + 细白边 + 内高光，替代生硬的纯白卡片 */
	.acard {
		padding: 0;
		overflow: hidden;
		margin-bottom: 22rpx;
		border-radius: 32rpx;
		background: linear-gradient(150deg, rgba(255,255,255,0.92) 0%, rgba(247,242,255,0.82) 100%);
		border: 2rpx solid rgba(255,255,255,0.9);
		box-shadow:
			0 14rpx 36rpx rgba(123, 97, 255, 0.12),
			inset 0 2rpx 0 rgba(255,255,255,0.95);
	}
	.acard__cover {
		width: 100%;
		height: 240rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
		position: relative;
	}
	.acard__cover-img {
		width: 100%; height: 100%;
	}
	.acard__cover-icon {
		width: 120rpx; height: 120rpx;
		opacity: 0.92;
	}
	.acard__hot {
		position: absolute;
		top: 16rpx; right: 16rpx;
		display: flex; align-items: center;
		padding: 6rpx 16rpx;
		border-radius: 999rpx;
		background: rgba(255, 255, 255, 0.92);
		color: $unida-orange;
		font-size: 20rpx;
		font-weight: 700;
		box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
	}
	.acard__hot-icon { width: 24rpx; height: 24rpx; margin-right: 6rpx; }
	.acard__body { padding: 20rpx 24rpx 24rpx; }
	.acard__title-row { display: flex; align-items: center; justify-content: space-between; }
	.acard__title {
		font-size: 30rpx; font-weight: 700; color: $unida-text;
		flex: 1; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;
	}
	.acard__tags { display: flex; gap: 12rpx; margin-top: 16rpx; }
	.acard__meta { margin-top: 18rpx; display: flex; flex-direction: column; gap: 10rpx; }
	.acard__meta-item { display: flex; align-items: center; font-size: 24rpx; color: $unida-text-sub; }
	.acard__meta-icon { width: 26rpx; height: 26rpx; margin-right: 8rpx; opacity: 0.6; }
	.acard__footer {
		margin-top: 20rpx; display: flex; align-items: center; justify-content: space-between;
		padding-top: 18rpx; border-top: 2rpx solid $unida-divider;
	}
	.acard__people { display: flex; align-items: center; }
	.acard__avatars { display: flex; margin-right: 12rpx; }
	.acard__avatar {
		width: 36rpx; height: 36rpx; border-radius: 50%;
		border: 2rpx solid #fff;
		margin-right: -10rpx;
		display: flex; align-items: center; justify-content: center;
		color: #fff; font-size: 18rpx; font-weight: 700;
	}
	.acard__count { font-size: 24rpx; color: $unida-text-sub; margin-left: 14rpx; }
	.acard__price { font-size: 30rpx; font-weight: 700; color: $unida-orange; }
	.acard__price--free { color: $unida-green; }
</style>
