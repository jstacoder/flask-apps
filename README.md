##flask-apps

this gives flask applications a setting similar to djangos `INSTALLED_APPS`,
called `INSTALLED_BLUEPRINTS`

- to use:
    - first install:
        
        - pip install flask-apps

    - in your settings file add:
        ```python
        INSTALLED_BLUEPRINTS = [
            'path.to.the.bp',
            'path.to.next.bp'
        ]
        ```

    - then when you create your app do
        ```python
        from flask_apps import FlaskApps

        app = Flask(__name__)

        flask_apps = FlaskApps(app)
    
        ```

    - or use the factory pattern
        ```python
        flask_apps = FlaskApps()
        ```

    - then later
        ```python
        flask_apps.init_app(app)
        ```

And thats it, from there FlaskApps will import and register all of the blueprints from the `INSTALLED_BLUEPRINTS` setting, as well as any modules inside the blueprints, ie: models, views, filters, anything

Here's 2 small, trivial examples. To give you a better idea. One without flask-apps, and one using flask-apps.
Both will use the same file structure, the only differernce will be in the amount of code needed in each file.

File Structure:
    -   app/
        -   __init__.py
        -   apps/
            -   users/
                - models.py
                - views.py
                - __init__.py
            -   comments/
                - models.py
                - views.py
                - __init__.py
            -   admin/
                - models.py
                - views.py
                - __init__.py
- Example1
    - No flask-apps
        `app/__init__.py`
        ```python
            from flask import Flask
            from .apps.users import user
            from .apps.comments import comment
            from .apps.admin import admin
            
            app = Flask(__name__)
            app.register_blueprint(user)
            app.register_blueprint(comment)
            app.register_blueprint(admin)
            
            if __name__ == "__main__":
                app.run()
        ```
        `app/apps/users/__init__.py`
        ```python
            from flask import Blueprint
            
            user = Blueprint(__name__,'user')
            
            from .views import *
            from .models import *
        ```
        `app/apps/users/models.py`
        ```python
            class User(object):
                _count = 0
                _lst = []
                def __init__(self,name):
                    self.id = User._count = User._count  + 1
                    self.name = name
                    User._lst.append(self)
        ```
        `app/apps/users/views.py`
        ```python
            from flask import views
            from . import models,user
            
            class UserView(views.MethodView):
                def get(self,id=None):
                    if id is None:
                        return models.User._userlst
                    return filter(lambda x: x.id == id,models.User._userlst)
            
            user.add_url_rule('/','index',view_func=UserView.as_view('index'))
            user.add_url_rule('/<id>','user_list',view_func=UserView.as_view('list'))
        ```
        `app/apps/comments/__init__.py`
        ```python
            from flask import Blueprint
            
            comment = Blueprint(__name__,'comment')
            
            from .views import *
            from .models import *
        ```
        `app/apps/comments/models.py`
        ```python
            class Comment(object):
                _count = 0
                _lst = []
                def __init__(self,text,user_id):
                    self.id = Comment._count = Comment._count  + 1
                    self.text = text
                    self.user_id = user_id
                    Comment._lst.append(self)
        ```
        `app/apps/comments/views.py`
        ```python
            from flask import views
            from . import models,comment
            
            class CommentView(views.MethodView):
                def get(self,id=None,user_id=None):
                    if id is None and user_id is None:
                        return False
                    if user_id:
                        return filter(lambda x: x.user_id == user_id,Comment._commentlst)
                    else:
                        return filter(lambda x: x.id == id,Comment._commentlst)
            
            comment.add_url_rule('/<user_id>','index_by_user',view_func=CommentView.as_view('cmt_by_user'))
            comment.add_url_rule('/<id>','index_by_id',view_func=CommentView.as_view('cmt_by_idx'))
        ```
        `app/apps/admin/__init__.py`
        ```python
            from flask import Blueprint
            
            admin = Blueprint(__name__,'admin')
            
            from .views import *
            from .models import *
        ```
        `app/apps/admin/models.py`
        ```python
            class Admin(object):
                _adminItemcount = 0
                _Itemlst = []
                def __init__(self,itmClass):
                    self.id = Admin._adminItemcount = Admin._adminItemcount + 1
                    self.name = itmClas.__name__
                    self._itmLst = itmClass._lst
                    self._count = itmClass._count
        ```
        `app/apps/admin/views.py`
        ```python
            from flask import views
            from ..users import user
            from ..comments import comment
            from . import models,admin
            
            
            
            class AdminView(views.MethodView):
                models = dict(
                    user=user,
                    comment=comment
                )
            
                def get(self,admin_name):
                    return self.models[admin_name]._itmLst
                    
            
            admin.add_url_rule('/<admin_name>','index',view_func=AdminView.as_view('index'))
        ```
