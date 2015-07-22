from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class Move(db.Model):
    __tablename__ = 'moves'
    id = db.Column(db.Integer, primary_key=True)
    source_position_id = db.Column(db.Integer, index=True)
    destination_position_id = db.Column(db.Integer)
    quality_id = db.Column(db.Integer, db.ForeignKey('quality.id'))
    san = db.Column(db.String(8))


class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True)
    fen = db.Column(db.String(88), unique=True, index=True)


class Quality(db.Model):
    __tablename__ = 'quality'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(7))
    moves = db.relationship('Move', backref='quality', lazy='dynamic')

    def __repr__(self):
        return '<Quality %r>' % self.name
