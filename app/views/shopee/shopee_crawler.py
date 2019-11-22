from flask import Blueprint, current_app, jsonify
from ...database.database import db
from ...models.product import Product
from ...lib.http_ultility import send_request

shopee_crawler = Blueprint('shopee_crawler', __name__)
shopeeApiUrl = "https://shopee.vn/api/v2/search_items/"
shopeeMaxPage = 1000
shopeeLimit = 100
shopeeImageUrl = "https://cf.shopee.vn/file/"
sourceTypeCode = 'shopee'

@shopee_crawler.route('/shopee/crawler', methods = ['GET'])
def shopee_crawler_func():
	cates = get_categories()
	products = []
	for cate in cates:
		page = 0
		while page <= shopeeMaxPage:
			result = crawler(cate, page*shopeeLimit)
			page = page + 1
			if (result != None):
				for p in result:
					image = shopeeImageUrl + p['image']
					name = p['name']
					name_search = name
					shopId = p['shopid']
					salePrice = format_price(p['price'])
					price = format_price(p['price_before_discount'])
					sourceId = p['itemid']
					newProduct = Product(name, name_search, price, salePrice, None, image, shopId, sourceId, sourceTypeCode)
					if (sourceId not in products):
						db.session.add(newProduct)
						db.session.commit()
					products.append(sourceId)

	return jsonify(result)

def crawler(cateId, newest):
	querystring = {
		"by":"ctime",
		"limit": shopeeLimit,
		"match_id":cateId,
		"newest":newest,
		"page_type": "search",
		"order":"desc",
		"version":"2"
	}
	result = send_request(shopeeApiUrl, querystring)
	if result and 'error' not in result:
		try:
			data = result.json()
			return data['items']
		except Exception as e:
			print(e)
			return None

def get_categories():
	return [
		#78 thoi trang nam
		2827#, 2828, 2829, 9566
	]

def format_price(price):
	if (price == None):
		return 0
	return int(price)/10000 if price > 0 else price
