from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
import json

recommendation = Blueprint('recommendation', __name__, url_prefix='/api')

@recommendation.route('/recommendation/scores', methods=['GET'])
def calculate_recommendation():
    """Get dummy data returned from the server."""

    # Access body parameters like: max_rental_price, max_tranport_time...

    # Access model instances array.


    data = {'Recommendation': 'Should return an array of results for each neighborhood/district id!'}

    json_response = json.dumps(data)
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')