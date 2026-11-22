/**
 * 云函数 itemDetail —— 活动详情
 * ------------------------------------------------------------------
 * 入参 { id }，按 id 在 discover_items / activities 里找单条活动。
 * 返回详情页所需字段。公开可读（未登录也能看详情）。
 */
'use strict';

exports.main = async (event = {}) => {
  const id = String(event.id || '').trim();
  if (!id) return { errCode: 1, errMsg: '缺少活动 id' };

  try {
    const db = uniCloud.database();
    for (const col of ['discover_items', 'activities']) {
      try {
        const q = await db.collection(col).where({ id }).limit(1).get();
        const it = q.data && q.data[0];
        if (!it) continue;
        return {
          errCode: 0,
          errMsg: 'ok',
          item: {
            id: it.id,
            title: it.title || '未命名活动',
            cover: it.cover || '/static/art/art-guitar.jpg',
            time: it.time || '',
            place: it.place || '',
            price: it.price || '免费',
            category: it.category || '校园活动',
            joined: Number(it.joined) || 0,
            total: Number(it.total) || 50,
            desc: it.desc || '',
            status: it.status || '报名中'
          }
        };
      } catch (e) {
        console.warn('查 ' + col + ' 失败:', e.message);
      }
    }
    return { errCode: 1, errMsg: '活动不存在或已下架' };
  } catch (e) {
    console.error('itemDetail error:', e);
    const msg = String((e && e.message) || e);
    if (msg.indexOf('request has expired') >= 0) {
      return { errCode: 2, errMsg: '本地调试数据库鉴权过期：请切到「连接云端云函数」' };
    }
    return { errCode: 2, errMsg: '获取详情失败：' + msg };
  }
};
