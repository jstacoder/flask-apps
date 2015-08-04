from flask import views,jsonify
from . import models,user
            
class UserView(views.MethodView):
    def get(self,id=None):
        if id is None:
            return jsonify(result=[x.name for x in models.User.get_all()])
        return jsonify(result=models.User.get(id).name)
            
user.add_url_rule('/','index',view_func=UserView.as_view('index'))
user.add_url_rule('/<id>','user_list',view_func=UserView.as_view('list'))
