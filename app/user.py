#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
@AUTHER:   hailiyang
@DATE:     2024/8/28 16:26
@FILENAME: user
"""
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id_, username):
        self.id = id_
        self.username = username

    def get_id(self):
        return self.id