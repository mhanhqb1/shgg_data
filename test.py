from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import unquote

import time
import re

def init_driver(url):
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1200x600')
	# driver = webdriver.Chrome(chrome_options=options)
	driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
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
			image = image[0]

		result.append({
			'id': productId,
			'shop_id': shopId,
			'name': name,
			'price': price,
			'image': image
		})
	return result

def crawler(url):
	count = 0
	i = 0
	while i <= 100:
		param = '?page=' + str(i) + '&newest=50&sortBy=pop'
		driver = init_driver(url + param)
		i = i + 1
		scroll_page(driver)
		result = get_data(driver)
		for e in result:
			count = count + 1
			print(count)
		driver.close()
	print(count)

def main():
	url = 'https://shopee.vn/%C3%81o-thun-cat.78.2827'
	crawler(url)

main()


