from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Declaring model
class DataTable(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String, index = True, unique = True)
    value = db.Column(db.String)
