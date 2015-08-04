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


