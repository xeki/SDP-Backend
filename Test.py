import flask
import requests
from flask import Flask, flash, redirect, render_template, request, session, abort
import json
import Vaccination
import Attraction
import flight
import hotel
import trade_off
import package
import combine

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
