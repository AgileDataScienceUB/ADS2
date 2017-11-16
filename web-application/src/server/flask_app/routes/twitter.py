from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
import json

twitter = Blueprint('twitter', __name__, url_prefix='/api')


#Add tweets to this array to make them automatically sent to the client when '/twitter/tweets/get' is called.
tweets_array = []

@twitter.route('/twitter/tweets/get', methods=['GET'])
def get_gathered_tweets():
    data = {'tweets': tweets_array}

    print("Starting twitter data gathering")
    json_response = json.dumps(data)
    tweets_array = []
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')

@twitter.route('/twitter/gather/start/', methods=['GET'])
def start_twitter_gathering():
    data = {'Twitter': 'Gathering started'}

    print("Starting twitter data gathering")
    json_response = json.dumps(data)

    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')

@twitter.route('/twitter/gather/stop/', methods=['GET'])
def stop_twitter_gathering():
    data = {'Twitter': 'Gathering stopped'}

    json_response = json.dumps(data)
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')



