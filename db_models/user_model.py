from manage import db


#定义用户模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(36), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

