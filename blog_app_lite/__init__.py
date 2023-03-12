from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_security import Security,SQLAlchemyUserDatastore,auth_token_required,RegisterForm

from wtforms import StringField
from wtforms.validators import DataRequired

# import config

from dotenv import load_dotenv,dotenv_values
load_dotenv()

class ExtendedRegisterForm(RegisterForm):
    name = StringField('Name', [DataRequired()])

app=None
db=None

def create_app(configuration=None):
    global app,db
    app=Flask(__name__)
    app.debug=True
    
    if not configuration == None:
        app.config.from_mapping(configuration)
    app.config.from_mapping(dotenv_values())
    app.config.from_pyfile('config.py', silent=True)

    db=SQLAlchemy()
    db.init_app(app)
    app.app_context().push()
    
    
    from blog_app_lite.models import User,Role
    from blog_app_lite.api import api
    
    api.init_app(app)
    app.app_context().push()

    user_datastore = SQLAlchemyUserDatastore(db,User,Role)
    app.security = Security(app, user_datastore,register_form=ExtendedRegisterForm,confirm_register_form=ExtendedRegisterForm)
    
    return app

print('NAME ===============',__name__)
if __name__ =='__main__':
    
    create_app()
    app.run()