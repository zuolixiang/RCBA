#!/bin/bash

# 启动 Gunicorn 服务
watchmedo auto-restart --directory=./ --pattern="*.py;*.html;*.js;*.css" --recursive -- python3 app.py