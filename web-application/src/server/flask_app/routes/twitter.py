from flask import Blueprint, Response, request
from flask_security import auth_token_required
from ..app_utils import html_codes, token_login
import json
import csv as csv
import pymongo
import tweepy
from tweepy import Stream,StreamListener

twitter = Blueprint('twitter', __name__, url_prefix='/api')


#Add tweets to this array to make them automatically sent to the client when '/twitter/tweets/get' is called.
tweets_array = []
storing_tweets_array = False
auth = None
conn = None
db = None

@twitter.route('/twitter/tweets/get', methods=['GET'])
def get_gathered_tweets():
    #data = {'tweets': tweets_array}

    ##mock block to read non dynamic data yet
    #data = {'tweets':{'_id': '59fb4c6bec130e310c4bdf55','coordinates': [41.38567462, 2.19740259],
    #'text': '@popthatpartybcn PRES: \nEste Miércoles 8 de noviembre - @Asap__tyy -\nShow en directo en… https://t.co/uJF7HLKv6c',
    #'created': 'Thu Nov 02 16:48:41 +0000 2017'}}

    #resources_folder = "./data/"
    #tweets = json.load(open(resources_folder+'tweets_2017.json'))
    #data={'tweets':tweets}

    data = get_all_tweet_data()

    json_response = json.dumps(data)
    tweets_array = []
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')

@twitter.route('/twitter/gather/start/', methods=['GET'])
def start_twitter_gathering():
    data = {'Twitter': 'Gathering started'}
    
    storing_tweets_array = True
    twitterStream = Stream(auth, listener()) 
    twitterStream.filter(locations=[2.0504377635,41.2787636541,2.3045074059,41.4725622346])	
    
    print("Starting twitter data gathering")
    json_response = json.dumps(data)
    
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')
    
@twitter.route('/twitter/gather/stop/', methods=['GET'])
def stop_twitter_gathering():
    data = {'Twitter': 'Gathering stopped'}
    
    conn.close()
    twitterStream = None
    storing_tweets_array = False
    
    json_response = json.dumps(data)
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')
                    
#------------------------------------------------------------------------------------------------------

key_words = [
    'party','fiesta','fest ','fest!','festival','festa',
    'club','disco','discoteca','vip','dj',
    'night','noche','nit','nocturna',
    'event','show',
    'cine','teatr','theatre',
    'concert','concierto',
    'pub','bar',
    'beer','drink','drunk','cervesa','cerveza','mojito','gintonic','cocktail','wine',
    'whiskey','rum','wine','sangria',
    'copas','copes','tapas','tapes',
    'dance','dancing','ball','baile','baila','salsa',
    'musical','rave ',
    'going out','go out','hang out','goingout','goout','hangout',
    'having fun','havingfun','celebra'
]
false_key_words = [
    'barcelon','bare ','baron',
    'travel',
    'public',
    'manifest',
    'Trump','rumia','forum',
    'peniten',
    'brave',
    'bonit','dignit'
] #bar in barcelona, rave in travel

def criteria(jdata):
    return geo_check(jdata) and key_word_check(jdata['text'])
def geo_check(jdata):
    return jdata['coordinates'] is not None

def key_word_check(text):
    import re
    print(text)
    text = text.lower()
    big_regex = re.compile('|'.join(map(re.escape, false_key_words)))
    text = big_regex.sub("", text)
    for key_word in key_words:
        if key_word in text:
            print('Stored! Keyword ', key_word, ' found')
            return True
    return False

class listener(StreamListener):
    def __init__(self):
        super(StreamListener, self).__init__()
        self.num_tweets = 0
        self.db = db
        self.collection = self.db.tweets
    
    def on_data(self, status):
        if self.num_tweets < 1e4:
            jdata = json.loads(status)
            if geo_check(jdata) is True:
                document = {'id': jdata['id'], 'geo': jdata['geo'], 'coordinates': jdata['coordinates'],
                            'text': jdata["text"], 'created': jdata["created_at"]}
                if storing_tweets_array:
                    tweets_array.append(document)
                if key_word_check(jdata):
                    self.collection.insert_one(document) 
                print (jdata['geo'],jdata["text"])
                self.num_tweets += 1
            return True
        else:
            return False
    
    def on_error(self, status):
        print(status)				
    
#------------------------------------------------------------------------------------------------------

def get_all_tweet_data():
    collection = connect_to_mlab()
    tweets = []
    attributes = ['id','geo','text','created']
    for tweet in collection.find()[:]:
        new_tweet = {}
        for attribute in attributes:
            try:
                new_tweet[attribute] = tweet[attribute]
            except:
                print('missing attribute ' + attribute)
        tweets.append(new_tweet)
    return tweets

def connect_to_mlab():
    try:
        with open("./data/credentials/mlab/credentials", 'r', encoding='utf-8') as f:
            [name,password,url,dbname]=f.read().splitlines()
        conn=pymongo.MongoClient("mongodb://{}:{}@{}/{}".format(name,password,url,dbname))
        print ("Connected successfully!!!")
        print([name,password,url,dbname])
    except pymongo.errors.ConnectionFailure as e:
        print ("Could not connect to MongoDB: %s" % e)
    
    db = conn[dbname]
    print (db)
    collection = db.tweets
    return  collection

def twitter_auth():	
    with open('./data/credentials/twitter/consumer_key', 'r') as f:
        consumer_key =  f.read()
    f.closed
    with open('./data/credentials/twitter/consumer_secret', 'r') as f:
        consumer_secret = f.read()
    f.closed
    with open('./data/credentials/twitter/access_key', 'r') as f:
        access_key = f.read()
    f.closed
    with open('./data/credentials/twitter/access_secret', 'r') as f:
        access_secret = f.read()
    f.closed
    with open('./data/credentials/twitter/user_name', 'r') as f:
        USER_NAME = f.read()
    f.closed
    
    #Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)