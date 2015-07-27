from flask import Blueprint,views

users = Blueprint(__name__,'users',url_prefix='/users',template_folder='templates/users')

class IndexView(views.MethodView):
    def get(self):
        return "Users index view"

users.add_url_rule('/','index',view_func=IndexView.as_view('users_index'))




