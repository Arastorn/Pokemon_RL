# app/__init__.py

from flask import Flask

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the views
from app import routes

# Load the config file
app.config.from_object('app.config.DevelopmentConfig')

# Launch the url on your browser
import webbrowser
from threading import Timer
port = 5000
url = "http://127.0.0.1:{0}".format(port)
#Timer(1.25, lambda: webbrowser.open(url)).start()
