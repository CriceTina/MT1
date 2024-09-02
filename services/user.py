from models.user import db
from models.user import User
from flask import jsonify


def user_register(username, password):
    # 检查用户名是否已经存在
    u = User.query.filter_by(username=username).first()
    if u:
        return jsonify({"message": "用户名已存在"}), 400

    # 创建新用户
    new_user = User(username=username, password=password)
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

    return jsonify({
        'code': 0,
        "message": "登录成功",
        "data": u_dict
    })


