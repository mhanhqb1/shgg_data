from flask import Blueprint, current_app

from .common import api_response, api_error
from ...database.database import db
from ...models.cate import Cate

settings_all = Blueprint('settings_all', __name__)

@settings_all.route('/api/settings/all', methods = ['GET', 'POST'])
def settings_all_func():
    # Init
    result = {
        'cates': []
    }

    # Get list cates
    cates = db.session.query(Cate).all()
    for c in cates:
        result['cates'].append({
            'id': c.id,
            'name': c.name,
            'slug': c.slug,
            'image': c.image,
            'icon': c.icon
        })

    # Get list social
    result['social'] = [
        {
            'icon': 'fa-facebook-f',
            'name': 'Facebook',
            'url': '',
            'class': 'facebook'
        },
        {
            'icon': 'fa-instagram',
            'name': 'Instagram',
            'url': '',
            'class': 'instagram'
        },
        {
            'icon': 'fa-twitter',
            'name': 'Twitter',
            'url': '',
            'class': 'twitter'
        },
        {
            'icon': 'fa-google-plus-g',
            'name': 'Google+',
            'url': '',
            'class': 'gplus'
        }
    ]

    return api_response(result)