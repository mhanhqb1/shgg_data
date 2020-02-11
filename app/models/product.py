from ..database.database import db
from .cate import Cate
from .master_source_type import MasterSourceType

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
    updated = db.Column('updated', db.Integer)
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

    def get_all(param = {}):
        # Init
        shopeeImageUrl = "https://cf.shopee.vn/file/"
        result = []
        productCates = {}
        productSourceTypes = {}

        # Get param
        sourceType = param['type'] if 'type' in param else ''
        limit = param['limit'] if 'limit' in param else 20
        page = param['page'] if 'page' in param else 1
        offset = int(limit)*(int(page) - 1)
        cateSlug = param['cate_slug'] if 'cate_slug' in param else ''
        search = param['s'] if 's' in param else ''
        cateId = None

        # Get list source types
        sourceTypes = db.session.query(MasterSourceType).all()
        for s in sourceTypes:
            productSourceTypes[s.code] = {
                'id': s.id,
                'code': s.code,
                'name': s.name,
                'logo': s.logo,
                'url': s.url,
                'description': s.description
            }

        # Get list cate
        cates = db.session.query(Cate).all()
        for c in cates:
            if (c.slug == cateSlug):
                cateId = c.id
            productCates[c.id] = {
                'id': c.id,
                'name': c.name,
                'slug': c.slug,
                'image': c.image,
                'icon': c.icon
            }

        # Query
        query = db.session.query(Product).filter(Product.cate_id.isnot(None))

        # Filter
        if (cateId != None):
            query = query.filter(Product.cate_id == cateId)

        if (sourceType != ''):
            query = query.filter(Product.source_type_code == sourceType)

        if (search != ''):
            query = query.filter(Product.name.like("%{}%".format(search)))

        # Get product list
        products = query.order_by(Product.updated.desc()).limit(limit).offset(offset).all()
        total = query.count()
        for p in products:
            result.append({
                'id': p.id,
                'name': p.name,
                'price': p.price,
                'source_url': p.source_url,
                'image': shopeeImageUrl + p.image,
                'shop_id': p.shop_id,
                'cate': productCates[p.cate_id] if p.cate_id in productCates else None,
                'updated': p.updated,
                'source_type': productSourceTypes[p.source_type_code] if p.source_type_code in productSourceTypes else None
            })

        return {
            'data': result,
            'total': total
        }

    def check_link(input):
        result = ''
        return result