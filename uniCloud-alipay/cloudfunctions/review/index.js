/**
 * 云函数 review —— 活动评价
 * ------------------------------------------------------------------
 * action:
 *   submit {token, itemId, title, rating, tags, content} → { ok }
 *   check  {token, itemId} → { reviewed }
 *
 * 规则：同一活动每人只能评价一次；提交成功 +15 积分并写流水（type=review）。
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

async function addLedger(db, openid, type, title, delta, balance, refId) {
  try {
    await db.collection('point_ledgers').add({
      openid, type, title, delta, balance, refId: refId || '', createdAt: Date.now()
    });
  } catch (e) {
    console.warn('积分流水写入失败:', e.message);
  }
}

exports.main = async (event = {}) => {
  const openid = verifyToken(event.token);
  if (!openid) return { errCode: 401, errMsg: '登录态已失效，请重新登录' };

  const action = event.action || 'submit';
  const itemId = String(event.itemId || '').trim();

  try {
    const db = uniCloud.database();
    const reviews = db.collection('reviews');

    if (action === 'check') {
      if (!itemId) return { errCode: 1, errMsg: '缺少活动 id' };
      const q = await reviews.where({ openid, itemId }).limit(1).get();
      return { errCode: 0, errMsg: 'ok', reviewed: !!(q.data && q.data.length) };
    }

    if (action === 'submit') {
      if (!itemId) return { errCode: 1, errMsg: '缺少活动 id' };
      const rating = Math.max(1, Math.min(5, Number(event.rating) || 5));
      const content = String(event.content || '').trim().slice(0, 200);
      const tags = Array.isArray(event.tags) ? event.tags.map((t) => String(t).slice(0, 12)).slice(0, 6) : [];
      if (!content && !tags.length) return { errCode: 1, errMsg: '写点评价或选个标签再提交吧' };

      const dup = await reviews.where({ openid, itemId }).limit(1).get();
      if (dup.data && dup.data.length) {
        return { errCode: 1, errMsg: '这个活动你已经评价过啦' };
      }

      await reviews.add({
        openid,
        itemId,
        title: String(event.title || '').slice(0, 60),
        rating,
        tags,
        content,
        createdAt: Date.now()
      });

      // +15 积分奖励并写流水
      const uq = await db.collection('users').where({ openid }).limit(1).get();
      const user = uq.data && uq.data[0];
      if (user) {
        const next = (Number(user.points) || 0) + 15;
        await db.collection('users').doc(user._id).update({ points: next });
        await addLedger(db, openid, 'review', '评价「' + (event.title || '活动') + '」', 15, next, itemId);
      }
      return { errCode: 0, errMsg: 'ok', gained: 15 };
    }

    return { errCode: 1, errMsg: '未知 action' };
  } catch (e) {
    console.error('review error:', e);
    const msg = String((e && e.message) || e);
    if (msg.indexOf('request has expired') >= 0) {
      return { errCode: 2, errMsg: '本地调试数据库鉴权过期：请切到「连接云端云函数」' };
    }
    return { errCode: 2, errMsg: '评价提交失败：' + msg };
  }
};
