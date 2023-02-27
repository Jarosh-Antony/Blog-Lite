from flask_restful import Resource
from flask_security import current_user, auth_token_required


class Post(Resource):
    @auth_token_required
    def post(self):
        user=current_user
        
        return 201

