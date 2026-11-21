<script>
	import { CLOUD_MODE, getToken, getUser } from '@/common/cloud.js';

	export default {
		onLaunch: function() {
			// 云端模式下恢复登录态到全局，供各页面读取
			if (CLOUD_MODE.enabled) {
				const token = getToken();
				this.globalData = this.globalData || {};
				this.globalData.token = token;
				this.globalData.user = getUser();
			}
		},
		onShow: function() {},
		onHide: function() {}
	}
</script>

<style lang="scss">
	/* UNIDA（有你搭）全局设计系统 — 依据 docs/UI-Design.md */
	@import '@/common/unida-global.scss';
</style>
