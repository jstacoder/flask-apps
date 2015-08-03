import os
from werkzeug import import_string,find_modules
from sqlalchemy import create_engine

class FlaskApps(object):
    '''
        object to perform our needs
    '''
    def __init__(self,app=None):
        '''
            just grab the app and initalize it if its there
        '''
        self.app = app
        if self.app is not None:
            self.init_app(self.app)

    def init_app(self,app):
        '''
            - load config from FLASK_APPS_CFG env var

            - run through installed_blueprints and import 
            
            - import modules within blueprints
        '''
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
        '''
            grab the db engine for use later, if we have the DATABASE_URI set
        '''
        if app.extensions['apps']['_has_models'] and app.config.get('DATABASE_URI'):
            app.extensions['apps']['_db_engine'] = create_engine(app.config['DATABASE_URI'],echo=True)
        else:
            app.extensions['apps']['_db_engine'] = None
        for bp in bps:
            app.register_blueprint(bp)
