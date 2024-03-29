#SECRET_KEY=os.getenv('SECRET_KEY')
#SECURITY_PASSWORD_SALT=os.getenv('SECURITY_PASSWORD_SALT')
SECURITY_TOKEN_AUTHENTICATION_HEADER='Authorization'
#SECURITY_USER_IDENTITY_ATTRIBUTES=
#SECURITY_CSRF_PROTECT_MECHANISMS=None
SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS=True
SECURITY_API_ENABLED_METHODS=['token']
SECURITY_BACKWARDS_COMPAT_AUTH_TOKEN=True
SECURITY_REGISTERABLE=True
SECURITY_SEND_REGISTER_EMAIL=False
SECURITY_USERNAME_ENABLE=True
SECURITY_USERNAME_REQUIRED=True

SECURITY_LOGIN_USER_TEMPLATE="security/enter_user.html"
SECURITY_LOGIN_URL='/enter'
#SECURITY_POST_REGISTER_VIEW='/'
#SECURITY_POST_LOGOUT_VIEW='/home'
# WTF_CSRF_ENABLED=False
# app.config['SESSION_COOKIE_NAME'] = None
SESSION_COOKIE_SECURE=True

#SQLALCHEMY_DATABASE_URI=os.getenv('DB')
SQLALCHEMY_TRACK_MODIFICATIONS=False

#UPLOAD_FOLDER=os.getenv('UPLOAD_FOLDER')


CACHE_TYPE='RedisCache'
CACHE_REDIS_HOST='localhost'
