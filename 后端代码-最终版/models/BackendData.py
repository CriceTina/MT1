from config import db_init as db
from datetime import datetime

class BackendData(db.Model):
    __tablename__ = 'backenddata'  # 指定表名

    backendData_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 后台数据ID
    onlineuser_qty = db.Column(db.Integer, nullable=False)  # 在线用户数量
    user_qty = db.Column(db.Integer, nullable=False)  # 用户总数量
    char_qty = db.Column(db.Integer, nullable=False)  # 翻译的文本数量
    file_qty = db.Column(db.Integer, nullable=False)  # 翻译的文件数量
    pic_qty = db.Column(db.Integer, nullable=False)  # 翻译的图片数量
    speech_qty = db.Column(db.Integer, nullable=False)  # 翻译的语音数量
    time_of_the_day = db.Column(db.DateTime, default=datetime.utcnow)  # 当日时间

    def to_dict(self):
        return {
            'backendData_id': self.backendData_id,
            'onlineuser_qty': self.onlineuser_qty,
            'user_qty': self.user_qty,

            'char_qty': self.char_qty,
            'file_qty': self.file_qty,
            'pic_qty': self.pic_qty,
            'speech_qty': self.speech_qty,
            'time_of_the_day': self.time_of_the_day.strftime("%Y-%m-%d %H:%M:%S")
        }


