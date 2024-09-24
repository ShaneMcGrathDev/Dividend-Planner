from flask import Flask, jsonify, request 
from flask_restful import Api, Resource
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Ensure this is added to allow cross-origin requests
api = Api(app)

class AddNumbers(Resource):
    def get(self):
        num1 = request.args.get('num1', type=float)
        num2 = request.args.get('num2', type=float)

        result = num1 + num2

        return jsonify({"result: result"})
    
# Register route code

api.add_resource(AddNumbers, '/api/add')


if __name__ == '__main__':
    app.run(debug=True)