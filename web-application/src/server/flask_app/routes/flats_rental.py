from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
import json
from ..extensions import csv_to_json

flats_rental = Blueprint('flats_rental', __name__, url_prefix='/api')

@flats_rental.route('/flats_rental/', methods=['GET'])
def get_flats_rental_data():
    resources_folder = "./data/"
    with open(resources_folder+'flats_rental_council.csv', 'r') as f:
        json_response = csv_to_json(f)
        return Response(json_response,
                        status=html_codes.HTTP_OK_BASIC,
                        mimetype='application/json')