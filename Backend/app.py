from flask import Flask
from config import Config
from database import db
from auth import auth_bp
from routes.user import user_bp
from routes.feedback import feedback_bp
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(feedback_bp, url_prefix='/feedback')

if __name__ == '__main__':
    app.run(host='0.0.0.0')