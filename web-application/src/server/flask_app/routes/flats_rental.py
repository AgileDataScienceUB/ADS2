from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
import json
import csv as csv

flats_rental = Blueprint('flats_rental', __name__, url_prefix='/api')

@flats_rental.route('/flats_rental/districts', methods=['GET'])
def get_district_polygons_data():
    """Get dummy data returned from the server."""
    data = {'Rental': ['District1', 'District2', 'District3']}

    json_response = json.dumps(data)
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')

@flats_rental.route('/flats_rental/neighborhoods', methods=['GET'])
def get_neeighborhood_polygons_data():


    resources_folder = "./data/"


    with open(resources_folder+'plloguer2017.csv', 'rb') as f:


        reader = csv.reader(f)
        """
        header = reader.next()

        csv_lines = list(reader)

        print("Header -> ", header)
        print("Data from file: ", csv_lines)

        """
        header = reader.next()
        csv_lines = list(reader)

        print("CSV LINES: ", csv_lines)

        json_object = []

        tmp = {}
        for row in csv_lines:
            tmp = {}
            for item_idx, item in enumerate(row):


                tmp[header[item_idx]] = item
            json_object.append(tmp)
            #data = json.dumps( [ row for row in csv_lines ] )

            #print("DATA: {}".join(data))
            #print out

        json_response = json.dumps(json_object)
        return Response(json_response,
                        status=html_codes.HTTP_OK_BASIC,
                        mimetype='application/json')
