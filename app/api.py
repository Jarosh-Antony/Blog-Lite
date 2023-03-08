from flask_restful import Api
from resources import Post,Follow

api=Api()
api.add_resource(Post,"/post")
api.add_resource(Follow,"/follow")