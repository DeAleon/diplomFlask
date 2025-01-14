from config import db, login_manager
from flask_login import (LoginManager, UserMixin, login_required,
			  login_user, current_user, logout_user)
from werkzeug.security import generate_password_hash, check_password_hash


user_game = db.Table('user_game',
                     db.Column('users_id', db.Integer, db.ForeignKey('games.id')),
                     db.Column('games_id', db.Integer, db.ForeignKey('users.id'))
                     )

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, index=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), nullable=False, index=True, unique=True)
    email = db.Column(db.String(50), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)
    games = db.relationship('Game', secondary=user_game, backref='users')

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer(), primary_key=True, index=True)
    title = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False)
    age_limited = db.Column(db.Boolean(), nullable=False, default=False)
    cost = db.Column(db.Float())
    size = db.Column(db.Float())
    slug = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return "<{}:{}>".format(id, self.title)
