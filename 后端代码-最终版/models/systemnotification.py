from enum import Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from sqlalchemy import Enum

from config import db_init as db

from models.user import db
from models.user import User


class AnnouncementType(PyEnum):
    NEW_VERSION_UPDATE = '新版本更新'
    ACCOUNT_SECURITY_ALERT = '账户安全提醒'
    TRANSLATION_TASK_ALERT = '翻译任务提醒'


class Systemnotification(db.Model):
    __tablename__ = 'systemnotification'  # 指定表名
    announce_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 系统通知ID
    announce_type = db.Column(db.String(50), nullable=False)  # 系统通知类型
    announce_title = db.Column(db.String(50), nullable=False)  # 系统通知标题

    announce_time = db.Column(db.DateTime, nullable=False)  # 系统通知发布时间
    announce_content = db.Column(db.String(255), nullable=False)  # 系统通知内容

    def to_dict(self):
        return {
            'announce_id': self.announce_id,
            'announce_type': self.announce_type,
            'announce_title': self.announce_title,
            'announce_time': self.announce_time,
            'announce_content': self.announce_content,

        }



