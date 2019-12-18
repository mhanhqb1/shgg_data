from flask import Blueprint, current_app

from .common import api_response, api_error
from ...database.database import db
from ...models.cate import Cate

settings_all = Blueprint('settings_all', __name__)

@settings_all.route('/api/settings/all', methods = ['GET', 'POST'])
def settings_all_func():
    result = {
    	'cates': []
    }
    cates = db.session.query(Cate).all()
    for c in cates:
    	result['cates'].append({
    		'id': c.id,
    		'name': c.name,
    		'slug': c.slug,
    		'image': c.image,
    		'icon': c.icon
    	})
    return api_response(result)