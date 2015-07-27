import os
from werkzeug import import_string,find_modules
from sqlalchemy import create_engine

class FlaskApps(object):
    def __init__(self,app=None):
        self.app = app
        if self.app is not None:
            self.init_app(self.app)

    def init_app(self,app):
        blueprints = []
        app.extensions = app.extensions or {}
        app.extensions['apps'] = {}
        app.extensions['apps']['_has_models'] =  False
        if 'FLASK_APPS_CFG' in os.environ:
            app.config.from_envvar('FLASK_APPS_CFG')

        if app.config.get('DATABASE_URI'):
            os.environ['DATABASE_URI'] = app.config.get('DATABASE_URI')
        if 'INSTALLED_BLUEPRINTS' in app.config:
            blueprints = app.config['INSTALLED_BLUEPRINTS']
            bps = []
            for b in blueprints:
                module = import_string(b)
                children = list(find_modules(b))
                bp = getattr(module,b.rsplit('.',1)[-1])
                bps.append(bp)
                for child in children:
                    if child.endswith('models'):
                        app.extensions['apps']['_has_models'] =  True
                    import_string(child)
        if app.extensions['apps']['_has_models']:
            app.extensions['apps']['_db_engine'] = create_engine(app.config['DATABASE_URI'],echo=True)
        else:
            app.extensions['apps']['_db_engine'] = None
        for bp in bps:
            app.register_blueprint(bp)
        




