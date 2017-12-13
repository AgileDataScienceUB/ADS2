from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
from ..models import Root, TransportGraph
import json
import numpy as np
import pandas as pd
from random import randint


recommendation = Blueprint('recommendation', __name__, url_prefix='/api')

r = Root()
transport_graph = TransportGraph()

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
	#print("Body: ", body)

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
				metro = 1	#int(0 no, 1 si)
				bus = 0		#int (0 no, 1 si)
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
	metro = 1	#int(0 no, 1 si)
	bus = 0		#int (0 no, 1 si)
	max_transport_time = 100 #int
	min_rental_price = 100 #int
	max_rental_price = 2000 #int
	night_live = 2 #int 0->low, 1->middium, 2->High"""


	# Access model instances array.
	data = filter_neighbourhood(max_transport_time, min_rental_price, max_rental_price, night_live,lat,lng)

	#print(transport_graph.calculateRouteBetween([40.38570, 1.16383],[lat, lng]))
	#data = {'Recommendation': 'Should return an array of results for each neighborhood/district id!'}

	json_response = json.dumps(data)
	return Response(json_response,
					status=html_codes.HTTP_OK_BASIC,
					mimetype='application/json')

@recommendation.route('/recommendation/generate', methods=['GET'])
def calculate_recommendation_generate():
	"""Get dummy data returned from the server."""

	lat = 41.38570
	lng = 2.16383
	metro = 1	#int(0 no, 1 si)
	bus = 0		#int (0 no, 1 si)
	max_transport_time = 100 #int
	min_rental_price = 100 #int
	max_rental_price = 2000 #int
	night_live = 2 #int 0->low, 1->middium, 2->High"""

	rental_prince_options = np.array([400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 5000])
	max_transport_time_options = np.array([20,30,40,50,60,90,120]) #5,10,
	night_live_options = np.array([0,1,2])
	lat_lng_option = np.array([['Universitat', 41.38570, 2.16383], ['MediaPro', 41.40436, 2.19382], ['Sant Joan De Deu', 41.38364, 2.10125], ['Vall dHebron', 41.42792, 2.14186], ['LaCaixa', 41.38768, 2.12667] ])

	finaldata = []
	for max_transport_time in max_transport_time_options:
		for min_rental_price in rental_prince_options:
			for max_rental_price in rental_prince_options[rental_prince_options > min_rental_price]:
				for night_live in night_live_options:
					for name, lat, lng in lat_lng_option:
						lat = float(lat)
						lng = float(lng)
						# Access model instances array.
						data = filter_neighbourhood(max_transport_time, min_rental_price, max_rental_price, night_live,lat,lng)

						data['input'] = [name, lat, lng, max_transport_time, min_rental_price, max_rental_price, night_live]
						print (data['input'] )
						print (data['recommendation'])
						finaldata.append(data)


	finaldataToSend = {'data' : finaldata}
	json_response = json.dumps(finaldataToSend)
	return Response(json_response,
					status=html_codes.HTTP_OK_BASIC,
					mimetype='application/json')

@recommendation.route('/recommendation/generate2', methods=['GET'])
def calculate_recommendation_generate2():
	"""Get dummy data returned from the server."""

	res = pd.DataFrame(columns= ['name', 'lat', 'lng', 'max_transport_time', 'min_rental_price', 'max_rental_price', 'night_live', 'recommendation'])
	rental_prince_options = np.array([400, 500, 600, 700, 800, 900, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 5000])
	max_transport_time_options = np.array([20,30,40,50,60,90,120]) #5,10,
	night_live_options = np.array([0,1,2])
	lat_lng_option = np.array([['Universitat', 41.38570, 2.16383], ['MediaPro', 41.40436, 2.19382], ['Sant Joan De Deu', 41.38364, 2.10125], ['Vall dHebron', 41.42792, 2.14186], ['LaCaixa', 41.38768, 2.12667] ])

	finaldata = []
	for max_transport_time in max_transport_time_options:
		for min_rental_price in rental_prince_options:
			for max_rental_price in rental_prince_options[rental_prince_options > min_rental_price]:
				for night_live in night_live_options:
					for name, lat, lng in lat_lng_option:
						lat = float(lat)
						lng = float(lng)
						print([name, lat, lng, max_transport_time, min_rental_price, max_rental_price, night_live])
						# Access model instances array.
						data = filter_neighbourhood(max_transport_time, min_rental_price, max_rental_price, night_live,lat,lng)

						res.loc[res.shape[0]] = np.array([name, lat, lng, max_transport_time, min_rental_price, max_rental_price, night_live, data])

	res.to_csv('restult.csv')
	print(res)
	json_response = json.dumps({'ok': 1})
	return Response(json_response,
					status=html_codes.HTTP_OK_BASIC,
					mimetype='application/json')






def filter_neighbourhood(max_transport_time, min_rental_price, max_rental_price, night_live, lat, lng):

	array_possible_neighbourhoods = []

	ordre =np.array([-1,-1,night_live-1,1,1,1,-1])
	addend = np.array([6,6,night_live-1,0,0,0,6])
	dics={}
	score={}
	maxim=np.zeros(7)
	minim=1e6*np.ones(7)



	#Bar values --> 25% - 17.000000 50% - 50.000000 75% - 94.000000
	#Disco values --> 25% - 0.000000 50% - 1.000000 75% - 3.000000

	for key, value in r.neighborhoods.items():

		include = False
		if ((value.avg_flat_rental_from_council <= max_rental_price) and (value.avg_flat_rental_from_council >= min_rental_price)) or ((value.avg_flat_rental_from_web <= max_rental_price) and (value.avg_flat_rental_from_web >= min_rental_price)):

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



		if include:
			tTransport = transport_graph.calculateRouteBetween([value.geometry.centroid.y, value.geometry.centroid.x],[lat, lng])[0]
			if (tTransport <= max_transport_time):
				poblacio = value.men +value.women
				rental_web = value.avg_flat_rental_from_web
				mean_size_price = value.avg_flat_meter_rental
				night = value.store_bar + 3*value.store_disco
				restaurants = value.store_restaurant /float(poblacio)
				clothes_stores = value.store_clothes /float(poblacio)
				aliment_stores = value.store_grocery /float(poblacio)
				temps_trans= tTransport

				llista=np.array([rental_web,mean_size_price,night,restaurants,clothes_stores,aliment_stores,temps_trans])
				score[key]=llista

				maxim[llista>maxim]=llista[llista>maxim]
				minim[llista<minim]=llista[llista<minim]

	# return(len(score))
	interval = (maxim-minim)/5. +minim

	#print(interval)
	#print(score)
	final_rank={}
	for key in score:
		llista = score[key]
		rank = []
		print(key, llista)
		for item , fact in zip(llista,interval):
			#----------------------------------
			#Que fa exactament???
			i=1
			while item>i*fact:
				i=i+1
			#----------------------------------
			rank.append(i)

		hola=rank*ordre
		hola[hola<0]+=6
		final_rank[key]=list(hola)

	print(final_rank)

	rank_ordre={}
	for barri in final_rank:
		rank_ordre[barri]=int(np.sum(final_rank[barri]))

	#print(rank_ordre)

	sort=(sorted(rank_ordre.items(), key=lambda x: x[1]))[::-1]

	i=1
	for item in sort:
		array_possible_neighbourhoods.append({'id':'%02d' % item[0], 'value': i} )
		i=i+1 if i<5 else 5


	return {'recommendation': array_possible_neighbourhoods}

	#{'recommendation': [1,3,5,6]}
	#{'recommendation': [{id:01, value:1}, {id:02, value:2}]}}

	#'recommendation': array_possible_neighbourhoods és un diccionari amb id dels barris que compleixen i el temps de transport_cost
	###################################
