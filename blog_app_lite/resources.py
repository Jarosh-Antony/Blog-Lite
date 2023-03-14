from flask_restful import Resource,fields,marshal
from flask_security import current_user, auth_token_required
from flask import request, redirect, url_for
from datetime import datetime
import os
from flask import current_app
from blog_app_lite import db
from blog_app_lite.models import User,Posts,Followings


post_rf={
    'id':fields.Integer,
    'title':fields.String,
    'description':fields.String,
    'timestamp':fields.String,
    'imageurl':fields.String
}
posts_rf={
    'posts':fields.List(fields.Nested(post_rf))
}

class Post(Resource):
    @auth_token_required
    def post(self):
        user_id=current_user.id
        title=request.form['title']
        time=datetime.now()
        
        if 'description' in request.form:
            desc=request.form['description']
        else:
            desc=None
        
        if 'image' in request.files:
            image = request.files['image']
            image_name=str(user_id)+'_'+time.strftime('%Y-%m-%d-%H-%M-%S-%f')+'_'+str(image.filename)
            imageurl=os.path.join(current_app.config['UPLOAD_FOLDER'],image_name)
            image.save(imageurl)
        else :
            imageurl=None
            
        newPost=Posts(title=title,description=desc,imageurl=imageurl,timestamp=str(time),userID=user_id)
        db.session.add(newPost)
        db.session.commit()    
        
        return 200
    
    @auth_token_required
    def get(self):
        user_id=current_user.id
        posts=Posts.query.filter_by(userID=user_id).all()
        
        return marshal({'posts':posts},posts_rf),200
        
        

class Follow(Resource):
    @auth_token_required
    def post(self):
        follower_id=current_user.id
        
        try:
            following_id=User.query.filter_by(username=request.json['to_follow']).first().id
        except:
            return 400
        if follower_id==following_id:
            return 400
            
        newFollow=Followings(follower_id=follower_id,following_id=following_id)
        db.session.add(newFollow)
        db.session.commit()
        
        return 200
        
        
class Feed(Resource):
    @auth_token_required
    def get(self):
        user_id=current_user.id
        following=Followings.query.filter_by(follower_id=user_id).all()
        following_id=[f.id for f in following]
        
        posts=[]
        for f_id in following_id:
            post=Posts.query.filter_by(userID=f_id).all()
            for p in post:
                posts.append(p)
        
       
        return marshal({'posts':posts},posts_rf),200


class Search(Resource):
    @auth_token_required
    def get(self):
        search=request.json['search'].split(' ')
        
        search_results=[]
        
        for s in search:
            s_r=User.query.filter_by(username=s).all()
            for sr in s_r:
                name_username={
                                'name':sr.name,
                                'username':sr.username}
                if name_username not in search_results:
                    search_results.append(name_username)
        
        return {'search_results':search_results},200