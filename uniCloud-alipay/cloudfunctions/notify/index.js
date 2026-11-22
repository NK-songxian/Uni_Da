/**
 * 云函数 notify —— 业务通知中心
 * ------------------------------------------------------------------
 * action:
 *   list   {token, type?}  → { list, counts } 通知列表 + 各类型未读数（首次自动写欢迎通知）
 *   read   {token, id?}    → { ok } 标记已读（id 为空 = 全部已读）
 *   unread {token}         → { total } 未读总数（tabbar 角标用）
 *
 * type: system 系统通知 / activity 活动通知 / order 订单通知
 *       booking 预约通知 / interact 互动消息
 *
 * 写入方：joinActivity（报名成功）、posts（评论/点赞互动）、errand（订单流转）
 *        都直接写 notifications 集合，本函数只负责读取与已读。
 */
'use strict';

const crypto = require('crypto');

function verifyToken(token) {
  if (!token || typeof token !== 'string') return '';
  const parts = token.split('.');
  if (parts.length !== 3) return '';
  const [openid, ts, sig] = parts;
  if (!openid || !/^\d+$/.test(ts)) return '';
  const expect = crypto.createHash('md5')
    .update(openid + '|' + ts + '|unida')
    .digest('hex').slice(0, 16);
  if (sig !== expect) return '';
  return openid;
}

function timeTextOf(ts) {
  const d = new Date(ts);
  const now = new Date();
  const hm = ('0' + d.getHours()).slice(-2) + ':' + ('0' + d.getMinutes()).slice(-2);
  if (d.toDateString() === now.toDateString()) return hm;
  const yest = new Date(now.getTime() - 86400 * 1000);
  if (d.toDateString() === yest.toDateString()) return '昨天 ' + hm;
  return (d.getMonth() + 1) + '月' + d.getDate() + '日';
}

exports.main = async (event = {}) => {
  const openid = verifyToken(event.token);
  if (!openid) return { errCode: 401, errMsg: '登录态已失效，请重新登录' };

  const action = event.action || 'list';

  try {
    const db = uniCloud.database();
    const nf = db.collection('notifications');

    if (action === 'list') {
      // 首次使用：写一条系统欢迎通知
      const sq = await nf.where({ openid }).limit(1).get();
      if (!sq.data || !sq.data.length) {
        await nf.add({
          openid,
          type: 'system',
          title: '欢迎来到 UNIDA!',
          text: '在这里，找到同频的搭子、参与精彩的校园活动、解锁更丰富的大学生活！',
          link: '/pages/home/home',
          read: false,
          createdAt: Date.now()
        });
      }
      const where = { openid };
      if (event.type && event.type !== 'all') where.type = event.type;
      const q = await nf.where(where).orderBy('createdAt', 'desc').limit(50).get();
      // 各类型未读数
      const all = await nf.where({ openid, read: false }).limit(100).get();
      const counts = { system: 0, activity: 0, order: 0, booking: 0, interact: 0 };
      for (const x of (all.data || [])) {
        if (counts[x.type] !== undefined) counts[x.type] += 1;
      }
      return {
        errCode: 0,
        errMsg: 'ok',
        list: (q.data || []).map((x) => ({
          id: x._id,
          type: x.type || 'system',
          title: x.title || '',
          text: x.text || '',
          link: x.link || '',
          read: !!x.read,
          time: timeTextOf(x.createdAt || 0)
        })),
        counts,
        unread: (all.data || []).length
      };
    }

    if (action === 'read') {
      if (event.id) {
        await nf.where({ _id: event.id, openid }).update({ read: true });
      } else {
        await nf.where({ openid, read: false }).update({ read: true });
      }
      return { errCode: 0, errMsg: 'ok' };
    }

    if (action === 'unread') {
      const q = await nf.where({ openid, read: false }).count();
      return { errCode: 0, errMsg: 'ok', total: q.total || 0 };
    }

    return { errCode: 1, errMsg: '未知 action' };
  } catch (e) {
    console.error('notify error:', e);
    const msg = String((e && e.message) || e);
    if (msg.indexOf('request has expired') >= 0) {
      return { errCode: 2, errMsg: '本地调试数据库鉴权过期：请切到「连接云端云函数」' };
    }
    return { errCode: 2, errMsg: '通知操作失败：' + msg };
  }
};
