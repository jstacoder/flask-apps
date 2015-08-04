from flask import views,make_response
from . import models,comment
from ..users.models import User
from ...base import dumps
            

def jsonify(*args,**kwargs):
    r = []
    r.extend(args)
    r.append(kwargs)

    res = make_response(dumps(r))
    res.headers['Content-Type'] = 'application/json'
    return res

class CommentView(views.MethodView):
    def get(self,user_id=None):
        if user_id:
            return jsonify(result=dict(user=User.get(user_id).name,comments=[x._to_json() for x in User.get(user_id).comments]))
        else:
            return jsonify(result=dict(comments=[x._to_json() for x in models.Comment.get_all()]))
            
comment.add_url_rule('/','index_by_id',view_func=CommentView.as_view('cmt_by_idx'))
comment.add_url_rule('/<user_id>','index_by_user',view_func=CommentView.as_view('cmt_by_user'))
