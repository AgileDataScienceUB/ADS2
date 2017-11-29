from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
import json

recommendation = Blueprint('recommendation', __name__, url_prefix='/api')

global data_form
data_form = {'lat': 0, 'lng' : 0, 'max_rental_price' : 0, 'min_rental_price' : 0, 'max_transport_time' : 0, 'tipo_transporte' : 'hola', 'night_live' : 0}

@recommendation.route('/recommendation/scores', methods=['GET'])
def calculate_recommendation():
    """Get dummy data returned from the server."""

    # Access body parameters like: max_rental_price, max_tranport_time...

    # Access model instances array.
    data = filter_neighbourhood()

    #data = {'Recommendation': 'Should return an array of results for each neighborhood/district id!'}

    json_response = json.dumps(data_form)
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')


@recommendation.route('/recommendation/submit_form/<lat>/<lng>/<max_rental_price>/<min_rental_price>/<max_transport_time>/<tipo_transporte>/<night_live>', methods=['POST'])
def set_data_form(lat, lng, max_rental_price, min_rental_price, max_transport_time, tipo_transporte, night_live):
	

	data_form['lat'] = lat
	data_form['lng'] = lng
	data_form['max_rental_price'] = max_rental_price
	data_form['min_rental_price'] = min_rental_price
	data_form['max_transport_time'] = max_transport_time
	data_form['tipo_transporte'] = tipo_transporte
	data_form['night_live'] = night_live

	json_response = json.dumps(data_form)
	return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')


def filter_neighbourhood():

	array_possible_neighbourhoods = []

	#r.neighborhoods = {'id' : Neighbourhood()}
	#Neighbouhood = self.avg_flat_rental_from_council = None
    #Neighbouhood = self.avg_flat_rental_from_web = None
    #Neighbouhood = self.store_bar = None
    #Neighbouhood = self.store_disco = None

    #Bar values --> 25% - 1.479290, 50% - 2.391592, 75% -3.317221
    #Disco values --> 25% - 0.000000, 50% - 0.026244, 75% - 0.113033

	for key, value in r.neighborhoods.items():

		include = False
		if ((value.avg_flat_rental_from_council < data_form['max_rental_price']) and (value.avg_flat_rental_from_council > data_form['min_rental_price'])) or ((value.avg_flat_rental_from_web < data_form['max_rental_price']) and (value.avg_flat_rental_from_web > data_form['min_rental_price'])):
			
			if (data_form['night_live'] == 0):
				if((value.store_bar <= 1.479290) and (value.store_disco <= 0.000000)):
					include = True
			elif(data_form['night_live'] == 1):
				if((value.store_bar <= 3.317221) and (value.store_bar > 1.479290)):
					include = True
				elif((value.store_disco <= 0.113033) and (value.store_disco <= 0.000000)):
					include = True

			elif(data_form['night_live'] == 2):
				if((value.store_bar > 3.317221)):
					include = True
				elif((value.store_disco > 0.113033)):
					include = True



		if include: array_possible_neighbourhoods.append(key)

	
	return {'Recommendation': array_possible_neighbourhoods}

