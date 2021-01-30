from flask import Flask
from flask import request
from flask_api import FlaskAPI
import urllib
import requests as urlRequests
import pprint
import worker



app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

@app.route('/bounce', methods=["GET", "POST"]) 
def bounce():
    if request.method == "POST":
        return request.data
    return "Pancakes!"

@app.route('/bounce/get', methods=["POST"])
def get():
    return str(urlRequests.get(url = request.data).json())
    #return urllib.request.urlopen(request.data).read().decode('utf-8')
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')