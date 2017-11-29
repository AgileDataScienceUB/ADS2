from flask import Flask
from flask_cors import CORS
from .config import CONFIG, setup_logger
from .models import District, Neighborhood
from .routes import polygons, incomes, flats_rental, transport, twitter, recommendation, test
import os





__version__ = '0.0.1'

BLUEPRINTS = (polygons, incomes, flats_rental, transport, twitter, recommendation, test)

def create_app():
    """Create app and configure Flask-security, databases, loggers."""
    app = Flask(__name__)


    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    print("Configuring flask app for: {}".format(config_name))
    app.config.from_object(CONFIG[config_name])

    setup_logger()
    #db.init_app(app)




    # set this running app as global context. This will tell SQLAlchemy which
    # 'app' to use, since flask can have multiple apps
    app.app_context().push()

    configure_blueprints(app, BLUEPRINTS)

    #transport_graph = TransportGraph().construct_graph()
    #Instantiate root class to have the neighborhood instances array

    # set up cross origin handling
    CORS(app, headers=['Content-Type'])
    #user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    #security = Security(app, user_datastore)



    return app

def configure_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
