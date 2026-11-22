/**
 * 云函数 favorite —— 收藏系统
 * ------------------------------------------------------------------
 * action:
 *   check  {token, type, targetId}              → { faved }
 *   toggle {token, type, targetId, snapshot...} → { faved }
 *   list   {token, type?}                       → { list }
 * type: 'item'（活动）| 'post'（帖子）
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

async function incPostFavs(db, postId, d) {
  try {
    const q = await db.collection('posts').where({ id: postId }).limit(1).get();
    const p = q.data && q.data[0];
    if (!p) return;
    await db.collection('posts').doc(p._id).update({ favs: Math.max(0, (Number(p.favs) || 0) + d) });
  } catch (e) {}
}

exports.main = async (event = {}) => {
  const openid = verifyToken(event.token);
  if (!openid) return { errCode: 401, errMsg: '登录态已失效，请重新登录' };

  const action = event.action || 'list';
  const type = event.type === 'post' ? 'post' : 'item';
  const targetId = String(event.targetId || '').trim();

  try {
    const db = uniCloud.database();
    const favs = db.collection('favorites');

    if (action === 'check') {
      const q = await favs.where({ openid, type, targetId }).limit(1).get();
      return { errCode: 0, errMsg: 'ok', faved: !!(q.data && q.data.length) };
    }

    if (action === 'toggle') {
      if (!targetId) return { errCode: 1, errMsg: '缺少 targetId' };
      const q = await favs.where({ openid, type, targetId }).limit(1).get();
      if (q.data && q.data.length) {
        await favs.doc(q.data[0]._id).remove();
        if (type === 'post') await incPostFavs(db, targetId, -1);
        return { errCode: 0, errMsg: 'ok', faved: false };
      }
      await favs.add({
        openid,
        type,
        targetId,
        title: String(event.title || '').slice(0, 60),
        cover: String(event.cover || ''),
        desc: String(event.desc || '').slice(0, 80),
        createdAt: Date.now()
      });
      if (type === 'post') await incPostFavs(db, targetId, 1);
      return { errCode: 0, errMsg: 'ok', faved: true };
    }

    if (action === 'list') {
      const where = { openid };
      if (event.type) where.type = event.type === 'post' ? 'post' : 'item';
      const q = await favs.where(where).orderBy('createdAt', 'desc').limit(50).get();
      return {
        errCode: 0,
        errMsg: 'ok',
        list: (q.data || []).map((x) => ({
          id: x.targetId,
          type: x.type,
          title: x.title,
          cover: x.cover,
          desc: x.desc,
          createdAt: x.createdAt
        }))
      };
    }

    return { errCode: 1, errMsg: '未知 action' };
  } catch (e) {
    console.error('favorite error:', e);
    const msg = String((e && e.message) || e);
    if (msg.indexOf('request has expired') >= 0) {
      return { errCode: 2, errMsg: '本地调试数据库鉴权过期：请切到「连接云端云函数」' };
    }
    return { errCode: 2, errMsg: '收藏操作失败：' + msg };
  }
};
