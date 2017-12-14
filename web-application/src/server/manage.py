from flask_script import Manager
from flask_app.app import app

print('Initializing Manager...')
manager = Manager(app)

import sys

print("Python version: ", sys.version)

@manager.command
def runserver():
    """Run the flask app in development mode"""
    app.run('0.0.0.0', 80)

if __name__ == "__main__":
    manager.run()