import json
import time
from datetime import datetime

from flask import Blueprint, current_app, jsonify
from sqlalchemy.sql import text
from sqlalchemy import or_
from ...database.database import db
from ...models.product import Product
from ...models.master_cate import MasterCate
from ...lib.http_ultility2 import send_request, send_request_beecost

shopee_crawler = Blueprint('shopee_crawler', __name__)
shopeeApiUrl = "https://shopee.vn/api/v2/search_items/"
shopeeMaxPage = 1000
shopeeLimit = 100
shopeeImageUrl = "https://cf.shopee.vn/file/"
sourceTypeCode = 'shopee'
todayTime = int(time.mktime(time.strptime(datetime.today().strftime('%Y-%m-%d'), "%Y-%m-%d")))

#https://apiv2.beecost.com/ecom/product/history?product_base_id=1__1966264329__20175544
beecostApi = "https://apiv2.beecost.com/ecom/product/history"

@shopee_crawler.route('/shopee/crawler', methods = ['GET'])
def shopee_crawler_func():
	result = None
	cates = get_categories()
	if (len(cates) == 0):
		return jsonify('Done')
	ck = None
	count = 0
	for cate in cates:
		page = 0
		refer = cate.cate_url
		cateId = cate.cate_id
		cateName = cate.cate_name
		products = []
		while page <= shopeeMaxPage:
			try:
				result = crawler(cateId, page*shopeeLimit, refer, ck)
				page = page + 1
				if (result != None):
					for p in result:
						price = 0
						priceHistory = None
						priceHistoryTs = None
						beecost = get_price_from_beecost(p['itemid'], p['shopid'])
						if (beecost != None):
							itemHistory = beecost['item_history'] if 'item_history' in beecost else None
							if itemHistory != None:
								price = itemHistory['price'][-1]
								priceHistory = json.dumps(itemHistory['price'])
								priceHistoryTs = json.dumps(itemHistory['price_ts'])
								print(price)
						product = {
							"name": p['name'],
							'name_search': p['name'],
							'price': int(price),
							'sale_price': int(price),
							'image': p['image'] if 'image' in p else None,
							'thumb_images': json.dumps(p['images']) if 'images' in p else None,
							'shop_id': p['shopid'],
							'source_id': p['itemid'],
							'source_type_code': sourceTypeCode,
							'source_url': convert_url(p['name'], p['itemid'], p['shopid']),
							'source_cate_id': cateId,
							'source_cate_name': cateName,
							'history_price': priceHistory,
							'history_price_ts': priceHistoryTs
						}
						count += 1
						print(str(count) + '. ' + product['name'])
						products.append(product)
				else:
					print('None')
					break
				print('-------------Crawl page ' + str(page))
			except Exception as e:
				print(e)
				return jsonify('Error 1')
			if (products == []):
				continue
			sql = """
				INSERT INTO 
					products(name, name_search, price, sale_price, image, thumb_images, shop_id, source_id, source_type_code, source_url, source_cate_id, source_cate_name, history_price, history_price_ts) 
				VALUES
					(:name, :name_search, :price, :sale_price, :image, :thumb_images, :shop_id, :source_id, :source_type_code, :source_url, :source_cate_id, :source_cate_name, :history_price, :history_price_ts)
				ON 
					DUPLICATE KEY 
				UPDATE
					name=VALUES(name),
					name_search=VALUES(name_search),
					source_url=VALUES(source_url),
					image=VALUES(image),
					price=VALUES(price),
					sale_price=VALUES(sale_price),
					source_cate_id=VALUES(source_cate_id),
					source_cate_name=VALUES(source_cate_name),
					history_price=VALUES(history_price),
					history_price_ts=VALUES(history_price_ts),
					thumb_images=VALUES(thumb_images)
			"""
			statement = text(sql)
			try:
				db.engine.execute(statement, products)
				cate.updated = todayTime
				db.session.commit()
			except Exception as e:
				print(e)
				return 'Error'		

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
			print(e)

def get_categories():
	cates = db.session.query(MasterCate).filter(or_(MasterCate.updated < todayTime, MasterCate.updated == None)).filter(MasterCate.source_type_code == sourceTypeCode).all()
	return cates

def format_price(price):
	if (price == None):
		return 0
	return int(price)/10000 if price > 0 else price

def convert_url(name, productId, shopId):
	baseUrl = ""#"https://shopee.vn/"
	name = name.replace(" ", "-")
	name = name.replace("[","-")
	name = name.replace("]", "-")
	return baseUrl + "-" + name + "-i." + str(shopId) + "." + str(productId)

def get_price_from_beecost(productId, shopId):
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


