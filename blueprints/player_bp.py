#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
@AUTHER:   hailiyang
@DATE:     2024/8/23 16:40
@FILENAME: player_bp
"""

from flask import render_template, request, redirect, url_for, session, Blueprint
import json
import os

# 注册蓝图
rcbaplayer = Blueprint('rcbaplayer', __name__, template_folder='templates')


current_file_path = os.path.dirname(os.path.abspath(__file__))
# 读取球员数据
def load_players():
    with open(current_file_path + '/../data/players.json', 'r') as file:
        return json.load(file)['players']

# 保存球员数据
def save_players(players):
    with open(current_file_path + '/../data/players.json', 'w', encoding='utf8') as file:
        json.dump({"players": players}, file, indent=4, ensure_ascii=False)

players = load_players()

@rcbaplayer.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('rcbaplayer.login'))
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

    # return render_template('index.html', players=paginated_players, page=page, per_page=per_page, total_players=total_players)
    return render_template('index.html', **context)

# Player details and update route
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
                pos_neg = request.form['pos_neg']
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
                player['pos_neg'] = pos_neg
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


@rcbaplayer.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form['username']
        role = request.form['role']  # 'admin' or 'user'

        # Logic for role enforcement
        if username == 'hailiyang' and role != 'admin':
            return "hailiyang must be an admin!", 403
        elif username != 'hailiyang' and role == 'admin':
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
