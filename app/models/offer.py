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

    def get_all(param = {}):
        # Init
        result = []
        sourceTypeCode = param['type'] if 'type' in param else ''
        limit = param['limit'] if 'limit' in param else 20
        page = param['page'] if 'page' in param else 1
        offset = int(limit)*(int(page) - 1)
        dateFormat = "%Y-%m-%d"

        # Query
        query = db.session.query(Offer)

        # Filter
        if (sourceTypeCode != ''):
            query = query.filter(Offer.source_type_code == sourceTypeCode)

        # Get data
        offers = query.order_by(Offer.id.desc()).limit(limit).offset(offset).all()
        total = query.count()

        for o in offers:
            result.append({
                'id': o.id,
                'name': o.name,
                'image': o.image,
                'url': o.url,
                'detail': o.detail,
                'start_date': o.start_date.strftime(dateFormat),
                'end_date': o.end_date.strftime(dateFormat)  
            })

        return {
            'data': result,
            'total': total
        }

