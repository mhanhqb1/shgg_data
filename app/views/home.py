from flask import Blueprint, current_app, jsonify

from ..lib.http_ultility import send_request

home = Blueprint('home', __name__)

@home.route('/', methods = ['GET'])
def hello_func():
    data = crawler()
    result = {
    	'a': data['items'][0]['name'],
    	'b': len(data['items'])
    }
    return jsonify(result)

def crawler():
	url = "https://shopee.vn/api/v2/search_items/"
	querystring = {
		"by":"ctime",
		"limit":"100",
		"match_id":"2827",
		"newest":"1",
		"order":"desc",
		# "page_type":"search",
		"version":"2",
		"page": 150
	}
	result = send_request(url, querystring)
	if result and 'error' not in result:
		try:
			json_response = result.json()
			return json_response
		except Exception as e:
			print(e)
			return None