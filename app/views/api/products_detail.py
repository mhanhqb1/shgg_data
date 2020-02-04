from flask import Blueprint, current_app, request

from .common import api_response, api_error, get_params
from ...database.database import db
from ...models.product import Product
from ...lib.http_ultility2 import send_request_beecost

products_detail = Blueprint('products_detail', __name__)

@products_detail.route('/api/products/detail', methods = ['GET', 'POST'])
def products_detail_func():
	# Init
	result = []
	shopeeImageUrl = "https://cf.shopee.vn/file/"

	# Get param
	params = get_params(request)
	productId = params['id'] if 'id' in params else ''

	# Validate param
	if (productId == ''):
		return api_error('Product ID is invalid.')

	# Get data
	data = db.session.query(Product).filter(Product.id == productId).first()
	if (data == None):
		return api_error('Product is not found.')

	# Get history price
	historyPrice = get_price_from_beecost(data.source_id, data.shop_id)
	prices = None
	price_ts = None
	if (historyPrice != None):
		prices = historyPrice['item_history']['price']
		price_ts = historyPrice['item_history']['price_ts']

	# Return
	result = {
		'id': data.id,
		'name': data.name,
		'price': data.price,
		'image': shopeeImageUrl + data.image,
		'source_url': data.source_url,
		'source_type_code': data.source_type_code,
		'source_type_name': data.source_type_code,
		'source_type_url': data.source_type_code,
		'history_price': prices,
		'history_price_ts': price_ts
	}

	return api_response(result)

def get_price_from_beecost(productId, shopId):
	beecostApi = "https://apiv2.beecost.com/ecom/product/history"
	url = beecostApi + "?product_base_id=1__" + str(productId) + "__" + str(shopId)
	try:
		result = send_request_beecost(url)
		if result and 'error' not in result:
			try:
				data = result.json()
				return data['data']
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)
	return None