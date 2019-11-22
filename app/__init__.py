from flask import Flask

from .views import home
# Init this app
app = Flask(__name__)
app.config.from_pyfile('../config.py', silent=True)

# Register blueprints
_target_modules_list = [
	home.home
]
for _m in _target_modules_list:
    app.register_blueprint(_m)