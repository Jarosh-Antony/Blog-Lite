from flask import render_template
from flask import current_app as app
from blog_app_lite.cache import cache

@app.route("/",methods=["GET"])
@cache.cached(timeout=3600)
def home():
    return render_template("home.html")
    
@app.route("/user/<string:username>",methods=['GET'])
@cache.cached(timeout=3600,make_cache_key='user_profile_view')
def profile(username):
    return render_template("profile.html")
    
@app.route("/exports",methods=['GET'])
@cache.cached(timeout=3600)
def exports():
    return render_template("exports.html")