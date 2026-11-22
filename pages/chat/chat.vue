<template>
	<view class="ch">
		<view class="ch__safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 导航 -->
		<view class="ch__nav">
			<view class="ch__back" @click="goBack"><image class="ch__back-img" src="/static/unida/msg/ico-bubble.webp" mode="aspectFit" /></view>
			<view class="ch__peer">
				<view class="ch__peer-avatar"><text class="ch__peer-ch">{{ peerName[0] }}</text></view>
				<view class="ch__peer-info">
					<text class="ch__peer-name">{{ peerName }}</text>
					<view class="ch__peer-status">
						<image class="ch__peer-shield" src="/static/unida/bubbles/shield-check.webp" mode="aspectFit" />
						<text class="ch__peer-status-t">{{ isOfficial ? '官方助手 · 随时在线' : '已认证搭友' }}</text>
					</view>
				</view>
			</view>
			<view class="ch__more" @click="onMore"><image class="ch__more-img" src="/static/unida/msg/ico-bell.webp" mode="aspectFit" /></view>
		</view>

		<!-- 消息区 -->
		<scroll-view class="ch__msgs" scroll-y="true" :scroll-top="scrollTop">
			<view class="ch__msgs-pad"></view>
			<view class="ch__empty" v-if="!loading && msgs.length === 0">
				<text class="ch__empty-t">打个招呼吧～</text>
			</view>
			<view class="ch__msg" :class="m.mine ? 'ch__msg--out' : 'ch__msg--in'" v-for="(m, i) in msgs" :key="m.id || i">
				<view class="ch__msg-avatar" v-if="!m.mine"><text class="ch__msg-ch">{{ peerName[0] }}</text></view>
				<view v-if="m.type === 'emoji'" class="ch__bubble ch__bubble--emoji"><image class="ch__emoji-img" :src="m.src" mode="aspectFit" /></view>
				<view v-else class="ch__bubble">{{ m.text }}</view>
				<view class="ch__msg-avatar ch__msg-avatar--me" v-if="m.mine"><text class="ch__msg-ch">我</text></view>
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
	import { callCloud, getToken } from '@/common/cloud.js';

	export default {
		data() {
			return {
				statusBar: 0,
				peer: '',
				peerName: '同学',
				text: '',
				scrollTop: 0,
				loading: false,
				sendBusy: false,
				pollTimer: null,
				emojis: [
					'/static/unida/msg/ico-heart.webp',
					'/static/unida/bubbles/emoji-like.webp',
					'/static/unida/bubbles/emoji-clap.webp',
					'/static/unida/bubbles/emoji-party.webp',
					'/static/unida/bubbles/emoji-fire.webp',
					'/static/unida/bubbles/emoji-star.webp'
				],
				msgs: []
			};
		},
		computed: {
			isOfficial() { return this.peer === 'official'; }
		},
		onLoad(q) {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
			if (q && q.peer) this.peer = q.peer;
			if (q && q.name) this.peerName = decodeURIComponent(q.name);
			if (!this.peer) this.peer = 'official';
			this.loadMsgs();
			// 5 秒轮询新消息（小程序无长连接，轮询足够轻量）
			this.pollTimer = setInterval(() => this.loadMsgs(true), 5000);
		},
		onUnload() {
			if (this.pollTimer) clearInterval(this.pollTimer);
			this.pollTimer = null;
		},
		methods: {
			goBack() { uni.navigateBack(); },
			onMore() { uni.showToast({ title: '会话设置待开发', icon: 'none' }); },
			onTool() { uni.showToast({ title: '更多工具待接入', icon: 'none' }); },
			onInput(e) { this.text = e.detail.value; },
			async loadMsgs(silent) {
				if (this.loading && !silent) return;
				this.loading = true;
				try {
					const r = await callCloud('chat', { action: 'list', token: getToken(), peer: this.peer });
					this.msgs = r.list || [];
					this.scrollTop = this.scrollTop + 1;
				} catch (e) {
					if (!silent) uni.showToast({ title: (e && e.message) || '加载消息失败', icon: 'none' });
				} finally {
					this.loading = false;
				}
			},
			async onEmoji(i) {
				if (this.sendBusy) return;
				this.sendBusy = true;
				try {
					const r = await callCloud('chat', {
						action: 'send',
						token: getToken(),
						peer: this.peer,
						peerName: this.peerName,
						type: 'emoji',
						content: this.emojis[i]
					});
					if (r.msg) this.msgs = this.msgs.concat([r.msg]);
					this.scrollTop = this.scrollTop + 1;
					// 官方助手自动回复稍后到达，立即拉一次
					if (this.isOfficial) setTimeout(() => this.loadMsgs(true), 600);
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '发送失败', icon: 'none' });
				} finally {
					this.sendBusy = false;
				}
			},
			async send() {
				const t = this.text.trim();
				if (!t || this.sendBusy) return;
				this.sendBusy = true;
				try {
					const r = await callCloud('chat', {
						action: 'send',
						token: getToken(),
						peer: this.peer,
						peerName: this.peerName,
						type: 'text',
						content: t
					});
					if (r.msg) this.msgs = this.msgs.concat([r.msg]);
					this.text = '';
					this.scrollTop = this.scrollTop + 1;
					if (this.isOfficial) setTimeout(() => this.loadMsgs(true), 600);
				} catch (e) {
					uni.showToast({ title: (e && e.message) || '发送失败', icon: 'none' });
				} finally {
					this.sendBusy = false;
				}
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
	.ch__empty { display: flex; justify-content: center; padding: 80rpx 0; }
	.ch__empty-t { font-size: 25rpx; color: $t-tertiary; }

	.ch__msg { display: flex; align-items: flex-start; margin-top: 24rpx; }
	.ch__msg--out { flex-direction: row-reverse; }
	.ch__msg-avatar {
		width: 64rpx; height: 64rpx;
		border-radius: 50%;
		background: $g-brand;
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.ch__msg-avatar--me { background: $g-cta; margin-left: 0; }
	.ch__msg--in .ch__msg-avatar { margin-right: 16rpx; }
	.ch__msg--out .ch__msg-avatar { margin-left: 16rpx; }
	.ch__msg-ch { font-size: 26rpx; color: $c-white; font-weight: 700; }

	.ch__bubble {
		max-width: 460rpx;
		background: $c-white;
		border-radius: 8rpx 28rpx 28rpx 28rpx;
		padding: 22rpx 28rpx;
		font-size: 27rpx;
		color: $t-main;
		line-height: 1.6;
		box-shadow: $sh-card;
		box-sizing: border-box;
	}
	.ch__msg--out .ch__bubble {
		background: $g-brand;
		color: $c-white;
		border-radius: 28rpx 8rpx 28rpx 28rpx;
		box-shadow: 0 8rpx 16rpx rgba(128, 92, 250, 0.28);
	}
	.ch__bubble--emoji {
		background: $c-white;
		padding: 12rpx;
	}
	.ch__emoji-img { width: 88rpx; height: 88rpx; display: block; }

	/* ---------- 表情快捷栏 ---------- */
	.ch__emojis {
		display: flex; align-items: center; justify-content: space-around;
		background: $c-white;
		padding: 18rpx 24rpx;
		box-shadow: 0 -4rpx 16rpx rgba(57, 0, 126, 0.05);
	}
	.ch__emoji { width: 64rpx; height: 64rpx; }
	.ch__emoji:active { opacity: 0.7; }

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
	.ch__tool-img { width: 36rpx; height: 36rpx; }
	.ch__input {
		flex: 1; height: 76rpx;
		background: $c-mist;
		border-radius: $r-pill;
		padding: 0 30rpx;
		margin: 0 16rpx;
		font-size: 27rpx;
		color: $t-main;
		box-sizing: border-box;
	}
	.ch__send {
		background: $g-cta;
		border-radius: $r-pill;
		padding: 18rpx 34rpx;
		flex-shrink: 0;
		font-size: 26rpx;
		color: $c-white;
		font-weight: 700;
		box-shadow: 0 8rpx 16rpx rgba(255, 122, 82, 0.3);
	}
</style>
