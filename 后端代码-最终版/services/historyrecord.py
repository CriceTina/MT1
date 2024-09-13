from datetime import datetime

from flask import jsonify, session
from models.historyrecord import db
from models.historyrecord import Historyrecord
from config import db_init as db
from services.user import session_store
from models.user import db
from models.user import User


def create_history_record(user_id, source_content, target_content, target_type):
    # user_id = session.get('user_id')

    new_history_record = Historyrecord(
        source_content=source_content,
        target_content=target_content,
        target_type=target_type,
        translate_time=datetime.utcnow(),
        user_id=user_id
    )

    # 保存到数据库
    db.session.add(new_history_record)
    db.session.commit()

    return new_history_record.to_dict()
