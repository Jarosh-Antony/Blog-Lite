from flask_restful import Api
from resources import Post

api=Api()
api.add_resource(Post,"/post")