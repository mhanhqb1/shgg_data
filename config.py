import os

# Debug mode
DEBUG = True

SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

# App path
APP_PATH = os.path.dirname(os.path.abspath(__file__))

# Database config
MYSQL_HOST = os.environ.get('MYSQL_HOST') or "localhost"
MYSQL_PORT = os.environ.get('MYSQL_PORT') or 3306
MYSQL_USER = os.environ.get('MYSQL_USER') or "root"
MYSQL_PASS = os.environ.get('MYSQL_PASS') or ""
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or "shgr_crawler"
SQLALCHEMY_DATABASE_URI = 'mysql://'+MYSQL_USER+':'+MYSQL_PASS+'@'+MYSQL_HOST+'/'+MYSQL_DATABASE