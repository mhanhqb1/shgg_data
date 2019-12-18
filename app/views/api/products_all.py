from flask import Blueprint, current_app

from .common import api_response, api_error
from ...database.database import db
from ...models.product import Product

products_all = Blueprint('products_all', __name__)

@products_all.route('/api/products/all', methods = ['GET', 'POST'])
def products_all_func():
    result = Product.get_all()
    return api_response(result)