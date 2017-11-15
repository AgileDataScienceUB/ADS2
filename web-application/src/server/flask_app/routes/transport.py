from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
import json

transport = Blueprint('transport', __name__, url_prefix='/api')

@transport.route('/transport/give/route', methods=['GET'])
def get_district_polygons_data():
    """Get dummy data returned from the server."""
    data = {'Route': 'This is our route'}

    json_response = json.dumps(data)
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')