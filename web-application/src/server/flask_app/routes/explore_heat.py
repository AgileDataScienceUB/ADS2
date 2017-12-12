from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
from ..models import Root
import json

import numpy as np

explore_heat = Blueprint('explore_heat', __name__, url_prefix='/api')

r = Root()

ordre=np.ones(8) #array que indica l'ordre d'ordenació, ara mateix tot seria de menor a major

#donada una llista de +1 (ordenat ascendent) o -1 (ordenat descendent)
#retorna un diccionari on per cada id (barri) hi ha una llista amb l'score (1-5)

@explore_heat.route('/explore_heat/', methods=['GET'])
def calculate_score():
    # la llista es rental_price, rental_price_web,mean_size_price, night_live, population, young_percent, num_restaurants, num_clothes_store
    score={}
    maxim=np.zeros(8)
    minim=1e6*np.ones(8)
    for key, value in r.neighborhoods.items():

        rental_council = value.avg_flat_rental_from_council
        rental_web = value.avg_flat_rental_from_web
        mean_size_price = value.avg_flat_meter_rental
        night = value.store_bar + 3*value.store_disco
        population = value.women + value.men
        young =  100*value.age_young
        restaurants = value.store_restaurant
        clothes_stores = value.store_clothes

        llista=np.array([rental_council,rental_web,mean_size_price,night,population,young,restaurants,clothes_stores])
        score[key]=llista

        maxim[llista>maxim]=llista[llista>maxim]
        minim[llista<minim]=llista[llista<minim]

    interval = (maxim-minim)/5. +minim

    final_rank={}
    for key in score:
        llista = score[key]
        rank = []
        for item , fact in zip(llista,interval):
            i=1
            while item>i*fact:
                i=i+1
            rank.append(i)
        final_rank[key]=list(rank*ordre)

    json_response = json.dumps(final_rank)
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')
