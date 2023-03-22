from flask_restful import Resource,fields,marshal
from flask_security import current_user, auth_token_required
from flask import request, redirect, url_for
from datetime import datetime
import os
from flask import current_app as app
from blog_app_lite import db
from sqlalchemy import func
from blog_app_lite.models import User,Posts,Followings


post_rf={
    'id':fields.Integer,
    'title':fields.String,
    'description':fields.String,
    'created':fields.String,
    'modified':fields.String,
    'imageurl':fields.String,
    'username':fields.String,
    'name':fields.String
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
            imageurl=os.path.join(app.config['UPLOAD_FOLDER'],image_name)
            image.save(imageurl)
        else :
            imageurl=None
            
        newPost=Posts(title=title,description=desc,imageurl=imageurl,created=str(time),modified=str(time),userID=user_id)
        db.session.add(newPost)
        db.session.commit()    
        
        return 200
    
    @auth_token_required
    def get(self):
        username=request.args.get('username')
        posts_query=(
            db.select(Posts)
            .join(User,User.id==Posts.userID)
            .where(User.username==username)
            .order_by(Posts.created.desc())
        )
        posts=db.session.execute(posts_query).scalars().all()
        
        return marshal({'posts':posts},posts_rf),200
        
    @auth_token_required
    def put(self):
        user_id=current_user.id
        post_id=request.args.get('id')
        
        post=Posts.query.filter_by(id=post_id,userID=user_id).first()
        if post==None:
            return 400
        
        post.title=request.form['title']
        time=datetime.now()
        
        if 'description' in request.form:
            post.description=request.form['description']
        else:
            post.description=None
        
        if post.imageurl is not None:
            os.remove(post.imageurl)
        
        if 'image' in request.files:
            image = request.files['image']
            image_name=str(user_id)+'_'+time.strftime('%Y-%m-%d-%H-%M-%S-%f')+'_'+str(image.filename)
            post.imageurl=os.path.join(app.config['UPLOAD_FOLDER'],image_name)
            image.save(post.imageurl)
        else :
            post.imageurl=None
            
        post.modified=str(time)
        db.session.commit()
        
        return 200
    
    @auth_token_required
    def delete(self):
        user_id=current_user.id
        post_id=request.json['id']
        post=Posts.query.filter_by(id=post_id,userID=user_id).first()
        if post==None:
            return 400
        
        if post.imageurl is not None:
            os.remove(post.imageurl)
        db.session.delete(post)
        db.session.commit()
        
        return 200



class Follow(Resource):
    @auth_token_required
    def post(self):
        follower_id=current_user.id
        
        try:
            following_id=User.query.filter_by(username=request.json['follow']).first().id
        except:
            return 400
        if follower_id==following_id:
            return 400
            
        newFollow=Followings(follower_id=follower_id,following_id=following_id)
        db.session.add(newFollow)
        db.session.commit()
        
        return 200
        
    @auth_token_required
    def delete(self):
        follower_id=current_user.id
        
        try:
            following_id=User.query.filter_by(username=request.json['follow']).first().id
        except:
            return 400
        
        follow=Followings.query.filter_by(follower_id=follower_id,following_id=following_id).first()
        if follow == None:
            return 400
        
        db.session.delete(follow)
        db.session.commit()
        
        return 200
        
class Feed(Resource):
    @auth_token_required
    def get(self):
        user=current_user
        
        posts_query=(
            db.select(Posts,User.username,User.name)
            .join(Followings,Followings.following_id==Posts.userID)
            .join(User,User.id==Posts.userID)
            .where(Followings.follower_id==user.id)
            .order_by(Posts.created.desc())
        )
        result=db.session.execute(posts_query)
        
        posts=[]
        for post,username,name in result:
            post.username=username
            post.name=name
            posts.append(post)
        
        return marshal({'posts':posts},posts_rf),200


class Search(Resource):
    @auth_token_required
    def get(self):
        search=request.json['search'].split(' ')
        
        search_results=[]
        
        s_r=User.query.all()
        for s in search:
            for sr in s_r:
                
                if sr.username.lower()==s.lower() or s.lower() in [name.lower() for name in sr.name.split()]:
                    name_username={
                                    'name':sr.name,
                                    'username':sr.username}
                    if name_username not in search_results:
                        search_results.append(name_username)
        
        return {'search_results':search_results},200


class Statistics(Resource):
    @auth_token_required
    def get(self):
        username=request.args.get('username')
        data={}
        
        user_query=(
            db.select(User.name,User.id)
            .where(User.username==username)
        )
        user=db.session.execute(user_query).first()
        data['name']=user[0]
        
        posts_query=(
            db.select(func.count())
            .select_from(Posts)
            .where(user[1]==Posts.userID)
        )
        data['posts']=db.session.execute(posts_query).scalar()
        
        followings_query=(
            db.select(func.count())
            .select_from(Followings)
            .where(Followings.follower_id==user[1])
        )
        data['followings']=db.session.execute(followings_query).scalar()
        
        followers_query=(
            db.select(func.count())
            .select_from(Followings)
            .where(Followings.following_id==user[1])
        )
        data['followers']=db.session.execute(followers_query).scalar()
        return data,200