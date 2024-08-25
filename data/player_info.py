#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
@AUTHER:   hailiyang
@DATE:     2024/8/23 22:15
@FILENAME: player_info
"""

import json

# 读取玩家数据
def load_players():
    with open('players.json', 'r') as file:
        return json.load(file)['players']

players = load_players()
print(type(players[0]))