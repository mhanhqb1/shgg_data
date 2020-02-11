from flask import Blueprint, current_app
import requests
import json
from sqlalchemy.sql import text

from ..api.common import api_response, api_error
from ...database.database import db
from ...models.offer import Offer
from ...models.master_source_type import MasterSourceType

acc_offer_all = Blueprint('acc_offer_all', __name__)

@acc_offer_all.route('/acc/offers/all', methods = ['GET', 'POST'])
def acc_offer_all_func():
	# Init
	result = []
	offers = None

	# Get source types
	# sourceTypes = db.session.query(MasterSourceType.code).all()
	# for st in sourceTypes:
	# 	merchant = st.code
	offers = get_offer()
	if (offers != None and offers != []):
		for o in offers:
			result.append(o)

	if (result != []):
		sql = """
			INSERT INTO 
				offers(name, detail, start_date, end_date, image, url, source_id, source_type_code) 
			VALUES
				(:name, :content, :start_time, :end_time, :image, :link, :id, :merchant)
			ON 
				DUPLICATE KEY 
			UPDATE
				name=VALUES(name),
				detail=VALUES(detail),
				start_date=VALUES(start_date),
				end_date=VALUES(end_date),
				image=VALUES(image),
				url=VALUES(url)
		"""
		statement = text(sql)
		try:
			db.engine.execute(statement, result)
		except Exception as e:
			print(e)
			return 'Error'

	# Return data
	return api_response('OK')

def get_offer(merchant = ''):
	result = None
	token = 'GKbYMT1dQsIJ4bcwwG_FJ2s_3XPYX0BZ'
	url = 'https://api.accesstrade.vn/v1/offers_informations?merchant='
	if (merchant != ''):
		url += merchant
	headers = {
		'Authorization': 'Token ' + token,
		'accept-encoding': 'gzip, deflate, br',
		'Accepts': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'x-requested-with': 'XMLHttpRequest',
		'Content-Type': 'application/json'
	}
	try:
		result = requests.get(
			url, 
			headers=headers
		)
		data = json.loads(result.text.encode('utf8'))
		return data['data']
	except Exception as e:
		raise e
	return result