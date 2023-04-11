from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pymysql
import json

app = Flask(__name__)
api = Api(app)
connection = pymysql.connect(host='localhost', user='root', password='QA2015!@#', db='classicmodels')


class OfficeMgt(Resource):
    # select data
    def get(self, office_code):
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `offices` WHERE `officeCode`=%s"
            cursor.execute(sql,(office_code))
            result = cursor.fetchone()
            if result is not None:
                res = {'code': result[0],
                        'city': result[1],
                       'phone': result[2],
                       'addressline1': result[3],
                       'addressline2': result[4],
                       'state': result[5],
                       'country': result[6],
                       'postalcode': result[7],
                       'territory': result[8]}
                return res
            else:
                return {"status": "not found"},404

    # insert data
    def post(self, office_code):
        args = parser.parse_args()
        json_msg = args['data'] #json.loads(args['data'])
        print(json_msg)
        print(type(json_msg))
        return {"status": "success"}, 200

    # modify data
    def put(self):
        pass

    # delete data
    def delete(self,office_code):
        with connection.cursor() as cursor:
            sql_delete = "DELETE FROM offices WHERE `officeCode`=%s"
            params = (office_code)
            # Execute the query
            cursor.execute(sql_delete, params)
            # the connection is not autocommited by default. So we must commit to save our changes.
            connection.commit()
        return {"status": "success"}, 204

api.add_resource(OfficeMgt, '/office/<string:office_code>')


if __name__ == '__main__':
    parser = reqparse.RequestParser()
    # Look only in the POST body
    parser.add_argument('data', type=list, location='json')
    app.run(debug=True)



from flask import Flask, jsonify, request

app = Flask(__name__)
stores = [
    {
        'name': 'beautiful store',
        'items': [
            {
                'name': 'flowers',
                'price': 100
            }
        ]
    },
    {
        'name': 'beautiful store 2',
        'items': [
            {
                'price': 100,
                'song_id':112,
                'name': 'hat bui nao',
                'description':'khong co',
                'type_id':'111111'
            }
        ]
    }
]


@app.route('/')
def home():
    return "Hello to Api cai nay da hoat dong"


@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store/<string:name>')
def get_store_name(name):
    for store in stores:
        if(store['name'] == name):
            return jsonify(store)
    return jsonify({'message': 'store not found'})


@app.route('/store')
def get_all_store_name():
    return jsonify({'stores': stores})


@app.route('/store/<string:name>/item', methods=['POST'])
def create_store_item(name):
    request_data = request.get_json()
    for store in stores:
        if(store['name'] == name):
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message':'store not found'})


@app.route('/store/<string:name>/item')
def get_store_item(name):
    for store in stores:
        if(store['name'] == name):
            return jsonify(store['items'])
    return jsonify({'message': 'store not found'})


app.run(port=8000)


