from flask import Blueprint, request, current_app
from json_tricks import dump, dumps
from datetime import datetime

common = Blueprint('common', __name__)

def api_response(data):
	result = {
		'status_code': 200,
		'status': 'OK',
		'body': data
	}
	return dumps(result)

def check_header(headers):
	check = True
	apiKey = hashlib.md5(current_app.config["API_SECRET_KEY"]).hexdigest()
	headerAuth = headers['Authorization'] if 'Authorization' in headers else ''
	if (headerAuth != apiKey):
		check = False
	return check

def api_error(message, codeType = '', field = ''):
	errorCodes = {
		'': '',
		'missing': 1000,
		'duplicate': 1001,
		'invalid': 1002,
		'other': 1003,
		'account_disable': 2000,
		'account_not_verified': 2001,
		'token_expired': 2002,
		'cannot_delete_user': 2003
	}
	result = {
		'status_code': 400,
		'status': 'ERROR',
		'error_code': errorCodes[codeType] if codeType in errorCodes else '',
		'error_field': field,
		'body': message
	}
	return dumps(result)

def get_params(req):
	params = {}
	if (req.is_json):
		for p in req.json:
			params[p] = req.json[p]
	if (req.form):
		for p in req.form:
			params[p] = req.form[p]
	if (req.args):
		for p in req.args:
			params[p] = req.args[p]
	return params