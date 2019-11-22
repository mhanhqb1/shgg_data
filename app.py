from app import app as application
from app import init_db

init_db()

if __name__ == "__main__":
	application.run(host='127.0.0.1', port=1234)