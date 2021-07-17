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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.data'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secret_key"
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

db.init_app(app)
api = Api(app)

jwt = JWT(app, authenticate, identity)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return "Hello World!"
    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/signup')

if __name__ == '__main__':
    app.run(debug=True)