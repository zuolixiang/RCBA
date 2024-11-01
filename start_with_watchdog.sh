#!/bin/bash

# 启动 Gunicorn 服务
#watchmedo auto-restart --directory=./ --pattern="*.py;*.html;*.js;*.css" --recursive -- python3 app.py
gunicorn -w 4 -k gthread -b 127.0.0.1:5001 --threads 2 gunicorn_service:app
