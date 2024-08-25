from flask import Flask
from blueprints.player_bp import rcbaplayer
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.secret_key = "fbdsijfdlshgk3827r9"
app.register_blueprint(rcbaplayer)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
