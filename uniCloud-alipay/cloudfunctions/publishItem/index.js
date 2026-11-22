/**
 * 云函数 publishItem —— 发布活动 / 找搭子 / 跑腿
 * ------------------------------------------------------------------
 * 前端提交表单 → 校验登录 token → 写入 discover_items 集合。
 * 写入后 getDiscover 立即可读到（数据库优先，种子数据仅兜底）。
 */
'use strict';

const crypto = require('crypto');

const TONE = {
  '学习': { bar: '#805CFA', barSoft: 'rgba(128,92,250,.10)' },
  '运动': { bar: '#29CA83', barSoft: 'rgba(41,202,131,.10)' },
  '娱乐': { bar: '#FFB020', barSoft: 'rgba(255,176,32,.14)' },
  '文体赛事': { bar: '#FFB020', barSoft: 'rgba(255,176,32,.14)' },
  '社团招新': { bar: '#805CFA', barSoft: 'rgba(128,92,250,.10)' },
  '讲座展览': { bar: '#69B9F5', barSoft: 'rgba(105,185,245,.12)' },
  '跑腿代办': { bar: '#FFB020', barSoft: 'rgba(255,176,32,.14)' },
  '其他求助': { bar: '#69B9F5', barSoft: 'rgba(105,185,245,.12)' }
};

/** 轻量校验 login 云函数签发的 token：openid.timestamp.sig */
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
  const title = String(event.title || '').trim();
  const place = String(event.place || '').trim();
  const time = String(event.time || '').trim();
  const type = String(event.type || '其他').trim();
  const total = Number(event.total) || 10;
  const price = String(event.price || '免费').trim();
  // 封面：只接受客户端已上传云存储的 http(s) 链接，否则回退默认图
  const rawCover = String(event.cover || '').trim();
  const cover = /^https?:\/\//.test(rawCover) ? rawCover.slice(0, 500) : '/static/art/art-campus.jpg';
  const openid = verifyToken(event.token);

  if (!title) return { errCode: 1, errMsg: '请填写标题' };
  if (!place || !time) return { errCode: 1, errMsg: '请选择时间和地点' };
  if (!openid) return { errCode: 401, errMsg: '登录态已失效，请重新登录' };

  // 统一分类体系：发布类型 → 发现页 tab + category
  const typeMap = {
    '学习搭子': { tab: 0, category: '学习' },
    '运动搭子': { tab: 0, category: '运动' },
    '娱乐聚会': { tab: 0, category: '娱乐' },
    '发起活动': { tab: 1, category: '文体赛事' },
    '活动招募': { tab: 1, category: '社团招新' },
    '技能教学': { tab: 0, category: '学习' },
    '学习': { tab: 0, category: '学习' },
    '运动': { tab: 0, category: '运动' },
    '娱乐': { tab: 0, category: '娱乐' },
    '教学': { tab: 0, category: '学习' },
    '跑腿': { tab: 2, category: '跑腿代办' },
    '其他': { tab: 2, category: '其他求助' }
  };
  const mapped = typeMap[type] || { tab: 0, category: '学习' };
  const category = mapped.category;
  const itemTab = mapped.tab;
  const tone = TONE[category] || TONE['学习'];
  const id = 'd' + Date.now();

  const doc = {
    id,
    tab: itemTab,
    category,
    hot: false,
    title,
    cover,
    time,
    place,
    joined: 0,
    total: Math.max(2, Math.min(100, total)),
    price: price || '免费',
    members: [],
    ...tone,
    type,
    createdBy: openid,
    createdAt: Date.now()
  };

  try {
    const db = uniCloud.database();
    const res = await db.collection('discover_items').add(doc);
    console.log('publishItem 写入成功:', id);
    return { errCode: 0, errMsg: 'ok', id, category, item: doc, addId: res && res.id };
  } catch (e) {
    console.error('publishItem error:', e);
    const msg = String(e && e.message || e);
    if (msg.indexOf('collection') >= 0 || msg.indexOf('not exist') >= 0) {
      return { errCode: 2, errMsg: '数据库还没有 discover_items 集合，请先在 uniCloud 控制台创建' };
    }
    return { errCode: 2, errMsg: '发布失败：' + msg };
  }
};
