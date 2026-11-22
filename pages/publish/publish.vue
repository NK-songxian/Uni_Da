<template>
	<view class="pb unida-page">
		<view class="pb__safe" :style="{ paddingTop: statusBar + 'px' }"></view>

		<!-- 顶栏 -->
		<view class="pb__top">
			<text class="pb__title">发布中心</text>
			<image class="pb__brand" src="/static/unida/bubbles/brand-badge-u.webp" mode="aspectFit" />
		</view>

		<!-- 云朵框 hero -->
		<view class="pb__hero">
			<image class="pb__hero-frame" src="/static/unida/bubbles/frame-unida-cloud.webp" mode="widthFix" />
			<view class="pb__hero-txt">
				<text class="pb__hero-t">选一种方式，开启你的校园故事</text>
				<text class="pb__hero-s">清晰的标题 · 真实的封面 · 明确的时间地点</text>
			</view>
			<view class="pb__spark pb__spark--a"></view>
			<view class="pb__spark pb__spark--b"></view>
		</view>

		<!-- 发布入口 2×3 -->
		<view class="pb__grid">
			<view class="pb__card" v-for="(item, i) in types" :key="i" @click="onType(i)">
				<view class="pb__cardhead">
					<view class="pb__ico" :class="'pb__ico--' + item.tone">
						<image class="pb__ico-img" :src="item.icon" mode="aspectFit" />
					</view>
					<image class="pb__chev" src="/static/icons-dark/chevron.png" mode="aspectFit" />
				</view>
				<text class="pb__name">{{ item.label }}</text>
				<text class="pb__desc">{{ item.desc }}</text>
			</view>
		</view>

		<!-- 热门标签 -->
		<view class="pb__sect">
			<view class="pb__spark pb__spark--c"></view>
			<text class="pb__sect-t">大家都在发</text>
			<text class="pb__sect-s">点标签，搭子更快找到你</text>
		</view>
		<scroll-view class="pb__lscroll" scroll-x="true">
			<view class="pb__lrow">
				<image class="pb__lab" v-for="(lab, i) in labels" :key="i" :src="lab.icon" mode="heightFix" @click="onLabel(i)" />
			</view>
		</scroll-view>

		<!-- 小贴士 -->
		<view class="pb__tip">
			<view class="pb__tip-ico"><image class="pb__tip-img" src="/static/icons-dark/bulb.png" mode="aspectFit" /></view>
			<view class="pb__tip-body">
				<text class="pb__tip-t">发布小贴士</text>
				<text class="pb__tip-s">写清楚做什么、什么时候、在哪儿，再选几个同频标签，搭子会主动来找你。</text>
			</view>
		</view>

		<view class="pb__bottom-space"></view>
		<unida-tabbar :current="2" />
	</view>
</template>

<script>
	import unidaTabbar from '@/components/unida-tabbar/unida-tabbar.vue';

	export default {
		components: { unidaTabbar },
		data() {
			return {
				statusBar: 0,
				types: [
					{ label: '学习搭子', desc: '自习·图书馆·技能教学', icon: '/static/icons-dark/buddy.png', tone: 'purple', route: 'form' },
					{ label: '运动搭子', desc: '健身·球类·跑步爬山', icon: '/static/icons-dark/flame.png', tone: 'orange', route: 'form' },
					{ label: '娱乐聚会', desc: '探店·桌游·唱歌摄影', icon: '/static/icons-dark/heart.png', tone: 'pink', route: 'form' },
					{ label: '发起活动', desc: '赛事·招新·讲座展览', icon: '/static/icons-dark/calendar.png', tone: 'sun', route: 'form' },
					{ label: '跑腿需求', desc: '快递·外卖·代取帮办', icon: '/static/icons-dark/box.png', tone: 'green', route: 'errand' },
					{ label: '校园动态', desc: '分享此刻的校园生活', icon: '/static/icons-dark/bulb.png', tone: 'sky', route: 'community' }
				],
				labels: [
					{ icon: '/static/unida/bubbles/label-hot.webp', name: '热门' },
					{ icon: '/static/unida/bubbles/label-new.webp', name: '新活动' },
					{ icon: '/static/unida/bubbles/label-study.webp', name: '学习' },
					{ icon: '/static/unida/bubbles/label-sport.webp', name: '运动' },
					{ icon: '/static/unida/bubbles/label-fun.webp', name: '娱乐' },
					{ icon: '/static/unida/bubbles/label-help.webp', name: '互助' },
					{ icon: '/static/unida/bubbles/label-campus.webp', name: '校园' },
					{ icon: '/static/unida/bubbles/label-rec.webp', name: '推荐' },
					{ icon: '/static/unida/bubbles/label-sync.webp', name: '同频' },
					{ icon: '/static/unida/bubbles/label-limit.webp', name: '限时' }
				]
			};
		},
		onLoad() {
			const sys = uni.getSystemInfoSync();
			this.statusBar = sys && sys.statusBarHeight || 0;
		},
		methods: {
			onType(i) {
				const t = this.types[i];
				if (!t) return;
				if (t.route === 'errand') { uni.navigateTo({ url: '/pages/errand-publish/errand-publish' }); return; }
				if (t.route === 'community') { uni.navigateTo({ url: '/pages/community/community' }); return; }
				uni.navigateTo({ url: '/pages/publish-form/publish-form?type=' + encodeURIComponent(t.label) });
			},
			onLabel(i) {
				uni.showToast({ title: '标签「' + this.labels[i].name + '」已带上（示例）', icon: 'none' });
			}
		}
	};
</script>

<style lang="scss" scoped>
	@import '@/common/unida-tokens.scss';

	.pb { min-height: 100vh; background: $c-mist; }

	/* ---------- 顶栏 ---------- */
	.pb__top { display: flex; align-items: center; padding: 24rpx $page-x 0; }
	.pb__title { font-size: 44rpx; font-weight: 800; color: $c-ink; flex: 1; }
	.pb__brand { width: 76rpx; height: 76rpx; }

	/* ---------- 云朵 hero ---------- */
	.pb__hero { position: relative; margin: 20rpx $page-x 0; }
	.pb__hero-frame { display: block; width: 686rpx; }
	.pb__hero-txt {
		position: absolute; left: 0; right: 0; top: 50%;
		transform: translateY(-52%);
		display: flex; flex-direction: column; align-items: center;
	}
	.pb__hero-t { font-size: 30rpx; font-weight: 800; color: $c-ink; }
	.pb__hero-s { margin-top: 12rpx; font-size: 20rpx; color: $t-sub; letter-spacing: 1rpx; }
	.pb__spark { position: absolute; border-radius: 3rpx; transform: rotate(45deg); }
	.pb__spark--a { right: 66rpx; top: -12rpx; width: 16rpx; height: 16rpx; background: $c-sun; }
	.pb__spark--b { right: 46rpx; top: 10rpx; width: 9rpx; height: 9rpx; background: $c-primary; opacity: 0.7; }
	.pb__spark--c { left: -20rpx; top: -8rpx; width: 13rpx; height: 13rpx; background: $c-sun; }

	/* ---------- 入口卡 ---------- */
	.pb__grid { display: flex; flex-wrap: wrap; justify-content: space-between; margin: 24rpx $page-x 0; }
	.pb__card {
		width: 335rpx;
		box-sizing: border-box;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 24rpx 26rpx 26rpx;
		margin-bottom: 16rpx;
		display: flex; flex-direction: column;
	}
	.pb__card:active { transform: scale(0.97); }
	.pb__cardhead { display: flex; align-items: flex-start; justify-content: space-between; }
	.pb__ico {
		width: 84rpx; height: 84rpx;
		border-radius: 26rpx;
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.pb__ico--purple { background: rgba(128, 92, 250, 0.13); }
	.pb__ico--orange { background: rgba(255, 155, 119, 0.16); }
	.pb__ico--pink { background: rgba(244, 114, 182, 0.14); }
	.pb__ico--green { background: rgba(41, 202, 131, 0.14); }
	.pb__ico--sky { background: rgba(105, 185, 245, 0.16); }
	.pb__ico--sun { background: rgba(255, 201, 79, 0.18); }
	.pb__ico-img { width: 44rpx; height: 44rpx; }
	.pb__name { display: block; margin-top: 20rpx; font-size: 30rpx; font-weight: 700; color: $t-main; }
	.pb__desc { display: block; margin-top: 8rpx; font-size: 21rpx; color: $t-sub; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
	.pb__chev { width: 26rpx; height: 26rpx; opacity: 0.35; }

	/* ---------- 热门标签 ---------- */
	.pb__sect { display: flex; align-items: baseline; margin: 28rpx $page-x 0; position: relative; }
	.pb__sect-t { font-size: 32rpx; font-weight: 800; color: $c-ink; }
	.pb__sect-s { margin-left: 14rpx; font-size: 20rpx; color: $t-tertiary; letter-spacing: 1rpx; }
	.pb__lscroll { width: 750rpx; margin-top: 18rpx; white-space: nowrap; }
	.pb__lrow { display: inline-flex; align-items: center; padding: 6rpx $page-x; }
	.pb__lab { height: 84rpx; margin-right: 18rpx; flex-shrink: 0; }
	.pb__lab:active { opacity: 0.8; }

	/* ---------- 小贴士 ---------- */
	.pb__tip {
		margin: 28rpx $page-x 0;
		background: $c-white;
		border-radius: $r-md;
		box-shadow: $sh-card;
		padding: 24rpx 26rpx;
		display: flex; align-items: flex-start;
	}
	.pb__tip-ico {
		width: 64rpx; height: 64rpx;
		border-radius: 20rpx;
		background: rgba(255, 201, 79, 0.2);
		display: flex; align-items: center; justify-content: center;
		flex-shrink: 0;
	}
	.pb__tip-img { width: 36rpx; height: 36rpx; }
	.pb__tip-body { margin-left: 20rpx; display: flex; flex-direction: column; }
	.pb__tip-t { font-size: 26rpx; font-weight: 700; color: $t-main; }
	.pb__tip-s { margin-top: 10rpx; font-size: 22rpx; color: $t-sub; line-height: 1.7; }

	.pb__bottom-space { height: 200rpx; }
</style>
