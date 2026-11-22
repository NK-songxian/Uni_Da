/**
 * 云函数 points —— 积分 / 签到 / 积分流水 / 商城兑换 / 我的统计
 * ------------------------------------------------------------------
 * action:
 *   home    {token}              → { points, streak, signedToday, profileDone, hasOrders }
 *   checkin {token}              → { points, streak, gained }（+5 并写积分流水）
 *   stats   {token}              → { points, streak, signedToday, orderCount, favCount, pubCount, level, levelName }
 *   ledger  {token, page?}       → { list, hasMore } 积分明细（每页 20 条）
 *   redeem  {token, name, cost}  → { points } 商城兑换（校验余额、扣分、写流水）
 *
 * 积分铁律：余额只能由服务端修改；所有变动必须写 point_ledgers 流水。
 * 流水 type：signin 签到 / booking 报名 / publish 发帖 / review 评价 /
 *            reward 互助完成 / redeem 兑换
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

/** 按东八区取 YYYY-MM-DD，避免服务器时区影响签到日切 */
function dateStr(offsetDays) {
  const d = new Date(Date.now() + 8 * 3600 * 1000 + (offsetDays || 0) * 86400 * 1000);
  return d.getUTCFullYear() + '-' + ('0' + (d.getUTCMonth() + 1)).slice(-2) + '-' + ('0' + d.getUTCDate()).slice(-2);
}

function levelOf(points) {
  const p = Number(points) || 0;
  if (p >= 2000) return { level: 6, levelName: '校园明星' };
  if (p >= 1000) return { level: 5, levelName: '活力星人' };
  if (p >= 500) return { level: 4, levelName: '活跃成长者' };
  if (p >= 200) return { level: 3, levelName: '热心搭友' };
  return { level: 2, levelName: '初来乍到' };
}

async function getStreak(checkins, openid, signedToday) {
  const targetDate = signedToday ? dateStr(0) : dateStr(-1);
  const q = await checkins.where({ openid, date: targetDate }).limit(1).get();
  const rec = q.data && q.data[0];
  return rec ? (Number(rec.streak) || 1) : 0;
}

/** 写积分流水（余额由调用方计算并更新，这里只记账） */
async function addLedger(db, openid, type, title, delta, balance, refId) {
  try {
    await db.collection('point_ledgers').add({
      openid,
      type,
      title,
      delta,
      balance,
      refId: refId || '',
      createdAt: Date.now()
    });
  } catch (e) {
    console.warn('积分流水写入失败:', e.message);
  }
}

exports.main = async (event = {}) => {
  const openid = verifyToken(event.token);
  if (!openid) return { errCode: 401, errMsg: '登录态已失效，请重新登录' };

  const action = event.action || 'home';

  try {
    const db = uniCloud.database();
    const users = db.collection('users');
    const checkins = db.collection('checkins');

    const uq = await users.where({ openid }).limit(1).get();
    const user = uq.data && uq.data[0];
    if (!user) return { errCode: 1, errMsg: '用户不存在，请重新登录' };

    if (action === 'home') {
      const tq = await checkins.where({ openid, date: dateStr(0) }).limit(1).get();
      const signedToday = !!(tq.data && tq.data.length);
      const streak = await getStreak(checkins, openid, signedToday);
      const oq = await db.collection('activity_members').where({ openid }).count();
      return {
        errCode: 0,
        errMsg: 'ok',
        points: Number(user.points) || 0,
        streak,
        signedToday,
        profileDone: !!(user.nickname && user.school),
        hasOrders: (oq.total || 0) > 0
      };
    }

    if (action === 'checkin') {
      const today = dateStr(0);
      const tq = await checkins.where({ openid, date: today }).limit(1).get();
      if (tq.data && tq.data.length) {
        return { errCode: 1, errMsg: '今日已签到，明天再来吧～' };
      }
      const yq = await checkins.where({ openid, date: dateStr(-1) }).limit(1).get();
      const streak = (yq.data && yq.data.length) ? (Number(yq.data[0].streak) || 0) + 1 : 1;
      const gained = 5;
      await checkins.add({ openid, date: today, streak, points: gained, createdAt: Date.now() });
      const nextPoints = (Number(user.points) || 0) + gained;
      await users.doc(user._id).update({ points: nextPoints });
      await addLedger(db, openid, 'signin', '每日签到', gained, nextPoints, today);
      return { errCode: 0, errMsg: 'ok', points: nextPoints, streak, gained };
    }

    if (action === 'stats') {
      const tq = await checkins.where({ openid, date: dateStr(0) }).limit(1).get();
      const signedToday = !!(tq.data && tq.data.length);
      const streak = await getStreak(checkins, openid, signedToday);
      const oq = await db.collection('activity_members').where({ openid }).count();
      const fq = await db.collection('favorites').where({ openid }).count();
      const pq = await db.collection('posts').where({ authorOpenid: openid }).count();
      const lv = levelOf(user.points);
      return {
        errCode: 0,
        errMsg: 'ok',
        points: Number(user.points) || 0,
        streak,
        signedToday,
        orderCount: oq.total || 0,
        favCount: fq.total || 0,
        pubCount: pq.total || 0,
        level: lv.level,
        levelName: lv.levelName
      };
    }

    if (action === 'ledger') {
      const size = 20;
      const page = Math.max(1, Number(event.page) || 1);
      const q = await db.collection('point_ledgers')
        .where({ openid })
        .orderBy('createdAt', 'desc')
        .skip((page - 1) * size)
        .limit(size)
        .get();
      const list = (q.data || []).map((x) => ({
        id: x._id,
        type: x.type || 'other',
        title: x.title || '',
        delta: Number(x.delta) || 0,
        balance: Number(x.balance) || 0,
        ts: x.createdAt || 0
      }));
      return { errCode: 0, errMsg: 'ok', list, hasMore: list.length >= size };
    }

    if (action === 'redeem') {
      const name = String(event.name || '').trim().slice(0, 30);
      const cost = Number(event.cost) || 0;
      if (!name || cost <= 0) return { errCode: 1, errMsg: '兑换参数有误' };
      const cur = Number(user.points) || 0;
      if (cur < cost) return { errCode: 1, errMsg: '积分不够，去签到/做任务赚积分吧' };
      const next = cur - cost;
      await users.doc(user._id).update({ points: next });
      await addLedger(db, openid, 'redeem', '兑换「' + name + '」', -cost, next, '');
      return { errCode: 0, errMsg: 'ok', points: next };
    }

    return { errCode: 1, errMsg: '未知 action' };
  } catch (e) {
    console.error('points error:', e);
    const msg = String((e && e.message) || e);
    if (msg.indexOf('request has expired') >= 0) {
      return { errCode: 2, errMsg: '本地调试数据库鉴权过期：请切到「连接云端云函数」' };
    }
    return { errCode: 2, errMsg: '积分操作失败：' + msg };
  }
};
