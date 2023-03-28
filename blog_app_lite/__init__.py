from flask import Flask
from flask import current_app
from flask import render_template
from flask_restful import Api
from flask_security import Security,SQLAlchemyUserDatastore,auth_token_required,RegisterForm

from wtforms import StringField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from blog_app_lite import workers
from dotenv import load_dotenv,dotenv_values
load_dotenv()

class ExtendedRegisterForm(RegisterForm):
    name = StringField('Name', [DataRequired()])

celery=None
def create_app(configuration=None,itis=None):
    
    app=Flask(__name__)
    app.debug=True
    
    if not configuration == None:
        app.config.from_mapping(configuration)
    app.config.from_mapping(dotenv_values())
    app.config.from_pyfile('config.py', silent=True)
    
    from blog_app_lite.DB import db
    db.init_app(app)
    app.app_context().push()

    from blog_app_lite.models import User,Role
    from blog_app_lite.api import api
    from blog_app_lite import routes
    
    api.init_app(app)
    app.app_context().push()
    
    celery=workers.celery
    celery.conf.update(
        broker_url = 'redis://localhost:6379/0',
        result_backend = 'redis://localhost:6379/1'
    )
    celery.Task=workers.ContextTask
    app.app_context().push()
    
    user_datastore = SQLAlchemyUserDatastore(db,User,Role)
    app.security=Security(app, user_datastore,register_form=ExtendedRegisterForm,confirm_register_form=ExtendedRegisterForm)
    if not itis== None:
        return app,celery
    return app

print('NAME =========================================================================',__name__)
if __name__ =='__main__':
    
    app=create_app()
    app.run()
    
if __name__=='blog_app_lite.__init__':
    app,celery=create_app(itis='celery')
    