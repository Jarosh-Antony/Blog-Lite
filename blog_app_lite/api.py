from flask_restful import Api
from blog_app_lite.resources import Post,Follow,Feed,Search

api=Api()
api.add_resource(Post,"/api/posts")
api.add_resource(Follow,"/api/follow")
api.add_resource(Feed,"/api/feeds")
api.add_resource(Search,"/api/search")