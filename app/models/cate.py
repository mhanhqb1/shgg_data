from ..database.database import db

class Cate(db.Model):
    __tablename__ = "cates"
    __table_args__ = {'extend_existing': True}

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255))
    slug = db.Column('slug', db.String(255))
    image = db.Column('image', db.String(255))
    icon = db.Column('icon', db.String(255))