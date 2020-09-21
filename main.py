#!/usr/bin/env python
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:yu715825@localhost:3306/school'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 每次请求结束后都会自动提交数据库中的变动

db = SQLAlchemy(app)
manager = Manager(app)

# 初始化 DB 迁移工具
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


class Student(db.Model):
    '''定义 Student 的表结构'''
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    gender = db.Column(db.Enum('男', '女', '保密'))
    city = db.Column(db.String(10), nullable=False)
    birthday = db.Column(db.Date, default='1990-01-01')
    bio = db.Column(db.Text)
    money = db.Column(db.Float)


class Teacher(db.Model):
    __tablename__ = 'teacher'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    gender = db.Column(db.Enum('男', '女', '保密'))
    cur_cls = db.Column(db.String(20), nullable=False, unique=True)
    age = db.Column(db.Integer)


@app.route('/')
def home():
    users = Student.query.all()
    top3 = Student.query.order_by(Student.money.desc()).limit(3)
    return render_template('home.html', users=users, top3=top3)


@manager.command
def add_data():
    '''添加初始数据'''
    u1 = Student(name='tom', gender='男', city='北京',
                 birthday='1990-3-21', bio='哈哈哈', money=238)
    u2 = Student(name='lucy', gender='女', city='上海',
                 birthday='1995-9-12', bio='班花', money=736)
    u3 = Student(name='jack', gender='男', city='武汉',
                 birthday='1998-5-14', bio='啦啦啦', money=8632)
    u4 = Student(name='bob', gender='男', city='苏州',
                 birthday='1994-3-9', money=1986)
    u5 = Student(name='lily', gender='女', city='南京',
                 birthday='1992-3-17', bio='撸哇撸')
    u6 = Student(name='eva', gender='女', city='芜湖',
                 birthday='1987-7-28', bio='阿里斯顿将开放', money=862)
    u7 = Student(name='alex', gender='男', city='成都',
                 birthday='1974-2-5', bio='阿库建设东路附近阿斯顿发')
    u8 = Student(name='jam', gender='男', city='太原',
                 birthday='1999-5-26', money=871)
    u9 = Student(name='rob', gender='男', city='青岛',
                 birthday='1997-5-9')
    u10 = Student(name='ella', gender='女', city='大连',
                  birthday='1999-9-7', bio='酷狗豆腐', money=8128)

    db.session.add_all([u1, u2, u3, u4, u5, u6, u7, u8, u9, u10])
    db.session.commit()


if __name__ == "__main__":
    manager.run()
    