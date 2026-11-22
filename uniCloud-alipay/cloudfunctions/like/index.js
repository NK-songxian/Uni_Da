/**
 * 云函数 like —— 帖子点赞
 * ------------------------------------------------------------------
 * action:
 *   check  {token, postId} → { liked }
 *   toggle {token, postId} → { liked, likes }
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

exports.main = async (event = {}) => {
  const openid = verifyToken(event.token);
  if (!openid) return { errCode: 401, errMsg: '登录态已失效，请重新登录' };

  const action = event.action || 'toggle';
  const postId = String(event.postId || '').trim();
  if (!postId) return { errCode: 1, errMsg: '缺少 postId' };

  try {
    const db = uniCloud.database();
    const likes = db.collection('likes');
    const posts = db.collection('posts');

    const pq = await posts.where({ id: postId }).limit(1).get();
    const post = pq.data && pq.data[0];

    const lq = await likes.where({ openid, postId }).limit(1).get();
    const liked = !!(lq.data && lq.data.length);

    if (action === 'check') {
      return { errCode: 0, errMsg: 'ok', liked };
    }

    if (liked) {
      await likes.doc(lq.data[0]._id).remove();
      const next = Math.max(0, (Number(post && post.likes) || 0) - 1);
      if (post) await posts.doc(post._id).update({ likes: next });
      return { errCode: 0, errMsg: 'ok', liked: false, likes: next };
    }

    await likes.add({ openid, postId, createdAt: Date.now() });
    const next = (Number(post && post.likes) || 0) + 1;
    if (post) {
      await posts.doc(post._id).update({ likes: next });
      // 互动通知：写给帖子作者（排除种子帖和自己）
      if (post.authorOpenid && post.authorOpenid !== 'seed' && post.authorOpenid !== openid) {
        try {
          const dbu = await uniCloud.database().collection('users').where({ openid }).limit(1).get();
          const uname = (dbu.data && dbu.data[0] && dbu.data[0].nickname) || '同学';
          await uniCloud.database().collection('notifications').add({
            openid: post.authorOpenid,
            type: 'interact',
            title: '收到新点赞',
            text: uname + ' 赞了你的帖子「' + String(post.text || '').slice(0, 15) + '…」',
            link: '/pages/post-detail/post-detail?id=' + postId,
            read: false,
            createdAt: Date.now()
          });
        } catch (e) { console.warn('通知写入失败:', e.message); }
      }
    }
    return { errCode: 0, errMsg: 'ok', liked: true, likes: next };
  } catch (e) {
    console.error('like error:', e);
    const msg = String((e && e.message) || e);
    if (msg.indexOf('request has expired') >= 0) {
      return { errCode: 2, errMsg: '本地调试数据库鉴权过期：请切到「连接云端云函数」' };
    }
    return { errCode: 2, errMsg: '点赞失败：' + msg };
  }
};
