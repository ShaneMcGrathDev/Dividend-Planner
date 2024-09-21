from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Backend Connection Test Worked!"})