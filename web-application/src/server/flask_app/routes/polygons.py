from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
import json as json
import csv as csv
from os import listdir
from os.path import isfile, join


polygons = Blueprint('polygons', __name__, url_prefix='/api')

@polygons.route('/polygons/districts', methods=['GET'])
def get_district_polygons_data():
    json_data=open('./data/polygons_districts_geo.json').read()
    data = json.loads(json_data)

    json_response = json.dumps(data)
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')

@polygons.route('/polygons/neighborhoods', methods=['GET'])
def get_neighborhood_polygons_data():
    json_data = open('./data/polygons_neighborhoods_geo.json').read()
    data = json.loads(json_data)

    json_response = json.dumps(data)
    return Response(json_response, status=html_codes.HTTP_OK_BASIC, mimetype='application/json')
