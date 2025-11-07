from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialisation de l'objet SQLAlchemy
db = SQLAlchemy()

# Modèle User minimal pour l'initialisation de la base de données
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

