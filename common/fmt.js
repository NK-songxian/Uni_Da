/**
 * 通用格式化工具
 */

/** 相对时间：刚刚 / N分钟前 / N小时前 / 昨天 / M月D日 */
export function timeAgo(ts) {
  if (!ts) return '';
  const d = new Date(ts);
  const now = Date.now();
  const diff = now - ts;
  if (diff < 60 * 1000) return '刚刚';
  if (diff < 60 * 60 * 1000) return Math.floor(diff / 60000) + '分钟前';
  if (diff < 24 * 60 * 60 * 1000) return Math.floor(diff / 3600000) + '小时前';
  const yest = new Date(now - 24 * 60 * 60 * 1000);
  if (d.toDateString() === yest.toDateString()) return '昨天';
  return (d.getMonth() + 1) + '月' + d.getDate() + '日';
}

/** 聊天时间：今天显示 HH:MM，昨天/更早显示日期 */
export function chatTime(ts) {
  if (!ts) return '';
  const d = new Date(ts);
  const now = new Date();
  const hm = ('0' + d.getHours()).slice(-2) + ':' + ('0' + d.getMinutes()).slice(-2);
  if (d.toDateString() === now.toDateString()) return hm;
  const yest = new Date(now.getTime() - 86400 * 1000);
  if (d.toDateString() === yest.toDateString()) return '昨天 ' + hm;
  return (d.getMonth() + 1) + '月' + d.getDate() + '日 ' + hm;
}
