from flask_restful import Api
from blog_app_lite.resources import Post,Follow,Feed,Search,Statistics,ExportPosts,ImageDelivery

api=Api()
api.add_resource(Post,"/api/posts")
api.add_resource(Follow,"/api/follow")
api.add_resource(Feed,"/api/feeds")
api.add_resource(Search,"/api/search")
api.add_resource(Statistics,"/api/statistics")
api.add_resource(ExportPosts,"/api/export")
api.add_resource(ImageDelivery,"/api/img")