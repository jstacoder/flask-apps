from flask import Blueprint,views

admin = Blueprint(__name__,'admin',url_prefix='/admin',template_folder='templates/admin')

class IndexView(views.MethodView):
    def get(self):
        return "Admin Index View"

admin.add_url_rule('/','index',view_func=IndexView.as_view('index'))
