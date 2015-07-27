from flask_apps import FlaskApps
from flask_testing import TestCase
from flask import Flask,Blueprint
import sys
import os

sys.path.insert(0,os.path.realpath(os.path.dirname(__file__)))

class FlaskAppsTest(TestCase):
    def create_app(self):
        test_app = Flask(__name__)
        test_app.config['INSTALLED_BLUEPRINTS'] = [
                'tests.apps.users',
                'tests.apps.comments',
                'tests.apps.admin'
        ]
        flask_apps = FlaskApps(test_app)
        self.app = test_app
        self.client = test_app.test_client()
        return test_app

    def test_admin_bp(self):
        res = self.client.get('/admin/')
        self.assertIn('admin',res.get_data().lower())

    def test_comment_bp(self):
        res = self.client.get('/comments/')
        self.assertIn('comment',res.get_data().lower())

    def test_users_bp(self):
        res = self.client.get('/users/')
        self.assertIn('user',res.get_data().lower())

    def test_have_all_bps(self):
        self.assertEquals(len(self.app.blueprints),3)


