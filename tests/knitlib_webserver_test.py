__author__ = 'tian'

import urllib2
from flask import Flask
from flask.ext.testing import LiveServerTestCase
from knitlib_webserver import app


class MyTest(LiveServerTestCase):
    def create_app(self):
        # app = Flask(__name__)
        app.config['TESTING'] = True
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 8943
        return app

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)
