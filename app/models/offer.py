from ..database.database import db

class Offer(db.Model):
    __tablename__ = "offers"
    __table_args__ = {'extend_existing': True}

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255))
    detail = db.Column('detail', db.Text)
    start_date = db.Column('start_date', db.Date)
    end_date = db.Column('end_date', db.Date)
    image = db.Column('image', db.String(255))
    url = db.Column('url', db.String(255))
    source_type_code = db.Column('source_type_code', db.String(45))
    source_id = db.Column('source_id', db.String(255))