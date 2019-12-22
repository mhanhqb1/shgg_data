from flask import Blueprint, current_app, request

from .common import api_response, api_error, get_params
from ...database.database import db
from ...models.offer import Offer

offers_all = Blueprint('offers_all', __name__)

@offers_all.route('/api/offers/all', methods = ['GET', 'POST'])
def offers_all_func():
	# Get param
	params = get_params(request)

	# Get products
	result = Offer.get_all(params)

	return api_response(result)