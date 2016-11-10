import flask
import requests
from flask import Flask, flash, redirect, render_template, request, session, abort
import json
from Vaccination import *
from Attraction import *
#from hotel import *
#from trade_off import *
#from flight import *
#from package import *
#from combine import *

app = Flask(__name__)

#limitless-lowlands-64274.herokuapp.com/sdp?originplace=Helsinki&destinationplace=Paris&outbounddate=2016-11-17&inbounddate=2016-11-21&attractions=shop,bar&tfd=min&tfp=min&tft=min&thr=max&thp=min
@app.route('/')
def hello_world():
    callMe = whatsApp()
    print("hey bro: " + callMe)
    return 'Hello World!' +callMe


if __name__ == '__main__':
    app.run()
