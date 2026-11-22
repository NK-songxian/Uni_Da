/**
 * 云函数 getMyOrders —— 我的报名列表
 * ------------------------------------------------------------------
 * 返回当前用户在 activity_members 里的全部报名记录。
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

exports.main = async (event) => {
  const openid = verifyToken(event.token);
  if (!openid) return { errCode: 401, errMsg: '登录态已失效，请重新登录' };

  try {
    const db = uniCloud.database();
    const res = await db.collection('activity_members')
      .where({ openid })
      .orderBy('createdAt', 'desc')
      .limit(100)
      .get();

    const list = (res.data || []).map((x) => ({
      id: x.code,
      itemId: x.itemId,
      title: x.title,
      cover: x.cover,
      time: x.time,
      place: x.place,
      price: x.price,
      count: x.count,
      remark: x.remark,
      status: x.status,
      createdAt: x.createdAt
    }));

    return { errCode: 0, errMsg: 'ok', list, total: list.length };
  } catch (e) {
    console.error('getMyOrders error:', e);
    const msg = String(e && e.message || e);
    if (msg.indexOf('request has expired') >= 0) {
      return { errCode: 2, errMsg: '本地调试数据库鉴权过期：请切到「连接云端云函数」' };
    }
    return { errCode: 2, errMsg: '获取我的报名失败：' + msg };
  }
};
