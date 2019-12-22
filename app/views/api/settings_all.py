from flask import Blueprint, current_app

from .common import api_response, api_error
from ...database.database import db
from ...models.cate import Cate
from ...models.master_source_type import MasterSourceType

settings_all = Blueprint('settings_all', __name__)

@settings_all.route('/api/settings/all', methods = ['GET', 'POST'])
def settings_all_func():
    # Init
    result = {
        'cates': [],
        'source_types': []
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

    # Get master source types
    sourceTypes = db.session.query(MasterSourceType).all()
    for st in sourceTypes:
        result['source_types'].append({
            'id': st.id,
            'code': st.code,
            'name': st.name,
            'url': st.url,
            'logo': st.logo
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