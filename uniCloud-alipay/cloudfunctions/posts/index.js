/**
 * 云函数 posts —— 社区帖子系统
 * ------------------------------------------------------------------
 * action:
 *   list    {token?, tab?}        → { list, likedIds, favedIds }（空集合自动写入 3 条种子帖）
 *   mine    {token}               → { list } 我发布的帖子
 *   detail  {postId, token?}      → { post, comments }
 *   publish {token, tag, text}    → { post }
 *   comment {token, postId, text} → { comment }
 *   remove  {token, postId}       → { ok }
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

function mapPost(x, likedIds, favedIds) {
  return {
    id: x.id,
    user: x.authorName || '同学',
    tone: x.tone || 'purple',
    campus: x.campus || '阳光大学',
    time: x.timeText || '',
    ts: x.createdAt || 0,
    tag: x.tag || '校园生活',
    text: x.text || '',
    images: x.images || [],
    likes: Number(x.likes) || 0,
    comments: Number(x.comments) || 0,
    favs: Number(x.favs) || 0,
    liked: !!(likedIds && likedIds.indexOf(x.id) >= 0),
    faved: !!(favedIds && favedIds.indexOf(x.id) >= 0)
  };
}

const SEEDS = [
  {
    id: 'seed-astar',
    authorOpenid: 'seed',
    authorName: '阿星',
    tone: 'purple',
    campus: '阳光大学',
    tag: '校园生活',
    text: '今天的晚霞也太美了吧！中心湖边随手一拍就是大片，分享给同样热爱生活的小伙伴们～',
    images: ['linear-gradient(135deg,#FF8A3D,#FFD76A)', 'linear-gradient(135deg,#805CFA,#B59BFF)'],
    likes: 128,
    comments: 0,
    favs: 36
  },
  {
    id: 'seed-lin',
    authorOpenid: 'seed',
    authorName: '小林同学',
    tone: 'green',
    campus: '阳光大学',
    tag: '找搭子',
    text: '有人一起去图书馆刷题吗？期末了，互相监督！位置已经占好啦，三楼靠窗～',
    images: [],
    likes: 45,
    comments: 0,
    favs: 12
  },
  {
    id: 'seed-wanzi',
    authorOpenid: 'seed',
    authorName: '丸子',
    tone: 'orange',
    campus: '阳光大学',
    tag: '社团活动',
    text: '周六下午街舞社在天台有公开课，零基础也能来玩，带上水就行！',
    images: ['linear-gradient(135deg,#F472B6,#FF8A3D)'],
    likes: 89,
    comments: 0,
    favs: 27
  }
];

async function ensureSeeds(posts) {
  const q = await posts.limit(1).get();
  if (q.data && q.data.length) return;
  const now = Date.now();
  const rows = SEEDS.map((s, i) => ({
    ...s,
    timeText: '',
    createdAt: now - (i + 1) * 3600 * 1000
  }));
  for (const r of rows) {
    try { await posts.add(r); } catch (e) { console.warn('seed fail:', e.message); }
  }
}

exports.main = async (event = {}) => {
  const action = event.action || 'list';
  const openid = verifyToken(event.token);
  // list/detail 允许未登录浏览，写操作必须登录
  const needLogin = ['publish', 'comment', 'remove', 'mine'];
  if (needLogin.indexOf(action) >= 0 && !openid) {
    return { errCode: 401, errMsg: '登录态已失效，请重新登录' };
  }

  const postId = String(event.postId || '').trim();
  const text = String(event.text || '').trim().slice(0, 500);

  try {
    const db = uniCloud.database();
    const posts = db.collection('posts');
    const comments = db.collection('post_comments');

    if (action === 'list') {
      await ensureSeeds(posts);
      const q = await posts.orderBy('createdAt', 'desc').limit(20).get();
      const ids = (q.data || []).map((x) => x.id);
      let likedIds = [];
      let favedIds = [];
      if (openid && ids.length) {
        const dbCmd = db.command;
        const lq = await db.collection('likes').where({ openid, postId: dbCmd.in(ids) }).get();
        likedIds = (lq.data || []).map((x) => x.postId);
        const fq = await db.collection('favorites').where({ openid, type: 'post', targetId: dbCmd.in(ids) }).get();
        favedIds = (fq.data || []).map((x) => x.targetId);
      }
      const list = (q.data || []).map((x) => mapPost(x, likedIds, favedIds));
      return { errCode: 0, errMsg: 'ok', list, likedIds, favedIds };
    }

    if (action === 'mine') {
      const q = await posts.where({ authorOpenid: openid }).orderBy('createdAt', 'desc').limit(50).get();
      return { errCode: 0, errMsg: 'ok', list: (q.data || []).map((x) => mapPost(x, [], [])) };
    }

    if (action === 'detail') {
      if (!postId) return { errCode: 1, errMsg: '缺少 postId' };
      const q = await posts.where({ id: postId }).limit(1).get();
      const p = q.data && q.data[0];
      if (!p) return { errCode: 1, errMsg: '帖子不存在或已被删除' };
      let liked = false;
      let faved = false;
      if (openid) {
        const lq = await db.collection('likes').where({ openid, postId }).limit(1).get();
        liked = !!(lq.data && lq.data.length);
        const fq = await db.collection('favorites').where({ openid, type: 'post', targetId: postId }).limit(1).get();
        faved = !!(fq.data && fq.data.length);
      }
      const cq = await comments.where({ postId }).orderBy('createdAt', 'asc').limit(50).get();
      const commentList = (cq.data || []).map((c) => ({
        id: c._id,
        name: c.name || '同学',
        tone: c.tone || 'purple',
        text: c.text || '',
        ts: c.createdAt || 0
      }));
      return { errCode: 0, errMsg: 'ok', post: mapPost(p, liked ? [postId] : [], faved ? [postId] : []), comments: commentList };
    }

    if (action === 'publish') {
      if (!text) return { errCode: 1, errMsg: '说点什么再发布吧' };
      const uq = await db.collection('users').where({ openid }).limit(1).get();
      const user = uq.data && uq.data[0];
      const now = Date.now();
      // 配图：只接受 http(s) 链接（客户端已上传云存储），最多 9 张
      const images = Array.isArray(event.images)
        ? event.images.map((x) => String(x || '')).filter((x) => /^https?:\/\//.test(x)).slice(0, 9)
        : [];
      const doc = {
        id: 'p' + now + Math.floor(Math.random() * 90 + 10),
        authorOpenid: openid,
        authorName: (user && user.nickname) || '同学',
        tone: 'purple',
        campus: (user && user.school) || '阳光大学',
        tag: String(event.tag || '校园生活').slice(0, 12),
        text,
        images,
        likes: 0,
        comments: 0,
        favs: 0,
        timeText: '',
        createdAt: now
      };
      await posts.add(doc);

      // 发布奖励：+5 积分并写流水
      if (user) {
        try {
          const next = (Number(user.points) || 0) + 5;
          await db.collection('users').doc(user._id).update({ points: next });
          await db.collection('point_ledgers').add({
            openid, type: 'publish', title: '发布动态奖励', delta: 5,
            balance: next, refId: doc.id, createdAt: now
          });
        } catch (e) { console.warn('积分奖励写入失败:', e.message); }
      }
      return { errCode: 0, errMsg: 'ok', post: mapPost(doc, [], []) };
    }

    if (action === 'comment') {
      if (!postId) return { errCode: 1, errMsg: '缺少 postId' };
      if (!text) return { errCode: 1, errMsg: '评论内容不能为空' };
      const uq = await db.collection('users').where({ openid }).limit(1).get();
      const user = uq.data && uq.data[0];
      const now = Date.now();
      const doc = {
        postId,
        openid,
        name: (user && user.nickname) || '我',
        tone: 'purple',
        text,
        createdAt: now
      };
      const added = await comments.add(doc);
      const pq = await posts.where({ id: postId }).limit(1).get();
      const p = pq.data && pq.data[0];
      if (p) {
        await posts.doc(p._id).update({ comments: (Number(p.comments) || 0) + 1 });
        // 互动通知：写给帖子作者（排除种子帖和自己）
        if (p.authorOpenid && p.authorOpenid !== 'seed' && p.authorOpenid !== openid) {
          try {
            await db.collection('notifications').add({
              openid: p.authorOpenid,
              type: 'interact',
              title: '收到新评论',
              text: (user && user.nickname || '同学') + ' 评论了你的帖子「' + String(p.text || '').slice(0, 15) + '…」',
              link: '/pages/post-detail/post-detail?id=' + postId,
              read: false,
              createdAt: Date.now()
            });
          } catch (e) { console.warn('通知写入失败:', e.message); }
        }
      }
      return {
        errCode: 0,
        errMsg: 'ok',
        comment: { id: added.id, name: doc.name, tone: doc.tone, text: doc.text, ts: now }
      };
    }

    if (action === 'remove') {
      if (!postId) return { errCode: 1, errMsg: '缺少 postId' };
      const q = await posts.where({ id: postId }).limit(1).get();
      const p = q.data && q.data[0];
      if (!p) return { errCode: 1, errMsg: '帖子不存在' };
      if (p.authorOpenid !== openid) return { errCode: 1, errMsg: '只能删除自己的帖子' };
      await posts.doc(p._id).remove();
      try { await comments.where({ postId }).remove(); } catch (e) {}
      return { errCode: 0, errMsg: 'ok' };
    }

    return { errCode: 1, errMsg: '未知 action' };
  } catch (e) {
    console.error('posts error:', e);
    const msg = String((e && e.message) || e);
    if (msg.indexOf('request has expired') >= 0) {
      return { errCode: 2, errMsg: '本地调试数据库鉴权过期：请切到「连接云端云函数」' };
    }
    return { errCode: 2, errMsg: '帖子操作失败：' + msg };
  }
};
