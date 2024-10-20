from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Pull configs from config file
app.config.from_object('app.config.Config')

# requires JWT_SECRET_KEY in config
jwt = JWTManager(app)

# Routes needs app and jwt. Only import after app creation.
from app import routes

# In case we are not running with gunicorn
if __name__ == '__main__':
    app.run()