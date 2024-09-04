from models.systemnotification import db
from models.systemnotification import AnnouncementType, Systemnotification
from models.user import User
from config import db_init as db
from datetime import datetime

import socketio
from flask_socketio import SocketIO, emit


def create_notification(announce_type, announce_title, announce_content):
    new_notification = Systemnotification(
        announce_type=announce_type,
        announce_title=announce_title,
        # user_id=user_id,
        announce_content=announce_content,
        announce_time=datetime.utcnow()
    )

    # 保存到数据库
    db.session.add(new_notification)
    db.session.commit()

    return new_notification.to_dict()


def notify_all_users(announce_type, announce_title, announce_content, announce_id):
    # 获取所有用户
    users = User.query.all()
    notifications = []

    for user in users:
        notification = create_notification(announce_type, announce_title, announce_content)
        notifications.append(notification)

        # 发送 WebSocket 通知
        socketio.emit('notification', {
            'id:': announce_id,
            'type': announce_type,
            'title': announce_title,
            'content': announce_content
        }, room=user.user_id)  # 假设你有用户 ID 作为房间标识

    return notifications
