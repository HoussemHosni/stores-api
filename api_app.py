import os
from datetime import timedelta
from db import db
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister
from security import authenticate, identity


app = Flask(__name__)

uri = os.environ.get("DATABASE_URL", 'sqlite:///data.db')  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "secret_key"
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)


api = Api(app)

jwt = JWT(app, authenticate, identity)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return "Hello REST API!"
    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/signup')


if __name__ == '__main__':
    app.run(debug=True)