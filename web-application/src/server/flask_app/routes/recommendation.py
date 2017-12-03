from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
from ..models import Root, TransportGraph
import json
import numpy as np


recommendation = Blueprint('recommendation', __name__, url_prefix='/api')

r = Root()
transport_graph = TransportGraph()
transport_graph.constructGraph()

@recommendation.route('/recommendation/scores', methods=['POST'])
def calculate_recommendation():
	"""Get dummy data returned from the server."""

	# Access body parameters like: max_rental_price, max_tranport_time...
	# Variables para calcular tiempo transport
	if not request.json:
		return Response(json.dumps({"Message":"Error getting body from request"}),
						status=html_codes.HTTP_OK_BASIC,
						mimetype='application/json')
	body = request.json
	print("Body: ", body)

	lat  = float(body['lat'])
	lng = float(body['lng'])
	metro = int(body['metro'])
	bus = int(body['bus'])
	max_transport_time = int(body['max_transport_time'])

	max_rental_price = int(body['max_rental_price'])
	min_rental_price = int(body['min_rental_price'])
	night_live = int(body['night_live'])

	"""lat = 1
                lng = 2
                metro = 1    #int(0 no, 1 si)
                bus = 0        #int (0 no, 1 si)
                transport_cost = {} #Obtain transport cost from each neighborhood to [lat,lng] {id : cost, id : cost,..}

                max_transport_time = 30 #int
                min_rental_price = 500 #int
                max_rental_price = 1000 #int
                night_live = 2 #int 0->low, 1->middium, 2->High"""


	# Access model instances array.
	data = filter_neighbourhood(max_transport_time, min_rental_price, max_rental_price, night_live,lat,lng)

	#data = {'Recommendation': 'Should return an array of results for each neighborhood/district id!'}

	json_response = json.dumps(data)
	return Response(json_response,
					status=html_codes.HTTP_OK_BASIC,
					mimetype='application/json')


@recommendation.route('/recommendation/test', methods=['GET'])
def calculate_recommendation_test():
	"""Get dummy data returned from the server."""

	lat = 41.38570
	lng = 2.16383
	metro = 1    #int(0 no, 1 si)
	bus = 0        #int (0 no, 1 si)
	max_transport_time = 30 #int
	min_rental_price = 500 #int
	max_rental_price = 1000 #int
	night_live = 2 #int 0->low, 1->middium, 2->High"""


	# Access model instances array.
	data = filter_neighbourhood(max_transport_time, min_rental_price, max_rental_price, night_live,lat,lng)

	#data = {'Recommendation': 'Should return an array of results for each neighborhood/district id!'}

	json_response = json.dumps(data)
	return Response(json_response,
					status=html_codes.HTTP_OK_BASIC,
					mimetype='application/json')


def filter_neighbourhood(max_transport_time, min_rental_price, max_rental_price, night_live, lat, lng):

	print( min_rental_price, max_rental_price)
	print(night_live)
	array_possible_neighbourhoods = []

	#r.neighborhoods = {'id' : Neighbourhood()}
	#Neighbouhood = self.avg_flat_rental_from_council
	#Neighbouhood = self.avg_flat_rental_from_web
	#Neighbouhood = self.store_bar
	#Neighbouhood = self.store_disco

	#Bar values --> 25% - 17.000000 50% - 50.000000 75% - 94.000000
	#Disco values --> 25% - 0.000000 50% - 1.000000 75% - 3.000000

	for key, value in r.neighborhoods.items():


		include = False
		if ((value.avg_flat_rental_from_council < max_rental_price) and (value.avg_flat_rental_from_council > min_rental_price)) or ((value.avg_flat_rental_from_web < max_rental_price) and (value.avg_flat_rental_from_web > min_rental_price)):

			if (night_live == 0):
				if((value.store_bar <= 17.000000) and (value.store_disco <= 0.000000)):
					include = True

			elif(night_live == 1):
				if((value.store_bar <= 94.000000) and (value.store_bar > 17.000000)):
					include = True
				elif((value.store_disco <= 3.000000) and (value.store_disco > 0.000000)):
					include = True

			elif(night_live == 2):
				if((value.store_bar > 94.000000) or (value.store_disco > 3.000000)):
					include = True


		print(transport_graph.shortpath([value.geometry.centroid.x, value.geometry.centroid.y],[lat, lng])[0])
		if include:
			if (transport_graph.shortpath(np.array([value.geometry.centroid.x, value.geometry.centroid.y]),np.array([lat, lng]))[0] <= max_transport_time):
				array_possible_neighbourhoods.append(key)
		#if include: array_possible_neighbourhoods.append(key)

	return {'recommendation': array_possible_neighbourhoods}
