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

Here's 2 ~~small~~, trivial examples. To give you a better idea. One without flask-apps, and one using flask-apps.
Both will use the same file structure, the only differernce will be in the amount of code needed in each file.

File Structure:
```
    -   app/
        -   __init__.py
        -   base.py
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
```
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
        `app/base.py`
        ```python
        from sqlalchemy.ext.declarative import declared_attr,declarative_base
        from inflection import pluralize, underscore
        import sqlalchemy as sa
        import os
        
        class classproperty(object):
            def __init__(self,getter):
                self.getter = getter
                
            def __get__(self,instance,owner):
                return self.getter(owner)
                
        class BaseModel(declarative_base()):
            _session = None
            _engine = None
            _query = None
            
            def save(self):
                self.session.add(self)
                self.session.commit()
                return self
            
            def delete(self):
                self.session.delete(self)
                
            @classmethod
            def get_all(cls):
                return cls.query.all()
                
            @classmethod
            def get(cls,id):
                return cls.query.get(id)
                
            @classproperty
            def query(cls):
                if cls._query is None:
                    cls._query = cls.session.query(cls)
                return cls._query
                
            @classproperty
            def session(cls):
                if cls._session is None:
                    cls._session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=cls.engine))
                return cls._session
        
            @classproperty
            def engine(cls):
                if cls._engine is None:
                    cls._engine = sa.create_engine(os.environ.get('DATABASE_URI','sqlite:///test.db'))
                return cls._engine
            
            @declared_attr
            def id(self):
                return sa.Column(sa.Integer,primary_key=True)
                
            @declared_attr
            def __tablename__(self):
                return underscore(pluralize(self.__name__))
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
            from ...base import BaseModel,sa
            
            
            class User(BaseModel):
                name = sa.Column(sa.String(255))
                
        ```
        `app/apps/users/views.py`
        ```python
            from flask import views,jsonify
            from . import models,user
            
            class UserView(views.MethodView):
                def get(self,id=None):
                    if id is None:
                        return jsonify(result=[x.name for x in models.User.get_all()])
                    return jsonify(result=models.User.get(id).name)
            
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
            from ...base import BaseModel,sa
            
            class Comment(BaseModel):
                text = sa.Column(sa.Text)
                user_id = sa.Column(sa.Integer,sa.ForeignKey('users.id'))
                user = sa.orm.relation('User',uselist=False)
        ```
        `app/apps/comments/views.py`
        ```python
            from flask import views,jsonify
            from . import models,comment
            from ..users.models impoer User
            
            class CommentView(views.MethodView):
                def get(self,id=None,user_id=None):
                    if id is None and user_id is None:
                        return False
                    if user_id:
                        return jsonify(result=[x.text for x in User.get(user_id).comments])
                    else:
                        return jsonify(result=[x.text for x in models.Comment.get_all()])
            
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
