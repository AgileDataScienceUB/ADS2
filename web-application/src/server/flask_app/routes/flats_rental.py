from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
import json
import csv as csv

flats_rental = Blueprint('flats_rental', __name__, url_prefix='/api')

@flats_rental.route('/flats_rental/', methods=['GET'])
def get_flats_rental_data():
    resources_folder = "./data/"
    with open(resources_folder+'palquiler.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        csv_lines = list(reader)
        header = csv_lines[0]
        json_object = []
        for row in csv_lines[1:]:
                tmp = {}
                for item_idx, item in enumerate(row):
                    if(item_idx < len(header)):
                        tmp[header[item_idx]] = item
                json_object.append(tmp)
        json_response = json.dumps(json_object)
        return Response(json_response,
                        status=html_codes.HTTP_OK_BASIC,
                        mimetype='application/json')