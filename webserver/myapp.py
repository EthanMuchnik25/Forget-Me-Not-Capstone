from flask import Flask

app = Flask(__name__)
# Routes needs app. Only import after app creation.
from app import routes

app.config.from_object('app.config.Config')

# In case we are not running with gunicorn
if __name__ == '__main__':
    app.run()