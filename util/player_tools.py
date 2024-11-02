#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
@AUTHER:   hailiyang
@DATE:     2024/11/2 10:18
@FILENAME: player_tools
"""

import os
import json


current_file_path = os.path.dirname(os.path.abspath(__file__))

# 读取球员数据
def load_json_data(filename, key):
    with open(filename, 'r') as file:
        return json.load(file)[key]


# 保存球员数据
def save_players(players):
    with open(current_file_path + '/../data/players.json', 'w', encoding='utf8') as file:
        json.dump({"players": players}, file, indent=4, ensure_ascii=False)


players_json = current_file_path + '/../data/players.json'
teams_json = current_file_path + '/../data/teams.json'
match_json = current_file_path + '/../data/match_statistics.json'

players = load_json_data(players_json, 'players')
teams = load_json_data(teams_json, 'teams')
comp_teams_2024 = load_json_data(teams_json, 'comp_teams_2024')
# matches = load_json_data(match_json, 'years')


# 获取比赛数据
def get_matches():
    with open(match_json, 'r') as file:
        matches = json.load(file)
        return matches


# 获取比赛轮次
def get_match_rounds_by_date(match_year):
    data = get_matches()
    match_rounds = []
    if match_year in data:
        for match in data[match_year]['matches']:
            match_rounds.append(match['match_id'])
    return match_rounds


# 根据分数值排序，并加上序号
def sort_list(init_dict):
    if not init_dict:
        return []
    ordered_list = sorted([{'name': key, 'score': init_dict[key]} for key in init_dict.keys()],
                        key=lambda x: x['score'], reverse=True)
    for i, item in enumerate(ordered_list):
        item['index'] = i+1

    return ordered_list