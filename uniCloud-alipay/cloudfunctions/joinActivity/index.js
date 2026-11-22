/**
 * 云函数 joinActivity —— 报名 / 加入活动
 * ------------------------------------------------------------------
 * 1. 校验登录 token
 * 2. 把报名写入 activity_members（openid + itemId 唯一）
 * 3. 若 discover_items / activities 里有对应条目，同步增加 joined 人数
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

  const db = uniCloud.database();
  const dbCmd = db.command;

  // ── 取消预约 ──────────────────────────────
  if ((event.action || 'join') === 'cancel') {
    const itemId = String(event.itemId || '').trim();
    if (!itemId) return { errCode: 1, errMsg: '缺少活动 id' };
    try {
      const members = db.collection('activity_members');
      const q = await members.where({ openid, itemId, status: '已报名' }).limit(1).get();
      const m = q.data && q.data[0];
      if (!m) return { errCode: 1, errMsg: '没有找到有效的报名记录' };
      await members.doc(m._id).update({ status: '已取消', updatedAt: Date.now() });
      // 同步减报名人数（能找到就减，找不到不影响取消本身）
      for (const col of ['discover_items', 'activities']) {
        try {
          const iq = await db.collection(col).where({ id: itemId }).limit(1).get();
          const item = iq.data && iq.data[0];
          if (!item) continue;
          const nextJoined = Math.max(0, (Number(item.joined) || 0) - (Number(m.count) || 1));
          await db.collection(col).doc(item._id).update({ joined: nextJoined });
        } catch (e) {
          console.warn('同步 ' + col + ' 人数失败:', e.message);
        }
      }
      return { errCode: 0, errMsg: 'ok' };
    } catch (e) {
      console.error('cancelBooking error:', e);
      return { errCode: 2, errMsg: '取消预约失败：' + (e.message || e) };
    }
  }

  // ── 报名 / 加入 ──────────────────────────────
  const itemId = String(event.itemId || '').trim();
  const title = String(event.title || '').trim() || '未命名活动';
  const time = String(event.time || '').trim();
  const place = String(event.place || '').trim();
  const price = String(event.price || '免费').trim();
  const cover = String(event.cover || '/static/art/art-guitar.jpg');
  const count = Math.max(1, Math.min(6, Number(event.count) || 1));
  const remark = String(event.remark || '').trim().slice(0, 100);

  if (!itemId) return { errCode: 1, errMsg: '缺少活动 id' };

  try {
    const members = db.collection('activity_members');

    const existed = await members.where({ openid, itemId }).limit(1).get();
    const code = 'UNI' + Date.now();

    if (existed.data && existed.data.length) {
      const old = existed.data[0];
      if (old.status === '已取消') {
        await members.doc(old._id).update({ status: '已报名', count, remark, updatedAt: Date.now(), code });
      } else {
        await members.doc(old._id).update({ count, remark, updatedAt: Date.now() });
        return { errCode: 0, errMsg: 'ok', alreadyJoined: true, orderId: old.code, itemId };
      }
    } else {
      await members.add({
        openid,
        itemId,
        title,
        cover,
        time,
        place,
        price,
        count,
        remark,
        code,
        status: '已报名',
        createdAt: Date.now(),
        updatedAt: Date.now()
      });
    }

    // 同步活动人数（能找到就加，找不到也不影响报名记录本身）
    for (const col of ['discover_items', 'activities']) {
      try {
        const q = await db.collection(col).where({ id: itemId }).limit(1).get();
        const item = q.data && q.data[0];
        if (!item) continue;
        const nextJoined = Math.min(Number(item.total) || 999, (Number(item.joined) || 0) + count);
        await db.collection(col).doc(item._id).update({ joined: nextJoined });
      } catch (e) {
        console.warn('同步 ' + col + ' 人数失败:', e.message);
      }
    }

    // 预约通知：报名成功写给本人
    try {
      await db.collection('notifications').add({
        openid,
        type: 'booking',
        title: '报名成功',
        text: '【' + title + '】你已成功报名，可在我的报名中查看详情',
        link: '/pages/my-orders/my-orders',
        read: false,
        createdAt: Date.now()
      });
    } catch (e) {
      console.warn('通知写入失败:', e.message);
    }

    // 报名奖励：+10 积分并写流水
    try {
      const uq = await db.collection('users').where({ openid }).limit(1).get();
      const user = uq.data && uq.data[0];
      if (user) {
        const next = (Number(user.points) || 0) + 10;
        await db.collection('users').doc(user._id).update({ points: next });
        await db.collection('point_ledgers').add({
          openid, type: 'booking', title: '报名「' + title + '」', delta: 10,
          balance: next, refId: itemId, createdAt: Date.now()
        });
      }
    } catch (e) {
      console.warn('积分奖励写入失败:', e.message);
    }

    return { errCode: 0, errMsg: 'ok', alreadyJoined: false, orderId: code, itemId };
  } catch (e) {
    console.error('joinActivity error:', e);
    const msg = String(e && e.message || e);
    if (msg.indexOf('request has expired') >= 0) {
      return { errCode: 2, errMsg: '本地调试数据库鉴权过期：请切到「连接云端云函数」' };
    }
    return { errCode: 2, errMsg: '报名失败：' + msg };
  }
};
