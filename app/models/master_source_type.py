from ..database.database import db

class MasterSourceType(db.Model):
    __tablename__ = "master_source_types"
    __table_args__ = {'extend_existing': True}

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255))
    code = db.Column('code', db.String(255))
    description = db.Column('description', db.Text)
    logo = db.Column('logo', db.String(255))
    url = db.Column('url', db.String(255))
