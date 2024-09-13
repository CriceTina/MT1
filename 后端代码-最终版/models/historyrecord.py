from config import db_init as db


class Historyrecord(db.Model):
    __tablename__ = 'historyrecord'  # 指定表名
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # id
    source_content = db.Column(db.String(300), nullable=False)  # 源语言文本
    target_content = db.Column(db.String(300), nullable=False)  # 目标语言文本
    translate_time = db.Column(db.DateTime, nullable=True)  # 翻译时间
    target_type = db.Column(db.String(300), nullable=False)  # 目标语言类型
    user_id = db.Column(db.Integer,nullable=True)  # id

    def to_dict(self):
        return {

            'history_id': self.history_id,
            'source_content': self.source_content,
            'target_content': self.target_content,
            'translate_time': self.translate_time,
            'target_type': self.target_type,
            'user_id':self.user_id
        }



