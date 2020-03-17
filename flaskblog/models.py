from datetime import datetime
from _init_ import , login_manager
from flask_login import UserMixin
from flask_socketio import SocketIO, emit, join_room
import sqlite3 as sql





class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return User(self.username, self.image_file)
    


