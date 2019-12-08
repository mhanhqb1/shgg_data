from flask import Blueprint, current_app, jsonify
from sqlalchemy.sql import text
from sqlalchemy import or_
from ...database.database import db
from ...models.product import Product
from ...models.master_cate import MasterCate

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import unquote

from datetime import datetime
import time
import re

shopee_crawler2 = Blueprint('shopee_crawler2', __name__)
shopeeMaxPage = 100
shopeeImageUrl = "https://cf.shopee.vn/file/"
sourceTypeCode = 'shopee'
todayTime = int(time.mktime(time.strptime(datetime.today().strftime('%Y-%m-%d'), "%Y-%m-%d")))

@shopee_crawler2.route('/shopee/crawler2', methods = ['GET'])
def shopee_crawler2_func():
	result = None
	cates = get_categories()
	if (len(cates) == 0):
		return jsonify('Done')
	ck = None
	count = 0
	for cate in cates:
		error = False
		page = cate.page
		cateUrl = cate.cate_url
		cateId = cate.cate_id
		cateName = cate.cate_name
		products = []
		while page <= shopeeMaxPage:
			try:
				print('---- Crawler Page ' + str(page) + ' ----')
				result = crawler(cateUrl, page)
				save_data(result, cateId, cateName)
				page = page + 1
				cate.page = page
				db.session.commit()
			except Exception as e:
				print(e)
				error = True
				return jsonify('Error 1')
		cate.updated = todayTime
		cate.page = 0
		db.session.commit()

	return jsonify(result)

def get_categories():
	cates = db.session.query(MasterCate).\
				filter(or_(MasterCate.updated < todayTime, MasterCate.updated == None)).\
				filter(MasterCate.source_type_code == sourceTypeCode).\
				all()
	return cates

def init_driver(url):
	# options = webdriver.ChromeOptions()
	# options.add_argument('headless')
	# options.add_argument('window-size=1200x600')
	# driver = webdriver.Chrome(chrome_options=options)
	driver = webdriver.Chrome(ChromeDriverManager().install())
	# driver = webdriver.Chrome()
	driver.get(url)
	time.sleep(3)
	print ("Executed Succesfull")
	return driver

def scroll_page(driver):
	SCROLL_PAUSE_TIME = 2

	# Get scroll height
	last_height = 4000
	new_height = 20

	while True:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(200, "+str(new_height)+");")
		driver.execute_script("console.log("+str(new_height)+");")
		driver.execute_script("console.log("+str(last_height)+");")

		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = new_height + 500
		if new_height >= last_height:
			break

def get_data(driver):
	# Init
	result = []
	i = 1

	# Get item
	itemsSelector = 'div.shopee-search-item-result div.shopee-search-item-result__item > div > a'
	items = driver.find_elements_by_css_selector(itemsSelector)
	for item in items:
		# print(i)
		i = i + 1
		price = 0
		image = None
		# Get url
		url = unquote(item.get_attribute('href'))

		# Get name
		parseName = re.findall(r'https://shopee.vn/(.*?)-i\.', url)
		name = str(parseName[0]).replace('-', ' ')

		# Get product ID, shop ID
		ids = re.findall(r'-i\.(.*?)$', url)
		ids = str(ids[0]).split('.')
		shopId = ids[0]
		productId = ids[1]

		# Get price
		priceCssSelector = 'div._36zw98 > div._2XtIUk > span._341bF0'
		parsePrice = item.find_elements_by_css_selector(priceCssSelector)
		if (parsePrice != []):
			price = parsePrice[0].text

		# Get image
		imageCssSelector = "._1gkBDw > ._3ZDC1p > ._1T9dHf"
		parseImage = item.find_elements_by_css_selector(imageCssSelector)
		if (parseImage != []):
			image = parseImage[0].get_attribute('style')
			image = re.findall(r'background-image: url\("https://cf.shopee.vn/file/(.*?)"\)', image)
			if (image != [] and image != None):
				image = image[0]

		result.append({
			'id': productId,
			'shop_id': shopId,
			'name': name,
			'price': price,
			'image': image,
			'url': url
		})
	return result

def crawler(url, page):
	param = '?page=' + str(page) + '&newest=50&sortBy=pop'
	driver = init_driver(url + param)
	scroll_page(driver)
	result = get_data(driver)
	print(len(result))
	driver.close()
	return result

def save_data(result, cateId, cateName):
	products = []
	if (result != None):
		for p in result:
			product = {
				"name": p['name'],
				'name_search': p['name'],
				'price': p['price'],
				'sale_price': p['price'],
				'image': p['image'] if 'image' in p else None,
				'thumb_images': json.dumps(p['images']) if 'images' in p else None,
				'shop_id': p['shop_id'],
				'source_id': p['id'],
				'source_type_code': sourceTypeCode,
				'source_url': p['url'],
				'source_cate_id': cateId,
				'source_cate_name': cateName,
				'history_price': None,
				'history_price_ts': None
			}
			products.append(product)
		if (products != []):
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
					source_cate_name=VALUES(source_cate_name)
			"""
			statement = text(sql)
			try:
				db.engine.execute(statement, products)
				cate.updated = todayTime
				db.session.commit()
			except Exception as e:
				print(e)
				return 'Error'