from flask import Flask, render_template, request, redirect, url_for, session
from data.player_info import players

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample data


# Index route
@app.route('/')
def index():
    return render_template('index.html', players=players)

# Player details and update route
@app.route('/player/<int:player_id>', methods=['GET', 'POST'])
def player(player_id):
    player = next((p for p in players if p['id'] == player_id), None)
    if player is None:
        return "Player not found", 404

    if request.method == 'POST':
        if 'user_id' in session and session['user_id'] == player_id:
            player['skills']['defense'] = int(request.form['defense'])
            player['skills']['offense'] = int(request.form['offense'])
            player['skills']['shooting'] = int(request.form['shooting'])
            player['skills']['speed'] = int(request.form['speed'])
            player['skills']['stamina'] = int(request.form['stamina'])
            player['skills']['charisma'] = int(request.form['charisma'])
            player['position'] = request.form['position']
            return redirect(url_for('index'))
        else:
            return "You can only edit your own profile", 403

    return render_template('playershow.html', player=player)

# Login route
@app.route('/login/<int:player_id>')
def login(player_id):
    session['user_id'] = player_id
    return redirect(url_for('index'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
