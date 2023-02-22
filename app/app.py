from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_security import Security,SQLAlchemyUserDatastore,auth_token_required


app=Flask(__name__)
app.debug=True


import config


db=SQLAlchemy()
db.init_app(app)
app.app_context().push()


from models import Users,Roles


api = Api(app)
app.app_context().push()


user_datastore = SQLAlchemyUserDatastore(db,Users,Roles)
app.security = Security(app,user_datastore)


@app.route("/")
@auth_token_required
def index():
    return render_template("home.html")



if __name__ =='__main__':
    app.run()