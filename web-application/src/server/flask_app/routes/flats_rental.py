from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
import json
import csv as csv

flats_rental = Blueprint('flats_rental', __name__, url_prefix='/api')

@flats_rental.route('/flats_rental/', methods=['GET'])
def get_flats_rental_data():


    resources_folder = "./data/"


    with open(resources_folder+'plloguer2017.csv', 'r') as f:


        reader = csv.reader(f, delimiter=',')
        """
        header = reader.next()

        csv_lines = list(reader)

        print("Header -> ", header)
        print("Data from file: ", csv_lines)

        """

        csv_lines = list(reader)

        #print("CSV LINES: ", csv_lines)

        json_object = []

        tmp = {}
        c = 0
        for row in csv_lines:
            if(c == 0):
                header = row
                print("Header: ", header)
                c=1
            else:
                tmp = {}
                for item_idx, item in enumerate(row):

                    if(item_idx < len(header)):
                        tmp[header[item_idx]] = item
                try:
                    tmp['value'] =  float(tmp['price'])
                    json_object.append(tmp)
                except:
                    print("Failed for: ", row)
                    pass
                #data = json.dumps( [ row for row in csv_lines ] )

                #print("DATA: {}".join(data))
                #print out

        json_response = json.dumps(json_object)
        return Response(json_response,
                        status=html_codes.HTTP_OK_BASIC,
                        mimetype='application/json')
