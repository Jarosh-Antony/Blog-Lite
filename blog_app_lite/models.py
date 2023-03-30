from blog_app_lite.DB import db
from flask_security import UserMixin, RoleMixin


class User(db.Model,UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String,nullable=False,unique=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    fs_uniquifier = db.Column(db.String(64), nullable=False, unique=True)
    profile_pic = db.Column(db.String,nullable=False, default='/static/dp/no_dp.png')
    last_seen = db.Column(db.String, nullable=False,default='0')
    post = db.relationship('Posts', cascade="all,delete", backref="User")
    roles = db.relationship('Role', secondary='roles_users',backref=db.backref('users', lazy='dynamic'))
    
    
    
class Role(db.Model,RoleMixin):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    
    
    
class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
    


class Posts(db.Model):
    __tablename__="post"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    imageName = db.Column(db.String)
    created = db.Column(db.String,nullable=False)
    modified = db.Column(db.String,nullable=False)
    userID = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    
    
class Followings(db.Model):
    __tablename__="follow"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_id=db.Column('follower', db.Integer,db.ForeignKey('user.id'),nullable=False)
    following_id=db.Column('following', db.Integer,db.ForeignKey('user.id'),nullable=False)
    
    
    
    