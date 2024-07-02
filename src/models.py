from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

#Model for table User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #Salt has been included to add an extra layer of security
    salt = db.Column(db.String(128), unique=False, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created": self.created_at,
        }