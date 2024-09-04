from models.user import db
from models.user import User
from flask import jsonify, session
from datetime import datetime


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


def user_login(username, password):
    u = User.query.filter_by(username=username).first()
    if u is None:
        # 用户不存在
        return jsonify({
            'code': -1,
            "message": "用户不存在",
            "data": ""
        }), 201
    u_dict = u.to_dict()

    if u_dict['password'] != password:
        # 用户存在 密码错误
        return jsonify({
            'code': -2,
            "message": "密码错误",
            "data": ""
        }), 202

    u.last_login_time = datetime.utcnow()  # 设置最近登录时间为当前时间
    db.session.commit()  # 提交更改
    session.permanent = True  # 设置session为永久有效
    session['username'] = username
    return jsonify({
        'code': 0,
        "message": "登录成功",
        "data": u_dict,
    })


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
