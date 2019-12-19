from requests_html import HTMLSession

def crawler():
	session = HTMLSession()
	url = "https://shopee.vn/"
	# url = "https://www.python.org/"
	r = session.get(url)
	r.html.render()
	# sel = 'div.shopee-recommend-search-word-text'
	sel = '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div/div/div[2]/div/div[1]/ul/li[1]/div/a[1]/div/div[2]/div'
	result = r.html.search('Thiết {} Điện Tử ')[0]
	print(result)
	

if __name__ == "__main__":
	crawler()