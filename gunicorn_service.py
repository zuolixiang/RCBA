#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
@AUTHER:   hailiyang
@DATE:     2024/10/17 16:55
@FILENAME: gunicorn_service
"""


from flask import Flask
from blueprints.player_bp import rcbaplayer
import gunicorn.app.base
import multiprocessing

app = Flask(__name__)
app.secret_key = "fbdsijfdlshgk3827r9"

app.register_blueprint(rcbaplayer)

class GunicornApp(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options
        super().__init__()

    def load(self):
        return self.application

    def load_config(self):
        config = {
            key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)


def number_of_workers():
    return multiprocessing.cpu_count() + 1


if __name__ == '__main__':
    options = {
        'workers': number_of_workers()
    }
    GunicornApp(app, options).run()