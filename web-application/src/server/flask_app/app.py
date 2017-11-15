"""Entry point for the server application."""

import json
import logging
from . import create_app
from flask_socketio import SocketIO


logger = logging.getLogger(__name__)

app = create_app()


# Configuring socket
global socketio
socketio = SocketIO(app)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    socketio.emit('event', {"message":"Hellow"})






def run():
    """Isolated entry point of the app, if not using manage.py"""
    try:
        #app.run('0.0.0.0', 8081)


        socketio.start_background_task(socketio.run(app,port=8081,host='0.0.0.0',debug=True))



    except Exception as exc:
        logger.error(exc.message)
    finally:
        # get last entry and insert build appended if not completed
        # Do something here
        pass
