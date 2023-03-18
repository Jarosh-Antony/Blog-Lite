from flask import render_template
from flask import current_app as app

@app.route("/",methods=["GET"])
def home():
    return render_template("home.html")
    
@app.route("/user/<string:username>",methods=['GET'])
def profile(username):
    return render_template("profile.html")