from ..database.database import db

class Product(db.Model):
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(255))
    name_search = db.Column('name_search', db.String(255))
    price = db.Column('price', db.String(30))
    sale_price = db.Column('sale_price', db.Float)
    history_price = db.Column('history_price', db.Text)
    history_price_ts = db.Column('history_price_ts', db.Text)
    cate_id = db.Column('cate_id', db.Integer)
    source_id = db.Column('source_id', db.String(45))
    source_url = db.Column('source_url', db.String(255))
    source_type_code = db.Column('source_type_code', db.String(45))
    source_cate_id = db.Column('source_cate_id', db.Integer)
    source_cate_name = db.Column('source_cate_name', db.String(255))
    # created = db.Column('created', db.Integer)
    # updated = db.Column('updated', db.Integer)
    image = db.Column('image', db.String(255))
    thumb_images = db.Column('thumb_images', db.Text)
    shop_id = db.Column('shop_id', db.String(255))

    def __init__(self, name, name_search, price, sale_price, history_price, image, thumb_images, shop_id, source_id, source_type_code, source_url=None):
        self.name = name
        self.name_search = name_search
        self.price = price
        self.sale_price = sale_price
        self.history_price = history_price
        self.image = image
        self.thumb_images = thumb_images
        self.shop_id = shop_id
        self.source_id = source_id
        self.source_type_code = source_type_code
        self.source_url = source_url