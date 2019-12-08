from ..database.database import db

class MasterCate(db.Model):
    __tablename__ = "master_cates"
    __table_args__ = {'extend_existing': True}

    id = db.Column('id', db.Integer, primary_key=True)
    cate_id = db.Column('cate_id', db.Integer)
    cate_url = db.Column('cate_url', db.String(255))
    cate_name = db.Column('cate_name', db.String(255))
    source_type_code = db.Column('source_type_code', db.String(45))
    updated = db.Column('updated', db.Integer)
    page = db.Column('page', db.Integer)

    def __init__(self, cate_id, cate_url, cate_name, source_type_code, updated, page = 0):
        self.cate_id = cate_id
        self.cate_url = cate_url
        self.cate_name = cate_name
        self.source_type_code = source_type_code
        self.updated = updated
        self.page = page