from flask_restful import Resource,fields,marshal
from flask_security import current_user, auth_token_required
from flask import request, redirect, url_for,send_file
from datetime import datetime
import os
from flask import current_app as app
from blog_app_lite.DB import db
from sqlalchemy import func,and_
from blog_app_lite.models import User,Posts,Followings
from blog_app_lite.async_jobs.tasks import dailyPDF

post_rf={
    'id':fields.Integer,
    'title':fields.String,
    'description':fields.String,
    'created':fields.String,
    'modified':fields.String,
    'imageName':fields.String,
    'imageurl':fields.String,
    'username':fields.String,
    'name':fields.String,
    'profile_pic':fields.String
}
posts_rf={
    'posts':fields.List(fields.Nested(post_rf))
}

class Post(Resource):
    @auth_token_required
    def post(self):
        user_id=current_user.id
        username=current_user.username
        
        title=request.form['title']
        time=datetime.now()
        if 'description' in request.form:
            desc=request.form['description']
        else:
            desc=None
        
        if 'image' in request.files:
            image = request.files['image']
            imageName=str(username)+'_'+time.strftime('%Y-%m-%d-%H-%M-%S-%f')+'_'+str(image.filename)
            image.save(os.path.join(app.config['POST_FOLDER'],imageName))
        else :
            imageName=None
            
        newPost=Posts(title=title,description=desc,imageName=imageName,created=str(time),modified=str(time),userID=user_id)
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
        username=current_user.username
        post_id=request.form['id']
        
        post=Posts.query.filter_by(id=post_id,userID=user_id).first()
        if post==None:
            return 400
        
        post.title=request.form['title']
        time=datetime.now()
        
        if 'description' in request.form:
            post.description=request.form['description']
        else:
            post.description=None
        
        if post.imageName is not None:
            os.remove(app.config['POST_FOLDER']+post.imageName)
        
        if 'image' in request.files:
            image = request.files['image']
            post.imageName=str(username)+'_'+time.strftime('%Y-%m-%d-%H-%M-%S-%f')+'_'+str(image.filename)
            image.save(app.config['POST_FOLDER']+post.imageName)
        else :
            post.imageName=None
            
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
        
        if post.imageName is not None:
            os.remove(app.config['POST_FOLDER']+post.imageName)
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
            db.select(Posts,User.username,User.name,User.profile_pic)
            .join(Followings,Followings.following_id==Posts.userID)
            .join(User,User.id==Posts.userID)
            # .where(and_(Followings.follower_id==user.id,Posts.modified>=user.last_seen))
            .where(Followings.follower_id==user.id)
            .order_by(Posts.created.desc())
        )
        result=db.session.execute(posts_query)
        
        posts=[]
        for post,username,name,profile_pic in result:
            post.username=username
            post.name=name
            post.profile_pic=profile_pic
            posts.append(post)
        
        user.last_seen=str(datetime.now())
        db.session.commit()
        return marshal({'posts':posts},posts_rf),200


class Search(Resource):
    @auth_token_required
    def get(self):
        search=request.args.get('search').split()
        search_results=[]
        
        s_r=User.query.all()
        for s in search:
            for sr in s_r:
                
                if sr.username.lower()==s.lower() or s.lower() in [name.lower() for name in sr.name.split()]:
                    name_username={
                                    'name':sr.name,
                                    'username':sr.username,
                                    'profile_pic':sr.profile_pic
                                }
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
        
        isFollowing_query=(
            db.select(Followings)
            .where(and_(Followings.following_id==user[1],Followings.follower_id==current_user.id))
        )
        data['isFollowing']=False if db.session.execute(isFollowing_query).scalar() is None else True
        
        return data,200
        

class ExportPosts(Resource):
    @auth_token_required
    def post(self):
        
        from blog_app_lite.async_jobs.tasks import csvGen
        email=current_user.email
        toExport=request.json['postIDs']
        csvGen.delay(toExport,email)
        return 200
        
        
class ImageDelivery(Resource):
    @auth_token_required
    def get(self):
        imageName=username=request.args.get('img')
        imageFile = open(app.config['POST_FOLDER'] + imageName, 'rb')
        return send_file(imageFile, mimetype='image/png')
        

class DailyPDF(Resource):
    @auth_token_required
    def get(self):
        dailyPDF.delay()
        return 200