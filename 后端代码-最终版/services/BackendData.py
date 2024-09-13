from datetime import datetime, timedelta

from flask import jsonify
from config import db_init as db

from models.BackendData import BackendData


def getBackendData():
    time_of_the_day = db.Column(db.DateTime, default=datetime.utcnow)

    # 查询时间最晚的记录
    latest_record = BackendData.query.order_by(BackendData.time_of_the_day.desc()).first()

    # 构建后台数据信息列表
    backend_data_info = None
    if latest_record:
        backend_data_info = [
            {
                "backendData_id": latest_record.backendData_id,
                "onlineuser_qty": latest_record.onlineuser_qty,
                "user_qty": latest_record.user_qty,
                "char_qty": latest_record.char_qty,
                "file_qty": latest_record.file_qty,
                "pic_qty": latest_record.pic_qty,
                "speech_qty": latest_record.speech_qty,
                "time_of_the_day": latest_record.time_of_the_day.strftime("%Y-%m-%d %H:%M:%S")
            }
        ]

    # 构建响应数据，包括后台数据信息列表
    response_data = {
        "backend_data": backend_data_info
    }

    # 返回响应数据
    return jsonify(response_data), 200


def listData():
    time_of_the_day = db.Column(db.DateTime, default=datetime.utcnow)

    # 查询时间最晚的记录
    latest_record = BackendData.query.order_by(BackendData.time_of_the_day.desc()).first()
    backend_data_info = None
    if latest_record:
        backend_data_info = [
            {
                "value": latest_record.char_qty,
                "name": "翻译文字数量"
            },
            {
                "value": latest_record.file_qty,
                "name": "翻译文件数量"
            },
            {
                "value": latest_record.pic_qty,
                "name": "翻译图片数量"
            },
            {
                "value": latest_record.speech_qty,
                "name": "翻译语音数量"
            }
        ]
        response_data = {
            "backend_data": backend_data_info
        }

        # 返回响应数据
        return jsonify(response_data), 200


def LineData():
    BackendDatas = BackendData.query.all()
    BackendData_count = BackendData.query.count()
    backend_data_info = []
    for i in range(BackendData_count):
        date_str = BackendDatas[i].time_of_the_day.strftime("%Y-%m-%d %H:%M:%S")
        timestamp = int(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
        onlineuser_qty = int(BackendDatas[i].onlineuser_qty)
        list1 = [timestamp, onlineuser_qty]
        backend_data_info.append(list1)
    # 将用户信息列表和用户总数封装在一起
    response_data = {
        "total": BackendData_count,
        "BackendDatas": backend_data_info
    }

    return jsonify(response_data), 200

