<template>
	<view class="ch">
		<view class="ch__safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 导航 -->
		<view class="ch__nav">
			<view class="ch__back" @click="goBack"><image class="ch__back-img" src="/static/unida/msg/ico-bubble.webp" mode="aspectFit" /></view>
			<view class="ch__peer">
				<view class="ch__peer-avatar"><text class="ch__peer-ch">{{ peerName[0] }}</text><image class="ch__peer-online" src="/static/unida/bubbles/check-green.webp" mode="aspectFit" /></view>
				<view class="ch__peer-info">
					<text class="ch__peer-name">{{ peerName }}</text>
					<view class="ch__peer-status">
						<image class="ch__peer-shield" src="/static/unida/bubbles/shield-check.webp" mode="aspectFit" />
						<text class="ch__peer-status-t">在线 · 已认证</text>
					</view>
				</view>
			</view>
			<view class="ch__more" @click="onMore"><image class="ch__more-img" src="/static/unida/msg/ico-bell.webp" mode="aspectFit" /></view>
		</view>

		<!-- 消息区 -->
		<scroll-view class="ch__msgs" scroll-y="true" :scroll-top="scrollTop">
			<view class="ch__msgs-pad"></view>
			<view class="ch__time">今天 10:24</view>
			<view class="ch__msg ch__msg--in" v-for="(m, i) in msgs" :key="i">
				<view class="ch__msg-avatar"><text class="ch__msg-ch">{{ peerName[0] }}</text></view>
				<view v-if="m.type === 'emoji'" class="ch__bubble ch__bubble--emoji"><image class="ch__emoji-img" :src="m.src" mode="aspectFit" /></view>
				<view v-else class="ch__bubble">{{ m.text }}</view>
			</view>
			<!-- 订单卡片 -->
			<view class="ch__ordercard">
				<view class="ch__ordercard-head">
					<view class="ch__ordercard-tag"><image class="ch__ordercard-tag-img" src="/static/unida/msg/ico-bag.webp" mode="aspectFit" /><text class="ch__ordercard-tag-t">跑腿订单</text></view>
					<text class="ch__ordercard-status">待接单</text>
				</view>
				<text class="ch__ordercard-title">帮忙取快递（中通北区）</text>
				<view class="ch__ordercard-foot">
					<text class="ch__ordercard-reward">赏金 ¥8.00</text>
					<image class="ch__ordercard-stamp" src="/static/unida/msg/tag-order.webp" mode="aspectFit" />
				</view>
			</view>
			<view class="ch__msg ch__msg--out">
				<view class="ch__bubble">太好了！取件码我私你，送到东园3栋楼下就行～</view>
				<view class="ch__msg-avatar ch__msg-avatar--me"><text class="ch__msg-ch">我</text></view>
			</view>
			<view class="ch__msgs-pad"></view>
		</scroll-view>

		<!-- 表情快捷栏 -->
		<view class="ch__emojis">
			<image class="ch__emoji" v-for="(e, i) in emojis" :key="i" :src="e" mode="heightFix" @click="onEmoji(i)" />
		</view>

		<!-- 输入区 -->
		<view class="ch__inputbar">
			<view class="ch__tool" @click="onTool"><image class="ch__tool-img" src="/static/unida/msg/ico-bubble.webp" mode="aspectFit" /></view>
			<input class="ch__input" :value="text" @input="onInput" placeholder="发消息…" confirm-type="send" @confirm="send" />
			<view class="ch__send" @click="send">发送</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				statusBar: 0,
				peerName: '周同学',
				text: '',
				scrollTop: 0,
				emojis: [
					'/static/unida/msg/ico-heart.webp',
					'/static/unida/bubbles/emoji-like.webp',
					'/static/unida/bubbles/emoji-clap.webp',
					'/static/unida/bubbles/emoji-party.webp',
					'/static/unida/bubbles/emoji-fire.webp',
					'/static/unida/bubbles/emoji-star.webp'
				],
				msgs: [
					{ type: 'text', text: '你好！看到你发布的跑腿需求，我可以帮你取～' },
					{ type: 'text', text: '我在东区，离北区驿站挺近的' }
				]
			};
		},
		onLoad(q) {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
			if (q && q.name) this.peerName = q.name;
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onMore() { uni.showToast({ title: '会话设置待开发', icon: 'none' }); },
			onTool() { uni.showToast({ title: '更多工具待接入', icon: 'none' }); },
			onInput(e) { this.text = e.detail.value; },
			onEmoji(i) {
				this.msgs = this.msgs.concat([{ type: 'emoji', src: this.emojis[i] }]);
				this.scrollTop = this.scrollTop + 1;
			},
			send() {
				if (!this.text.trim()) return;
				this.msgs = this.msgs.concat([{ type: 'text', text: this.text }]);
				this.text = '';
				this.scrollTop = this.scrollTop + 1;
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.ch { height: 100vh; display: flex; flex-direction: column; background: $c-mist; }

	/* ---------- 导航 ---------- */
	.ch__nav { display: flex; align-items: center; background: $c-white; padding: 20rpx $page-x; box-shadow: $sh-card; }
	.ch__back {
		width: 68rpx; height: 68rpx;
		background: $c-mist;
		border-radius: 50%;
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.ch__back-img { width: 38rpx; height: 38rpx; }
	.ch__peer { flex: 1; display: flex; align-items: center; margin-left: 20rpx; min-width: 0; }
	.ch__peer-avatar {
		position: relative;
		width: 84rpx; height: 84rpx;
		border-radius: 50%;
		background: $g-brand;
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.ch__peer-ch { font-size: 34rpx; font-weight: 800; color: $c-white; }
	.ch__peer-online { position: absolute; right: -4rpx; bottom: -2rpx; width: 26rpx; height: 26rpx; }
	.ch__peer-info { margin-left: 18rpx; display: flex; flex-direction: column; }
	.ch__peer-name { font-size: 30rpx; font-weight: 700; color: $t-main; }
	.ch__peer-status { display: flex; align-items: center; margin-top: 6rpx; }
	.ch__peer-shield { width: 28rpx; height: 28rpx; }
	.ch__peer-status-t { margin-left: 8rpx; font-size: 20rpx; color: $c-mint; }
	.ch__more {
		width: 68rpx; height: 68rpx;
		background: $c-mist;
		border-radius: 50%;
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.ch__more-img { width: 40rpx; height: 40rpx; }

	/* ---------- 消息区 ---------- */
	.ch__msgs { flex: 1; padding: 0 24rpx; box-sizing: border-box; }
	.ch__msgs-pad { height: 24rpx; }
	.ch__time { text-align: center; font-size: 21rpx; color: $t-tertiary; margin: 12rpx 0 28rpx; font-family: $ff-num; }
	.ch__msg { display: flex; align-items: flex-start; margin-bottom: 28rpx; }
	.ch__msg-avatar {
		width: 72rpx; height: 72rpx;
		border-radius: 50%;
		background: $g-brand;
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.ch__msg-avatar--me { background: linear-gradient(160deg, #FF9B77, #FFC94F); }
	.ch__msg-ch { font-size: 30rpx; font-weight: 800; color: $c-white; }
	.ch__bubble {
		max-width: 70%;
		padding: 22rpx 26rpx;
		font-size: 26rpx;
		line-height: 1.6;
		color: $t-main;
	}
	.ch__msg--in .ch__bubble { background: $c-white; border-radius: 6rpx 24rpx 24rpx 24rpx; margin-left: 16rpx; }
	.ch__msg--out { justify-content: flex-end; }
	.ch__msg--out .ch__bubble { background: $g-cta; border-radius: 24rpx 6rpx 24rpx 24rpx; margin-right: 16rpx; color: $c-white; }
	.ch__bubble--emoji { padding: 10rpx; }
	.ch__emoji-img { width: 96rpx; height: 96rpx; }

	.ch__ordercard {
		background: $c-white;
		border-radius: $r-md;
		padding: 24rpx;
		margin: 0 88rpx 28rpx;
		box-shadow: $sh-card;
	}
	.ch__ordercard-head { display: flex; align-items: center; justify-content: space-between; }
	.ch__ordercard-tag { display: flex; align-items: center; }
	.ch__ordercard-tag-img { width: 40rpx; height: 40rpx; }
	.ch__ordercard-tag-t { margin-left: 8rpx; font-size: 23rpx; color: $t-sub; }
	.ch__ordercard-status { font-size: 22rpx; color: $c-peach; font-weight: 600; }
	.ch__ordercard-title { display: block; margin-top: 16rpx; font-size: 26rpx; font-weight: 600; color: $t-main; }
	.ch__ordercard-foot { display: flex; align-items: center; justify-content: space-between; margin-top: 10rpx; }
	.ch__ordercard-reward { font-size: 30rpx; font-weight: 800; color: $c-peach; font-family: $ff-num; }
	.ch__ordercard-stamp { height: 40rpx; width: 116rpx; }

	/* ---------- 表情快捷栏 ---------- */
	.ch__emojis {
		display: flex; align-items: center; justify-content: space-between;
		padding: 14rpx $page-x;
		background: $c-white;
	}
	.ch__emoji { height: 72rpx; width: 72rpx; flex-shrink: 0; }
	.ch__emoji:active { transform: scale(0.85); }

	/* ---------- 输入区 ---------- */
	.ch__inputbar {
		display: flex; align-items: center;
		padding: 16rpx $page-x calc(16rpx + env(safe-area-inset-bottom));
		background: $c-white;
	}
	.ch__tool {
		width: 68rpx; height: 68rpx;
		background: $c-mist;
		border-radius: 50%;
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.ch__tool-img { width: 38rpx; height: 38rpx; }
	.ch__input {
		flex: 1;
		height: 72rpx;
		background: $c-mist;
		border-radius: $r-pill;
		padding: 0 28rpx;
		font-size: 26rpx;
		margin: 0 16rpx;
	}
	.ch__send {
		font-size: 26rpx;
		color: $c-white;
		background: $g-cta;
		padding: 18rpx 34rpx;
		border-radius: $r-pill;
		font-weight: 600;
		flex-shrink: 0;
	}
</style>
