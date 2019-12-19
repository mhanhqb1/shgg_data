from app import app as application
from app import init_db

init_db()

if __name__ == "__main__":
	application.run(host='0.0.0.0', port=5000)