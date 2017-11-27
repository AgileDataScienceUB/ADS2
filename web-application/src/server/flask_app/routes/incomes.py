from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
import json
from ..extensions import csv_to_json

incomes = Blueprint('incomes', __name__, url_prefix='/api')

@incomes.route('/incomes/neighborhoods', methods=['GET'])
def get_neeighborhood_polygons_data():
    resources_folder = "./data/"
    with open(resources_folder + 'avincome2015.csv', 'r') as f:
        json_response = csv_to_json(f)
        return Response(json_response,
                        status=html_codes.HTTP_OK_BASIC,
                        mimetype='application/json')
