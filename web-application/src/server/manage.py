from flask_script import Manager
from flask_app.app import app
import os

print('Initializing Manager...')
manager = Manager(app)

import sys

print("Python version: ", sys.version)

@manager.command
def runserver():
    """Run the flask app in development mode"""

    # app.run('0.0.0.0', 33507)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    manager.run()