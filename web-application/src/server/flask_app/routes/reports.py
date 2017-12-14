from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
from ..models import Root
import json

import numpy as np

report = Blueprint('report', __name__, url_prefix='/api')

r = Root()

ordre=np.ones(8) #array que indica l'ordre d'ordenació, ara mateix tot seria de menor a major

#donada una llista de +1 (ordenat ascendent) o -1 (ordenat descendent)
#retorna un diccionari on per cada id (barri) hi ha una llista amb l'score (1-5)

@report.route('/report/', methods=['GET'])
def obtain_report():
    id=int(request.args.get('n_id'))

    print('IDDDDDD',id,type(id))
    llista=r.neighborhoods
    barri=llista[id-1]

    web_link=barri.idealista_url
    web_retal_meter=barri.avg_flat_meter_rental


    child=barri.age_child*100
    young=barri.age_young*100
    adult=barri.age_adult*100
    old=barri.age_old*100
    population=barri.men +barri.women
    income = barri.avg_income
    print(income)

    array_report=[]
    array_report.append({
        'id': '%02d' % id,
        'link_idealista': web_link,
        'price_square_meter': web_retal_meter,
        'child': child,
        'young': young,
        'adult': adult,
        'old': old,
        'population': population,
        'income': income})  #

    json_response = json.dumps(array_report)
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')