from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
import json

incomes = Blueprint('incomes', __name__, url_prefix='/api')

@incomes.route('/incomes/districts', methods=['GET'])
def get_district_polygons_data():
    """Get dummy data returned from the server."""
    data = {'Incomes': ['District1', 'District2', 'District3']}

    json_response = json.dumps(data)
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')

@incomes.route('/incomes/neighborhoods', methods=['GET'])
def get_neeighborhood_polygons_data():
    data = {'Incomes': ['Neighborhood1', 'Neighborhood2', 'Neighborhood3']}

    json_response = json.dumps(data)
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')
