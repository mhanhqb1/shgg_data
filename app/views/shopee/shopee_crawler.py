from flask import Blueprint, current_app, jsonify
from sqlalchemy.sql import text
from ...database.database import db
from ...models.product import Product
from ...lib.http_ultility2 import send_request

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

shopee_crawler = Blueprint('shopee_crawler', __name__)
shopeeApiUrl = "https://shopee.vn/api/v2/search_items/"
shopeeMaxPage = 2
shopeeLimit = 50
shopeeImageUrl = "https://cf.shopee.vn/file/"
sourceTypeCode = 'shopee'

@shopee_crawler.route('/shopee/crawler', methods = ['GET'])
def shopee_crawler_func():
	cates = get_categories()
	driver = webdriver.Chrome(ChromeDriverManager().install())
	# driver = webdriver.Chrome()
	driver.get('https://shopee.vn/')
	ck = ';'.join(['{}={}'.format(item.get('name'), item.get('value')) for item in driver.get_cookies()]) 
	for cate in cates:
		page = 0
		refer = 'https://shopee.vn/%C3%81o-thun-cat.78.2827'
		while page <= shopeeMaxPage:
			try:
				result = crawler(cate, page*shopeeLimit, refer, ck)
				page = page + 1
				if (result != None):
					for p in result:
						product = {
							"name": p['name'],
							'name_search': p['name'],
							'price': format_price(p['price_before_discount']),
							'sale_price': format_price(p['price']),
							'image': shopeeImageUrl + p['image'],
							'shop_id': p['shopid'],
							'source_id': p['itemid'],
							'source_type_code': sourceTypeCode,
							'source_url': convert_url(p['name'], p['itemid'], p['shopid'])
						}
						statement = text("""
							INSERT INTO 
								products(name, name_search, price, sale_price, image, shop_id, source_id, source_type_code, source_url) 
							VALUES
								(:name, :name_search, :price, :sale_price, :image, :shop_id, :source_id, :source_type_code, :source_url)
							ON 
								DUPLICATE KEY 
							UPDATE
								name=VALUES(name),
								name_search=VALUES(name_search),
								source_url=VALUES(source_url),
								price=VALUES(price),
								sale_price=VALUES(sale_price)
						""")
						try:
							db.engine.execute(statement, **product)
						except Exception as e:
							return jsonify(e)
			except Exception as e:
				print(e)
				return jsonify('Error')
					

	return jsonify(result)

def crawler(cateId, newest, refer, ck):
	querystring = {
		"by":"pop",
		"limit": shopeeLimit,
		"match_id": cateId,
		"newest": newest,
		"page_type": "search",
		"order": "desc",
		"version": "2"
	}
	result = send_request(shopeeApiUrl, querystring, refer, ck)
	if result and 'error' not in result:
		try:
			data = result.json()
			return data['items']
		except Exception as e:
			raise e

def get_categories():
	return [
		#78 thoi trang nam
		2828, 2829, 9566
	]

def format_price(price):
	if (price == None):
		return 0
	return int(price)/10000 if price > 0 else price

def convert_url(name, productId, shopId):
	baseUrl = "https://shopee.vn/"
	name = name.replace(" ", "-")
	name = name.replace("[","-")
	name = name.replace("]", "-")
	return baseUrl + "-" + name + "-i." + str(shopId) + "." + str(productId)


