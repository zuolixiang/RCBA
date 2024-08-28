from flask import Flask
from blueprints.player_bp import rcbaplayer

app = Flask(__name__)
app.secret_key = "fbdsijfdlshgk3827r9"

app.register_blueprint(rcbaplayer)


if __name__ == '__main__':
    app.run(debug=True)
