##flask-apps

this gives flask applications a setting similar to djangos `INSTALLED_APPS`,
called `INSTALLED_BLUEPRINTS`

- to use:
    - in your settings file add:
        ```
        INSTALLED_BLUEPRINTS = [
            'path.to.the.bp',
            'path.to.next.bp'
        ]
        ```

    - then when you create your app do
        ```
        from flask_apps import FlaskApps

        app = Flask(__name__)

        flask_apps = FlaskApps(app)
    
        ```

And thats it, from there FlaskApps will import and register all of the blueprints from the `INSTALLED_BLUEPRINTS` setting, as well as any modules inside the blueprints, ie: models, views, filters, anything
