/**
 * 云函数 saveProfile —— 保存校园信息 / 昵称 / 兴趣
 * ------------------------------------------------------------------
 * 前端 profile-setup 完成资料后调用，写入 users 集合对应 openid 的记录。
 */
'use strict';

const crypto = require('crypto');

/** 与 login / publishItem 同款 token 校验 */
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

  const school = String(event.school || '').trim();
  const nickname = String(event.nickname || '').trim();
  // 头像：只接受客户端已上传云存储的 http(s) 链接
  const rawAvatar = String(event.avatar || '').trim();
  const avatar = /^https?:\/\//.test(rawAvatar) ? rawAvatar.slice(0, 500) : '';
  const interests = Array.isArray(event.interests)
    ? event.interests.map((x) => String(x).trim()).filter(Boolean).slice(0, 12)
    : [];

  if (!school && !nickname && !interests.length) {
    return { errCode: 1, errMsg: '没有要保存的资料' };
  }

  const patch = { updatedAt: Date.now() };
  if (school) patch.school = school;
  if (nickname) patch.nickname = nickname;
  if (avatar) patch.avatar = avatar;
  if (interests.length) patch.interests = interests;

  try {
    const db = uniCloud.database();
    const users = db.collection('users');
    const q = await users.where({ openid }).limit(1).get();
    const user = q.data && q.data[0];
    if (!user) {
      return { errCode: 404, errMsg: '用户不存在，请先登录' };
    }
    await users.doc(user._id).update(patch);

    // 返回给前端可直接覆盖本地缓存的 user 字段
    const nextUser = {
      id: user._id,
      nickname: nickname || user.nickname || '',
      avatar: avatar || user.avatar || '',
      points: typeof user.points === 'number' ? user.points : 0,
      school: school || user.school || '',
      interests: interests.length ? interests : (user.interests || [])
    };
    return { errCode: 0, errMsg: 'ok', user: nextUser };
  } catch (e) {
    console.error('saveProfile error:', e);
    const msg = String(e && e.message || e);
    if (msg.indexOf('request has expired') >= 0) {
      return { errCode: 2, errMsg: '本地调试数据库鉴权过期：请切到「连接云端云函数」' };
    }
    return { errCode: 2, errMsg: '保存失败：' + msg };
  }
};
