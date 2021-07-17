from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):

    '''parser = reqparse.RequestParser()
    parser.add_argument('name', 
                        required=True, 
                        help="A store must have a name")'''

    
    def get(self,name):

        store = StoreModel.find_by_name(name)
        if not store:
            return {"message":f"The store {name} not found"}, 404
        return store.json(), 200

    def post(self, name):
        
        if StoreModel.find_by_name(name):
            return {"message": f"The store {name} not found"}, 400
        
        store = StoreModel(name)
        
        try:
            store.save_to_db()
        except:
            return {"message": "Insertion Error! Try again please"}, 500
        
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if not store:
            return {"message": f"The store {name} not found"}, 404
        
        store.delete_from_db()
        return store.json()


class StoreList(Resource):
    def get(self):
        return {"Stores": [store.json() for store in StoreModel.query.all()]}

