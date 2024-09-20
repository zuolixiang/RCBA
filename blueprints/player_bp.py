#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
@AUTHER:   hailiyang
@DATE:     2024/8/23 16:40
@FILENAME: player_bp
"""

from flask import render_template, request, redirect, url_for, session, Blueprint, jsonify
import json
import os

# 注册蓝图
rcbaplayer = Blueprint('rcbaplayer', __name__, template_folder='templates')


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

players = load_json_data(players_json, 'players')
teams = load_json_data(teams_json, 'teams')
comp_teams_2024 = load_json_data(teams_json, 'comp_teams_2024')

# 首页
@rcbaplayer.route('/')
def index():
    return render_template('index.html')


@rcbaplayer.route('/schedule/<int:year>')
def schedule(year):
    # 处理该年份赛程的逻辑
    return render_template('schedule.html', year=year)


@rcbaplayer.route('/comp_team/<captain>')
def comp_team_detail(captain):
    # 根据队长名获取球队信息
    team = next((team for team in comp_teams_2024 if team['captain'] == captain), None)
    team_players = [player for player in players if player['comp_team'] == team['comp_team']]

    return render_template('comp_team_detail.html', team=team, players=team_players)


# 球队页
@rcbaplayer.route('/team')
def team():
    for team in teams:
        team_players = [player for player in players if player['team_name'] == team['team_name']]
        team['player_count'] = len(team_players)
    return render_template('teams.html', teams=teams)


@rcbaplayer.route('/team/<team_name>')
def team_detail(team_name):
    # 过滤出该球队的球员
    team_players = [player for player in players if player['team_name'] == team_name]
    contont = {
        "team_name": team_name,
        "players": team_players,
        "team_count": len(team_players)
    }
    return render_template('team_detail.html', **contont)


# 球星页
@rcbaplayer.route('/player')
def player():
    # if 'username' not in session:
    #     return redirect(url_for('rcbaplayer.login'))
    page = request.args.get('page', 1, type=int)
    per_page = 8
    total_players = len(players)
    paginated_players = players[(page - 1) * per_page: page * per_page]
    context = {
        "players": paginated_players,
        "total_players": total_players,
        "per_page": per_page,
        "page": page,
    }

    # return render_template('players.html', players=paginated_players, page=page, per_page=per_page, total_players=total_players)
    return render_template('players.html', **context)


# 球星detail页
@rcbaplayer.route('/player/<int:player_id>', methods=['GET', 'POST'])
def player_show(player_id):
    player = next((p for p in players if p['id'] == player_id), None)
    if player is None:
        return "Player not found", 404

    if request.method == 'POST':
        if session.get('is_admin', False) or session['username'] == player['name']:
            print(request.form)
            try:
                position = request.form['position']
                # pos_neg = request.form['pos_neg']
                defense = int(request.form.get('defense', 0))
                offense = int(request.form.get('offense', 0))
                shooting = int(request.form.get('shooting', 0))
                speed = int(request.form.get('speed', 0))
                stamina = int(request.form.get('stamina', 0))
                charisma = int(request.form.get('charisma', 0))

                # 验证数值是否在 0 到 100 之间
                if not all(0 <= value <= 100 for value in [defense, offense, shooting, speed, stamina, charisma]):
                    return "Values must be between 0 and 100", 400
                player['position'] = position
                # player['pos_neg'] = pos_neg
                player['skills'] = {
                    "defense": defense,
                    "offense": offense,
                    "shooting": shooting,
                    "speed": speed,
                    "stamina": stamina,
                    "charisma": charisma
                }
                save_players(players)
            except ValueError:
                return "Invalid input", 400

            return redirect(url_for('rcbaplayer.index'))
        else:
            return "对不起，你只能修改自己的信息！", 403

    return render_template('playershow.html', player=player)


# 球星对比页
@rcbaplayer.route('/compare')
def compare_players():
    if 'username' not in session:
        return redirect(url_for('rcbaplayer.login'))
    return render_template('compare.html', players=players)


@rcbaplayer.route('/compare/<int:player1_id>/<int:player2_id>')
def get_comparison_data(player1_id, player2_id):
    player1 = next((player for player in players if player['id'] == player1_id), None)
    player2 = next((player for player in players if player['id'] == player2_id), None)

    if player1 and player2:
        data = {
            'player1': {
                'name': player1['name'],
                'stats': [player1['skills']['defense'], player1['skills']['offense'], player1['skills']['shooting'],
                          player1['skills']['speed'], player1['skills']['stamina'], player1['skills']['charisma']]
            },
            'player2': {
                'name': player2['name'],
                'stats': [player2['skills']['defense'], player2['skills']['offense'], player2['skills']['shooting'],
                          player2['skills']['speed'], player2['skills']['stamina'], player2['skills']['charisma']]
            }
        }
        return jsonify(data)
    else:
        return jsonify({'error': 'Player not found'}), 404


# 登录页
@rcbaplayer.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form['username']
        role = request.form['role']  # 'admin' or 'user'

        # Logic for role enforcement
        if username in ('hailiyang', '陆智卿') and role != 'admin':
            return f" {username} must be an admin! 403"
        elif username not in ('hailiyang', '陆智卿')  and role == 'admin':
            return "对不起，您不是管理员，请用自己姓名作为用户名，选择普通用户登录!", 403


        # 设置 session 信息
        session['username'] = username
        session['is_admin'] = (role == 'admin')

        return redirect(url_for('rcbaplayer.index'))

    return render_template('login.html')


@rcbaplayer.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    return redirect(url_for('rcbaplayer.login'))
