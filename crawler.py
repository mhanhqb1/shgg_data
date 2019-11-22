from .lib.http_ultility import send_request

def crawler():
	url = "https://shopee.vn/api/v2/search_items/"

	querystring = {"by":"pop","limit":"50","match_id":"78","newest":"0","order":"desc","page_type":"search","version":"2"}

	headers = {
		'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
		'Accept': "*/*",
		'Cache-Control': "no-cache",
		'Host': "shopee.vn",
		'Accept-Encoding': "gzip, deflate, br",
		'Connection': "keep-alive",
		'cache-control': "no-cache"
	}
	result = send_request(url, querystring)
	json_response = ''
	if result and 'error' not in result:
		try:
			json_response = result.json()
		except Exception as e:
			print(e)
	print(json_response)

if __name__ == "__main__":
	crawler()