import secrets
import os
from __main__ import app

app.config['SECRET_KEY']=secrets.token_urlsafe()
#app.config['SECURITY_USER_IDENTITY_ATTRIBUTES']=
app.config['SECURITY_API_ENABLED_METHODS']=['token']
app.config['SECURITY_BACKWARDS_COMPAT_AUTH_TOKEN']=True


app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.realpath('../blogs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False