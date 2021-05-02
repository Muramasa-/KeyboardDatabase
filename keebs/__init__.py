from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from keebs.forms import SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "ba6bc4cb438bf7c70b8a7acbea72a5e1"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)

from keebs import routes

db.create_all()