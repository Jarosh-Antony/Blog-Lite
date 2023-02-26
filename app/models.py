from __main__ import db
from flask_security import UserMixin, RoleMixin

class User(db.Model,UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    fs_uniquifier = db.Column(db.String(64), nullable=False, unique=True)
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
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
    
