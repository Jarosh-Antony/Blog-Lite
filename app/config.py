import os
from __main__ import app
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT']=os.getenv('SECURITY_PASSWORD_SALT')
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER']='Authorization'
#app.config['SECURITY_USER_IDENTITY_ATTRIBUTES']=
#app.config['SECURITY_CSRF_PROTECT_MECHANISMS']=None
app.config['SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS']=True
app.config['SECURITY_API_ENABLED_METHODS']=['token']
app.config['SECURITY_BACKWARDS_COMPAT_AUTH_TOKEN']=True
app.config['SECURITY_REGISTERABLE']=True
app.config['SECURITY_SEND_REGISTER_EMAIL']=False

#app.config['SECURITY_LOGIN_URL']='/login?
#app.config['SECURITY_POST_REGISTER_VIEW']='/'
#app.config['SECURITY_POST_LOGOUT_VIEW']='/home'

#app.config['SESSION_COOKIE_NAME'] = None
app.config['SESSION_COOKIE_SECURE'] = True

app.config['SQLALCHEMY_DATABASE_URI']=os.getenv('DB')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config['UPLOAD_FOLDER']="../post_images"