from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO, join_room, leave_room
from flask_cors import CORS


f_app = Flask(__name__)
bootstrap = Bootstrap(f_app)
csrf = CSRFProtect(f_app)
f_app.static_folder = "static"
f_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///idedraw.db'
f_app.config['SECRET_KEY'] = '6de784b2628875dbae3a7a42'
f_app.config['CORS_HEADERS'] = 'Content-Type'
db = SQLAlchemy(f_app)
socketio = SocketIO(f_app, cors_allowed_origins="*")
cors = CORS(f_app,resources={r"/*":{"origins":"*"}})


from app import routes
from app import models