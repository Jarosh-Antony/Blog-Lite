from flask_restful import Resource,fields,marshal
from flask_security import current_user, auth_token_required
from flask import request, redirect, url_for,send_file
from datetime import datetime
import os
from flask import current_app as app
from blog_app_lite.DB import db
from sqlalchemy import func,and_
from blog_app_lite.models import User,Posts,Followings,MonthlyStat
from blog_app_lite.async_jobs.tasks import dailyPDF,monthlyReport
from blog_app_lite.cache import cache

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
        
        try:
            MS=MonthlyStat.query.filter_by(userID=user_id).first()
            MS.post_count+=1
        except:
            addUser=MonthlyStat(post_count=1,userID=user_id)
            db.session.add(addUser)
            
        db.session.commit()    
        
        return 200
    
    @auth_token_required
    @cache.cached(timeout=50)
    def get(self):
        username=request.args.get('username')
        posts_query=(
            db.select(Posts)
            .join(User,User.id==Posts.userID)
            .where(User.username==username)
            .order_by(Posts.created.desc())
        )
        posts=db.session.execute(posts_query).scalars().all()
        for post in posts:
            created=post.created
            created=created.split('.')[0]
            time=created
            if created.split(' ')[1] <'12:00:00':
                post.created=created+' AM'
            else :
                post.created=created+' PM'
        
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
        
        try:
            MS=MonthlyStat.query.filter_by(userID=user_id).first()
            MS.edit_count+=1
        except:
            addUser=MonthlyStat(edit_count=1,userID=user_id)
            db.session.add(addUser)
            
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
        
        try:
            MS=MonthlyStat.query.filter_by(userID=user_id).first()
            MS.delete_count+=1
        except:
            addUser=MonthlyStat(delete_count=1,userID=user_id)
            db.session.add(addUser)
            
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
        
        try:
            MS=MonthlyStat.query.filter_by(userID=following_id).first()
            MS.follow_count+=1
        except:
            addUser=MonthlyStat(follow_count=1,userID=following_id)
            db.session.add(addUser)
        
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
        
        try:
            MS=MonthlyStat.query.filter_by(userID=following_id).first()
            MS.unfollow_count+=1
        except:
            addUser=MonthlyStat(unfollow_count=1,userID=following_id)
            db.session.add(addUser)
        
        db.session.delete(follow)
        db.session.commit()
        
        return 200
        
class Feed(Resource):
    @auth_token_required
    def get(self):
        user=current_user
        
        cache_key='home_'+str(user.id)
        api_result=cache.get(cache_key)

        if api_result is None:
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
            
            api_result=marshal({'posts':posts},posts_rf)
            cache.set(cache_key,api_result,timeout=60)
            
        user.last_seen=str(datetime.now())
        db.session.commit()
            
        return api_result,200


class Search(Resource):
    @auth_token_required
    def get(self):
        search=request.args.get('search').split()
        search_results=[]
        
        s_r=User.query.all()
        usernames=[]
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
                        usernames.append(name_username['username'])
        
        user_ids = db.session.query(User.id).filter(User.username.in_(usernames)).all()
        user_ids = [id for (id,) in user_ids]
        
        for id in user_ids:
            try:
                MS=MonthlyStat.query.filter_by(userID=id).first()
                MS.search_count+=1
            except:
                addUser=MonthlyStat(search_count=1,userID=id)
                db.session.add(addUser)
        db.session.commit()
        
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
        
        try:
            MS=MonthlyStat.query.filter_by(userID=user[1]).first()
            MS.view_count+=1
        except:
            addUser=MonthlyStat(view_count=1,userID=user[1])
            db.session.add(addUser)
        db.session.commit()
        
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
        
class MonthlyReport(Resource):
    @auth_token_required
    def get(self):
        monthlyReport.delay()
        return 200