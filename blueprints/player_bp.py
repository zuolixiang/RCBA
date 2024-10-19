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
match_json = current_file_path + '/../data/match_statistics.json'

players = load_json_data(players_json, 'players')
teams = load_json_data(teams_json, 'teams')
comp_teams_2024 = load_json_data(teams_json, 'comp_teams_2024')
# matches = load_json_data(match_json, 'years')


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


# 数据页
@rcbaplayer.route('/data', methods=['GET', 'POST'])
def data():
    pass


@rcbaplayer.route('/data/add', methods=['GET'])
def add_data():
    # 检查用户是否已登录且是否为管理员
    if session['username'] not in ('hailiyang', '陆智卿'):
        return render_template('error.html')
    return render_template('enter_info.html')


# 录入比赛基本信息页
@rcbaplayer.route('/data/entercompdata')
def enter_comp_info():
    return render_template('enter_comp_info.html')


# 保存比赛基本信息的路由
@rcbaplayer.route('/save_match', methods=['POST'])
def save_match():
    match_data = request.get_json()
    print(match_data)

    # 检查是否存在 json 文件，如果不存在则创建
    if not os.path.exists(match_json):
        with open(match_json, 'w') as f:
            json.dump([], f)

    match_year = match_data['match_year']
    match_id = match_data['match_id']
    match_date = match_data['match_date']
    home_team = match_data['home_team']
    guest_team = match_data['guest_team']
    print(match_year, match_id, match_date, home_team, guest_team)

    matches = {}
    with open(match_json, 'r') as f:
        matches = json.load(f)

    # 如果该年份不存在，创建新的年份条目
    if match_year not in matches:
        matches[match_year] = {"matches": []}

    match_id_list = []
    if matches[match_year]['matches']:
        match_id_list = [x['match_id'] for x in matches[match_year]['matches']]

    # 如果该场比赛不存在，创建新的比赛条目
    if match_id not in match_id_list:
        match = {
            'match_id': match_id,
            'match_info': {
                "match_date": match_date,
                "home_team": home_team,
                "guest_team": guest_team,
                "players": []  # 初始化players为空
            }
        }
        matches[match_year]['matches'].append(match)
    else:
        print(f"比赛 {match_id} 已经存在于 {match_year} 年，无法重复初始化。")

    # 将更新后的数据写回 comp.json
    with open(match_json, 'w') as f:
        json.dump(matches, f, ensure_ascii=False, indent=4)

    return jsonify({"success": True})


# 获取比赛统计数据
@rcbaplayer.route('/data/matches')
def get_matches():
    with open(match_json, 'r') as file:
        matches = json.load(file)
        return matches


# 录入球员比赛信息数据
@rcbaplayer.route('/data/enterplayerdata')
def enter_player_info():
    return render_template('enter_player_info.html')


# 保存球员比赛信息数据
@rcbaplayer.route('/update_player_data', methods=['POST'])
def update_player_data():
    data = request.get_json()  # 获取前端提交的数据
    year = data.get('year')  # 获取年份
    match_id = data.get('match_id')  # 获取比赛的 match_id
    player_data = data.get('player_data')  # 获取球员数据
    player_team = player_data.get('team')
    player_name = player_data.get('name')

    # 加载现有比赛数据
    matches = get_matches()

    # 检查数据是否正确
    if year in matches and 'matches' in matches[year]:
        # 找到对应的比赛
        match_list = matches[year]['matches']
        match_found = False

        print(match_list)
        for match in match_list:
            print(match['match_id'], match_id)
            if match['match_id'] == match_id:
                # 找到对应比赛，确保 match_info 和 players 字段存在
                if 'match_info' in match and 'players' in match['match_info']:
                    players = match['match_info']['players']
                    player_exists = False

                    # 遍历现有的球员列表，检查该球员是否已经存在
                    for existing_player in players:
                        if existing_player['name'] == player_name and existing_player['team'] == player_team:
                            # 如果球员存在，更新其数据
                            existing_player.update(player_data)
                            player_exists = True
                            break

                    # 如果球员不存在，添加新球员数据
                    if not player_exists:
                        players.append(player_data)

                    match_found = True
                    break

        if match_found:
            # 保存更新后的比赛数据到 JSON 文件
            with open(match_json, 'w') as f:
                json.dump(matches, f, ensure_ascii=False, indent=4)
            return jsonify({"success": True, "message": "球员数据已保存"})
        else:
            return jsonify({"success": False, "message": "未找到该比赛场次"}), 400
    else:
        return jsonify({"success": False, "message": "未找到该年份的比赛"}), 400


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
        elif username not in ('hailiyang', '陆智卿') and role == 'admin':
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
