from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

database = Blueprint('manager', __name__)

# Make main db
db = SQLAlchemy()