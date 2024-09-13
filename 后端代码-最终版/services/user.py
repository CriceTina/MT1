import requests
from models.user import db
from models.user import User
from flask import jsonify, session
from datetime import datetime
import uuid


def user_register(username, password):
    # 检查用户名是否已经存在
    u = User.query.filter_by(username=username).first()
    if u:
        return jsonify({"message": "用户名已存在"}), 201

    # 创建新用户
    new_user = User(
        username=username,
        password=password,
        registration_time=datetime.utcnow()  # 设置注册时间为当前时间
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "注册成功"})


session_store = {}
# 微信小程序的 AppID 和 AppSecret
WX_APPID = 'wx3d169f8dc19e1f06'  # 替换为你的微信小程序 AppID
WX_SECRET = 'cb41a29729c5ffdb1477b140431dfbe6'  # 替换为你的微信小程序 AppSecret


def user_login(username, password, code):
    u = User.query.filter_by(username=username).first()
    if u is None:
        # 用户不存在
        return jsonify({
            'code_1': -1,
            "message": "用户不存在",
            "data": ""
        }), 201
    u_dict = u.to_dict()

    if u_dict['password'] != password:
        # 用户存在 密码错误
        return jsonify({
            'code_1': -2,
            "message": "密码错误",
            "data": ""
        }), 202

    u.last_login_time = datetime.utcnow()  # 设置最近登录时间为当前时间
    db.session.commit()  # 提交更改

    wx_login_url = f"https://api.weixin.qq.com/sns/jscode2session?appid={WX_APPID}&secret={WX_SECRET}&js_code={code}&grant_type=authorization_code"
    wx_response = requests.get(wx_login_url)
    wx_data = wx_response.json()

    if 'openid' not in wx_data or 'session_key' not in wx_data:
        return jsonify({'code': 1, 'message': 'Failed to authenticate with WeChat'}), 401

    openid = wx_data['openid']
    session_key = wx_data['session_key']

    # 生成自定义的 session_id，并将其与 openid 和 session_key 关联
    session_id = str(uuid.uuid4())
    session_store[session_id] = {
        'username': username,
        'openid': openid,
        'session_key': session_key,
        'user_id': u.user_id  # 存储用户 ID
    }
    session['user_id'] = u.user_id,

    print('登录成功')
    print(session_id)
    # 返回 session_id 给小程序
    return jsonify({'code_1': 0,
                    'session_id': session_id,
                    'user_id': u.user_id,
                    'message': '登录成功'})


def user_change_password(current_user, new_password1, new_password2):
    # 验证原密码

    # 检查新密码是否匹配
    if new_password1 != new_password2:
        return jsonify({
            "message": "新密码不匹配",
            'code': -1
        }), 201

    # 更新用户密码
    current_user.password = new_password1
    db.session.commit()

    return jsonify({
        "message": "密码修改成功",
        'code': 0
    })


