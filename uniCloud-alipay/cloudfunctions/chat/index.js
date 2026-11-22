/**
 * 云函数 chat —— 私信 / 会话系统
 * ------------------------------------------------------------------
 * action:
 *   conversations {token}             → { list }（首次使用自动写入官方欢迎消息）
 *   list          {token, peer}       → { list } 与某人的历史消息（自动置为已读）
 *   send          {token, peer, ...}  → { msg }（发给官方账号会自动回复）
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

function pairKey(a, b) {
  return [String(a), String(b)].sort().join('_');
}

const OFFICIAL = { openid: 'official', name: 'UNIDA 小助手' };
const AUTO_REPLIES = [
  '收到啦～我是 UNIDA 小助手，有任何问题都可以问我。',
  '好的，已记录！参加活动记得准时到场哦～',
  '感谢你的反馈！UNIDA 会越做越好玩的。',
  '可以试试去发现页看看最新的搭子活动～'
];

function previewOf(m) {
  return m.type === 'emoji' ? '[表情]' : String(m.content || '');
}

function timeTextOf(ts) {
  const d = new Date(ts);
  const now = new Date();
  const hm = ('0' + d.getHours()).slice(-2) + ':' + ('0' + d.getMinutes()).slice(-2);
  const sameDay = d.toDateString() === now.toDateString();
  if (sameDay) return hm;
  const yest = new Date(now.getTime() - 86400 * 1000);
  if (d.toDateString() === yest.toDateString()) return '昨天 ' + hm;
  return (d.getMonth() + 1) + '月' + d.getDate() + '日 ' + hm;
}

exports.main = async (event = {}) => {
  const openid = verifyToken(event.token);
  if (!openid) return { errCode: 401, errMsg: '登录态已失效，请重新登录' };

  const action = event.action || 'conversations';

  try {
    const db = uniCloud.database();
    const msgs = db.collection('messages');

    if (action === 'conversations') {
      // 首次使用：写入官方欢迎消息，保证会话列表不为空
      const pk = pairKey(openid, OFFICIAL.openid);
      const sq = await msgs.where({ pairKey: pk, from: OFFICIAL.openid }).limit(1).get();
      if (!sq.data || !sq.data.length) {
        await msgs.add({
          pairKey: pk,
          from: OFFICIAL.openid,
          to: openid,
          fromName: OFFICIAL.name,
          toName: '同学',
          type: 'text',
          content: '欢迎来到 UNIDA！在这里可以和搭子们私信聊天，有任何问题随时找我～',
          read: false,
          createdAt: Date.now()
        });
      }
      const q = await msgs.where(db.command.or([{ from: openid }, { to: openid }]))
        .orderBy('createdAt', 'desc').limit(200).get();
      const rows = q.data || [];
      const map = {};
      for (const m of rows) {
        const peer = m.from === openid ? m.to : m.from;
        if (!map[peer]) {
          map[peer] = {
            peer,
            name: m.from === openid ? (m.toName || '同学') : (m.fromName || '同学'),
            preview: previewOf(m),
            ts: m.createdAt || 0,
            unread: 0
          };
        }
        if (m.to === openid && !m.read) map[peer].unread += 1;
      }
      const list = Object.keys(map).map((k) => {
        const c = map[k];
        return {
          peer: c.peer,
          name: c.name,
          preview: c.preview,
          time: timeTextOf(c.ts),
          ts: c.ts,
          unread: c.unread
        };
      }).sort((a, b) => b.ts - a.ts);
      return { errCode: 0, errMsg: 'ok', list };
    }

    if (action === 'list') {
      const peer = String(event.peer || '').trim();
      if (!peer) return { errCode: 1, errMsg: '缺少 peer' };
      const pk = pairKey(openid, peer);
      const q = await msgs.where({ pairKey: pk }).orderBy('createdAt', 'asc').limit(100).get();
      // 置为已读
      try {
        await msgs.where({ pairKey: pk, to: openid, read: false }).update({ read: true });
      } catch (e) {}
      const list = (q.data || []).map((m) => ({
        id: m._id,
        mine: m.from === openid,
        type: m.type || 'text',
        text: m.type === 'emoji' ? '' : String(m.content || ''),
        src: m.type === 'emoji' ? String(m.content || '') : '',
        time: timeTextOf(m.createdAt || 0)
      }));
      return { errCode: 0, errMsg: 'ok', list, peer };
    }

    if (action === 'send') {
      const peer = String(event.peer || '').trim();
      const content = String(event.content || '').trim().slice(0, 300);
      const type = event.type === 'emoji' ? 'emoji' : 'text';
      const peerName = String(event.peerName || '').slice(0, 30) || '同学';
      if (!peer || !content) return { errCode: 1, errMsg: '消息内容不能为空' };

      const uq = await db.collection('users').where({ openid }).limit(1).get();
      const user = uq.data && uq.data[0];
      const myName = (user && user.nickname) || '同学';

      const doc = {
        pairKey: pairKey(openid, peer),
        from: openid,
        to: peer,
        fromName: myName,
        toName: peerName,
        type,
        content,
        read: false,
        createdAt: Date.now()
      };
      const added = await msgs.add(doc);
      const now = Date.now();

      // 发给官方账号：自动回复一条，保证单机也能测试聊天闭环
      if (peer === OFFICIAL.openid) {
        const reply = AUTO_REPLIES[Math.floor(Math.random() * AUTO_REPLIES.length)];
        await msgs.add({
          pairKey: pairKey(openid, OFFICIAL.openid),
          from: OFFICIAL.openid,
          to: openid,
          fromName: OFFICIAL.name,
          toName: myName,
          type: 'text',
          content: reply,
          read: false,
          createdAt: now + 1
        });
      }

      return {
        errCode: 0,
        errMsg: 'ok',
        msg: { id: added.id, mine: true, type, text: type === 'emoji' ? '' : content, src: type === 'emoji' ? content : '', time: timeTextOf(now) }
      };
    }

    return { errCode: 1, errMsg: '未知 action' };
  } catch (e) {
    console.error('chat error:', e);
    const msg = String((e && e.message) || e);
    if (msg.indexOf('request has expired') >= 0) {
      return { errCode: 2, errMsg: '本地调试数据库鉴权过期：请切到「连接云端云函数」' };
    }
    return { errCode: 2, errMsg: '消息操作失败：' + msg };
  }
};
