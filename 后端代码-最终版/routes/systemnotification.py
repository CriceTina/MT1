from flask import Blueprint, request, jsonify
from services.systemnotification import create_notification, notify_all_users, get_all_notifications
from flask_socketio import SocketIO
from models.systemnotification import AnnouncementType, Systemnotification

ss = Blueprint('ss', __name__)


@ss.route('/a', methods=['POST'])
def send_notification():
    # 使用 request.form 获取表单数据

    data = request.get_json()

    announce_type = data.get('announce_type')
    announce_title = data.get('announce_title')
    announce_content = data.get('announce_content')
    announce_id = data.get('announce_id')
    # 检查请求数据
    if not all([announce_type, announce_title, announce_content]):
        return jsonify({"message": "缺少必要字段"}), 403

    # 调用业务逻辑层发送通知给所有用户
    create_notification(announce_type, announce_title, announce_content)

    print("接收到的管理员通知参数:", announce_type, announce_title, announce_content)
    return jsonify({"message": "通知已发送"}), 200


@ss.route('/user_query_notification', methods=['POST'])
def view_notification():
    return get_all_notifications()


