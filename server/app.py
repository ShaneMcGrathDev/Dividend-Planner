from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for all routes
CORS(app)

# Define the route for the addition operation
@app.route('/api/add', methods=['GET'])
def add_numbers():
    try:
        # Retrieve the numbers from the query parameters
        num1 = float(request.args.get('num1'))
        num2 = float(request.args.get('num2'))
        
        # Perform the addition
        result = num1 + num2
        
        # Return the result as a JSON response
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
