from flask import Blueprint, current_app

from .common import api_response, api_error
from ...database.database import db
from ...models.product import Product
from ...models.offer import Offer

home_getdata = Blueprint('home_getdata', __name__)

@home_getdata.route('/api/home/getdata', methods = ['GET', 'POST'])
def home_getdata_func():
	# Init
	result = {}
	param = {
		'limit': 24
	}

	# Get list product
	products = Product.get_all(param)
	result['products'] = products['data']

	# Get list offer
	offers = Offer.get_all({
		'limit': 6	
	})
	result['offers'] = offers['data']

	# Return data
	return api_response(result)