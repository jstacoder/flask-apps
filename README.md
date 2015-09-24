[![Build Status](https://travis-ci.org/jstacoder/flask-apps.svg?branch=master)](https://travis-ci.org/jstacoder/flask-apps)
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
