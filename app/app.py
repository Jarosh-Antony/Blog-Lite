from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_security import Security,SQLAlchemyUserDatastore,auth_token_required,RegisterForm

from wtforms import StringField
from wtforms.validators import DataRequired


app=Flask(__name__)
app.debug=True


import config


db=SQLAlchemy()
db.init_app(app)
app.app_context().push()


from models import User,Role,Post
from api import api

api.init_app(app)
app.app_context().push()

user_datastore = SQLAlchemyUserDatastore(db,User,Role)

class ExtendedRegisterForm(RegisterForm):
    name = StringField('Name', [DataRequired()])

app.security = Security(app, user_datastore,confirm_register_form=ExtendedRegisterForm)


if __name__ =='__main__':
    app.run()