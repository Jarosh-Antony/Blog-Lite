from blog_app_lite.workers import celery as app
from blog_app_lite.DB import db
from blog_app_lite.models import User,Posts,Followings
from sqlalchemy import func,and_
import csv
from datetime import datetime
import zipfile
from blog_app_lite import email_sender as es
from jinja2 import Template
from flask import current_app
import os

@app.task()
def csvGen(toExport,email):
    
    posts_query=(
        db.select(Posts)
        .join(User,User.id==Posts.userID)
        .where(and_(User.email==email),(Posts.id.in_(toExport)))
        .order_by(Posts.created.desc())
    )
    posts=db.session.execute(posts_query).scalars()
    
    time=datetime.now()
    t=time.strftime('%Y-%m-%d-%H-%M-%S-%f')
    output='exports/'+email+t
    csv_filename=output+'.csv'
    images=[]
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'title', 'description', 'imageName', 'created', 'modified', 'userID'])
        for post in posts:
            if not post.imageName==None:
                images.append(post.imageName)
            writer.writerow([post.id, post.title, post.description, post.imageName, post.created, post.modified, post.userID])
            
    
    zip_filename = output+'.zip'
    zip_file = zipfile.ZipFile(zip_filename, 'w')
    zip_file.write(csv_filename,arcname=email+t+'.csv')
    
    for i in images:
        with open(current_app.config['POST_FOLDER'] + i, 'rb') as f:
            zip_file.write(f.name, arcname=i)
    zip_file.close()
    
    with open('blog_app_lite/templates/email_message.html') as file_:
        template=Template(file_.read())
        message=template.render()
    es.send_email(email,'Exported Posts/blogs',message,zip_filename)
    
    os.remove(csv_filename)
    os.remove(zip_filename)
    return toExport


@app.task()
def dailyPDF():
    users=User.query.all()
    
    for user in users:
        posts_query=(
            db.select(Posts,User.username,User.name)
            .join(Followings,Followings.following_id==Posts.userID)
            .join(User,User.id==Posts.userID)
            .where(and_(Followings.follower_id==user.id,Posts.modified>=user.last_seen))
            .order_by(Posts.created.desc())
        )
        result=db.session.execute(posts_query)
        
        posts={}
        for post,username,name in result:
            if username not in posts:
                posts[username]={}
            
            if post.created>=user.last_seen:
                if 'created' not in posts[username]:
                    posts[username]['created']=0
                posts[username]['created']+=1
                
            else :
                if 'modified' not in posts[username]:
                    posts[username]['modified']=0
                posts[username]['modified']+=1
        
        time=str(datetime.now()).split()[0]
        posted_query=(
            db.select(func.count())
            .select_from(Posts)
            .where(Posts.userID==user.id,Posts.created>=time)
        )
        posted=db.session.execute(posted_query).scalar()
        
        if len(posts)>0 or posted==0:
            
            with open('blog_app_lite/templates/dailyReport.html') as file_:
                template=Template(file_.read())
                message=template.render(posts=posts,posted=posted)
            es.send_email(user.email,'Daily Report',message)
    
    return True


