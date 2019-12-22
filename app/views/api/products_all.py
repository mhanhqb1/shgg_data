from flask import Blueprint, current_app, request

from .common import api_response, api_error, get_params
from ...database.database import db
from ...models.product import Product

products_all = Blueprint('products_all', __name__)

@products_all.route('/api/products/all', methods = ['GET', 'POST'])
def products_all_func():
	# Get param
	params = get_params(request)

	# Get products
	result = Product.get_all(params)

	return api_response(result)