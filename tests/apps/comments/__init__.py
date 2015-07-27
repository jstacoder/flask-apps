from flask import Blueprint,views

comments = Blueprint(__name__,'comments',url_prefix='/comments',template_folder='templates/comments')

class IndexView(views.MethodView):
    def get(self):
        return "Comments index view"

comments.add_url_rule('/','index',view_func=IndexView.as_view('comments_index'))




