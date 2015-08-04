import os
from app import app
from app.apps import comments,users
from flask_script import Manager,commands
from faker import Factory

User = users.models.User
Comment = comments.models.Comment

User.engine.echo = True
User.metadata.bind = User.engine

factory = Factory()
faker = factory.create()


manager = Manager(app)
manager.add_command('urls',commands.ShowUrls())

def make_user(name):
    user = User()
    user.name = name
    return user.save()

def make_cmt(txt,uid):
    cmt = Comment()
    cmt.text = txt
    cmt.user_id = uid
    return cmt.save()

@manager.command
def seed_db():
    User.metadata.create_all()
    for name in ['kyle','joe','jill','fred']:
        user = make_user(name)
        for x in range(15):
            cmt = make_cmt(faker.text(),user.id)

if __name__ == "__main__":
    manager.run()

