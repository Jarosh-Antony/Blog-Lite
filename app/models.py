# User

# primary key

# email (for most features - unique, non-nullable)

# password (string, nullable)

# active (boolean, non-nullable)

# fs_uniquifier (string, 64 bytes, unique, non-nullable)




# Role

# primary key

# name (unique, non-nullable)

# description (string)


from sqlalchemy.orm import relationship
from __main__ import db


class Users(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email=db.Column(db.String,nullable=False,unique=True)
    name = db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)
    active=db.Column(db.Boolean,nullable=False,default=True)
    fs_uniquifier=db.Column(db.String(64),nullable=False,unique=True)
    
    
class Roles(db.Model):
    __tablename__ = "Roles"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String,nullable=False)
    description=db.Column(db.String)