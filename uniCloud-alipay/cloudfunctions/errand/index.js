/**
 * 云函数 errand —— 跑腿订单闭环
 * ------------------------------------------------------------------
 * action:
 *   hall    {cat?, sort?}           → { list } 待接单大厅（空集合自动写入种子单）
 *   detail  {id}                    → { order }
 *   publish {token, ...}            → { order } 发布跑腿需求
 *   accept  {token, id}             → { order } 接单（status 条件更新防抢单并发）
 *   confirm {token, id}             → { order } 发布者确认完成
 *   cancel  {token, id}             → { ok }    发布者取消（仅待接单）
 *   mine    {token, role?}          → { list }  我的订单（published / accepted / all）
 *
 * 状态机：待接单 → 进行中 → 已完成；待接单可被发布者取消 → 已取消
 * 所有状态变更都会给相关人写入 notifications（type=order）
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

const CATS = ['快递代取', '外卖代拿', '物品代送', '其他互助'];

function mapOrder(x) {
  return {
    id: x.id,
    type: x.type || '其他互助',
    title: x.title || '',
    desc: x.desc || '',
    reward: Number(x.reward) || 0,
    pickup: x.pickup || '',
    delivery: x.delivery || '',
    deadline: x.deadline || '',
    status: x.status || '待接单',
    publisherOpenid: x.publisherOpenid || '',
    publisherName: x.publisherName || '同学',
    acceptorOpenid: x.acceptorOpenid || '',
    acceptorName: x.acceptorName || '',
    acceptAt: x.acceptAt || 0,
    doneAt: x.doneAt || 0,
    createdAt: x.createdAt || 0,
    updatedAt: x.updatedAt || 0
  };
}

const SEEDS = [
  {
    id: 'rt-seed-1',
    type: '快递代取',
    title: '帮忙取个快递（中通北区驿站）',
    desc: '帮我去北区快递驿站取一个快递，取件码已提供，包裹不大很轻，辛苦啦！',
    reward: 8,
    pickup: '北区快递驿站（近食堂）',
    delivery: '东园 6 栋 307',
    deadline: '今天 18:00 前',
    status: '待接单',
    publisherOpenid: 'seed',
    publisherName: '阿星'
  },
  {
    id: 'rt-seed-2',
    type: '外卖代拿',
    title: '带一杯瑞幸（索铁不加糖）',
    desc: '东门瑞幸带一杯拿铁到宿舍楼下，到了发消息就行～',
    reward: 12,
    pickup: '东门瑞幸咖啡',
    delivery: '东园 3 栋楼下',
    deadline: '1 小时内',
    status: '待接单',
    publisherOpenid: 'seed',
    publisherName: '丸子'
  },
  {
    id: 'rt-seed-3',
    type: '其他互助',
    title: '代打印资料（20 页）',
    desc: '三教 1 楼打印店代打印 20 页资料，双面，打好送到宿舍楼下即可。',
    reward: 6,
    pickup: '三教 1 楼打印店',
    delivery: '东园 2 栋',
    deadline: '明天 8:00 前',
    status: '待接单',
    publisherOpenid: 'seed',
    publisherName: '小林同学'
  }
];

async function ensureSeeds(orders) {
  const q = await orders.limit(1).get();
  if (q.data && q.data.length) return;
  const now = Date.now();
  for (const s of SEEDS) {
    try { await orders.add({ ...s, createdAt: now - Math.floor(Math.random() * 3600 * 1000), updatedAt: now }); } catch (e) {}
  }
}

async function addNotify(db, n) {
  try {
    await db.collection('notifications').add({
      openid: n.to,
      type: 'order',
      title: n.title,
      text: n.text,
      link: n.link || '/pages/my-errands/my-errands',
      read: false,
      createdAt: Date.now()
    });
  } catch (e) {
    console.warn('通知写入失败:', e.message);
  }
}

exports.main = async (event = {}) => {
  const action = event.action || 'hall';
  const openid = verifyToken(event.token);
  const needLogin = ['publish', 'accept', 'confirm', 'cancel', 'mine'];
  if (needLogin.indexOf(action) >= 0 && !openid) {
    return { errCode: 401, errMsg: '登录态已失效，请重新登录' };
  }

  const id = String(event.id || '').trim();

  try {
    const db = uniCloud.database();
    const orders = db.collection('orders');

    if (action === 'hall') {
      await ensureSeeds(orders);
      const where = { status: '待接单' };
      if (event.cat && CATS.indexOf(event.cat) >= 0) where.type = event.cat;
      const sortField = event.sort === 'reward' ? 'reward' : 'createdAt';
      const q = await orders.where(where).orderBy(sortField, 'desc').limit(30).get();
      return { errCode: 0, errMsg: 'ok', list: (q.data || []).map(mapOrder) };
    }

    if (action === 'detail') {
      if (!id) return { errCode: 1, errMsg: '缺少订单 id' };
      const q = await orders.where({ id }).limit(1).get();
      const o = q.data && q.data[0];
      if (!o) return { errCode: 1, errMsg: '订单不存在' };
      const out = mapOrder(o);
      // 当前用户角色与对端联系方式（seed 种子单 → 对端为官方助手，方便单机测试聊天）
      if (openid) {
        out.myRole = o.publisherOpenid === openid ? 'publisher' : (o.acceptorOpenid === openid ? 'acceptor' : 'guest');
      } else {
        out.myRole = 'guest';
      }
      if (o.publisherOpenid === 'seed' && out.myRole !== 'publisher') {
        out.peerOpenid = 'official';
        out.peerName = 'UNIDA 小助手';
      } else if (out.myRole === 'publisher') {
        out.peerOpenid = o.acceptorOpenid || '';
        out.peerName = o.acceptorName || '接单同学';
      } else {
        out.peerOpenid = o.publisherOpenid || '';
        out.peerName = o.publisherName || '同学';
      }
      return { errCode: 0, errMsg: 'ok', order: out };
    }

    if (action === 'publish') {
      const title = String(event.title || '').trim().slice(0, 40);
      if (!title) return { errCode: 1, errMsg: '请填写需求标题' };
      const type = CATS.indexOf(event.type) >= 0 ? event.type : '其他互助';
      const reward = Math.max(1, Math.min(200, Number(event.reward) || 1));
      const uq = await db.collection('users').where({ openid }).limit(1).get();
      const user = uq.data && uq.data[0];
      const now = Date.now();
      const doc = {
        id: 'rt' + now + Math.floor(Math.random() * 90 + 10),
        type,
        title,
        desc: String(event.desc || '').trim().slice(0, 300),
        reward,
        pickup: String(event.pickup || '').trim().slice(0, 40),
        delivery: String(event.delivery || '').trim().slice(0, 40),
        deadline: String(event.deadline || '').trim().slice(0, 30),
        status: '待接单',
        publisherOpenid: openid,
        publisherName: (user && user.nickname) || '同学',
        createdAt: now,
        updatedAt: now
      };
      await orders.add(doc);
      return { errCode: 0, errMsg: 'ok', order: mapOrder(doc) };
    }

    if (action === 'accept') {
      if (!id) return { errCode: 1, errMsg: '缺少订单 id' };
      const uq = await db.collection('users').where({ openid }).limit(1).get();
      const user = uq.data && uq.data[0];
      const myName = (user && user.nickname) || '同学';
      const now = Date.now();
      // 条件更新：仅 status=待接单 可改，天然防止两人并发抢单
      const r = await orders.where({ id, status: '待接单' }).update({
        status: '进行中',
        acceptorOpenid: openid,
        acceptorName: myName,
        acceptAt: now,
        updatedAt: now
      });
      if (!r.updated) return { errCode: 1, errMsg: '手慢了，该订单刚被别人接走' };
      const q = await orders.where({ id }).limit(1).get();
      const o = q.data && q.data[0];
      if (o) {
        if (o.publisherOpenid !== 'seed') {
          await addNotify(db, { to: o.publisherOpenid, title: '订单已被接单', text: '「' + o.title + '」已被 ' + myName + ' 接单，可联系对方沟通细节', link: '/pages/my-errands/my-errands' });
        }
        await addNotify(db, { to: openid, title: '接单成功', text: '你已接下「' + o.title + '」，记得按时完成哦', link: '/pages/my-errands/my-errands' });
      }
      return { errCode: 0, errMsg: 'ok', order: o ? mapOrder(o) : null };
    }

    if (action === 'confirm') {
      if (!id) return { errCode: 1, errMsg: '缺少订单 id' };
      const q = await orders.where({ id }).limit(1).get();
      const o = q.data && q.data[0];
      if (!o) return { errCode: 1, errMsg: '订单不存在' };
      if (o.publisherOpenid !== openid) return { errCode: 1, errMsg: '只有发布者能确认完成' };
      if (o.status !== '进行中') return { errCode: 1, errMsg: '订单当前状态不可确认完成' };
      const now = Date.now();
      await orders.where({ id, status: '进行中' }).update({ status: '已完成', doneAt: now, updatedAt: now });

      // 互助完成奖励：双方各 +20 积分并写流水
      const grantReward = async (targetOpenid) => {
        if (!targetOpenid || targetOpenid === 'seed') return;
        try {
          const uq2 = await db.collection('users').where({ openid: targetOpenid }).limit(1).get();
          const u2 = uq2.data && uq2.data[0];
          if (!u2) return;
          const next = (Number(u2.points) || 0) + 20;
          await db.collection('users').doc(u2._id).update({ points: next });
          await db.collection('point_ledgers').add({
            openid: targetOpenid, type: 'reward', title: '互助完成奖励「' + o.title + '」', delta: 20,
            balance: next, refId: id, createdAt: now
          });
        } catch (e) { console.warn('互助奖励写入失败:', e.message); }
      };
      await grantReward(o.acceptorOpenid);
      await grantReward(o.publisherOpenid);

      if (o.acceptorOpenid && o.acceptorOpenid !== 'seed') {
        await addNotify(db, { to: o.acceptorOpenid, title: '订单已完成', text: '「' + o.title + '」发布者已确认完成，辛苦啦！', link: '/pages/my-errands/my-errands' });
      }
      await addNotify(db, { to: openid, title: '订单已完成', text: '「' + o.title + '」已确认完成', link: '/pages/my-errands/my-errands' });
      return { errCode: 0, errMsg: 'ok', order: mapOrder({ ...o, status: '已完成', doneAt: now }) };
    }

    if (action === 'cancel') {
      if (!id) return { errCode: 1, errMsg: '缺少订单 id' };
      const q = await orders.where({ id }).limit(1).get();
      const o = q.data && q.data[0];
      if (!o) return { errCode: 1, errMsg: '订单不存在' };
      if (o.publisherOpenid !== openid) return { errCode: 1, errMsg: '只有发布者能取消' };
      if (o.status !== '待接单') return { errCode: 1, errMsg: '已接单的订单不能取消，可联系对方协商' };
      await orders.where({ id, status: '待接单' }).update({ status: '已取消', updatedAt: Date.now() });
      return { errCode: 0, errMsg: 'ok' };
    }

    if (action === 'mine') {
      const dbCmd = db.command;
      const role = event.role === 'accepted' ? 'accepted' : event.role === 'published' ? 'published' : 'all';
      let where;
      if (role === 'published') where = { publisherOpenid: openid };
      else if (role === 'accepted') where = { acceptorOpenid: openid };
      else where = dbCmd.or([{ publisherOpenid: openid }, { acceptorOpenid: openid }]);
      const q = await orders.where(where).orderBy('updatedAt', 'desc').limit(50).get();
      return { errCode: 0, errMsg: 'ok', list: (q.data || []).map(mapOrder) };
    }

    return { errCode: 1, errMsg: '未知 action' };
  } catch (e) {
    console.error('errand error:', e);
    const msg = String((e && e.message) || e);
    if (msg.indexOf('request has expired') >= 0) {
      return { errCode: 2, errMsg: '本地调试数据库鉴权过期：请切到「连接云端云函数」' };
    }
    return { errCode: 2, errMsg: '跑腿操作失败：' + msg };
  }
};
