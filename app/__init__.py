from flask import Flask

from .database.database import db
# from .views import home
from .views.shopee import shopee_crawler2, proxies, shopee_crawler
from .views.api import common, settings_all

# Init this app
app = Flask(__name__)
app.config.from_pyfile('../config.py', silent=True)

def init_db():
    db.init_app(app)

# Register blueprints
_target_modules_list = [
	# home.home,
	shopee_crawler.shopee_crawler,
	shopee_crawler2.shopee_crawler2,
	proxies.proxies,
	common.common,
	settings_all.settings_all
]
for _m in _target_modules_list:
    app.register_blueprint(_m)