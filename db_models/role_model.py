from manage import db

#定义角色模型, 角色有两种: 管理员, 普通用户
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    userslalala = db.relationship('User', backref = 'rolelalala')
