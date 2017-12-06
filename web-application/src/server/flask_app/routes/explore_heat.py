from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
from ..models import Root


explore_heat = Blueprint('explore_heat', __name__, url_prefix='/api')

r = Root()

@explore_heat.route('/explore_heat/', methods=['GET'])
#donada una llista amb les caracteristiques i una altra llista de +1 (ordenat ascendent) o -1 (ordenat descendent)
#retorna una llista on per cada id (barri) hi ha una llista amb l'score (1-5)
# {‘recomendation’ : [{id:01, value:1}, {id:02, value:2}]} el 01, 02.. son str i el 1, 2 son ints

def calculate_score():
    return 'hola'
