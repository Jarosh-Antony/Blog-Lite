from flask_restful import Resource
from flask_security import current_user, auth_token_required
from flask import request, redirect, url_for
from datetime import datetime
import os
from __main__ import app,db
from models import Posts

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
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],image_name))
            imageurl = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
            print(imageurl)
        else :
            imageurl=None
            
        newPost=Posts(title=title,description=desc,imageurl=imageurl,timestamp=str(time),userID=user_id)
        db.session.add(newPost)
        db.session.commit()    
        
        return 201

