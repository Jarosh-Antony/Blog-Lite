from flask_restful import Api
from blog_app_lite.resources import Post,Follow,Feed

api=Api()
api.add_resource(Post,"/posts")
api.add_resource(Follow,"/follow")
api.add_resource(Feed,"/feeds")