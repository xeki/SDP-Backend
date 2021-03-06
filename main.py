import flask
from flask import Flask, flash, redirect, render_template, request, session, abort
#from flask_cors import CORS, cross_origin
from Vaccination import *
from Attraction import *
from flight import *
from hotel import *
from trade_off import *
from package import *
from combine import *
from cors_flask import *
from datetime import datetime

app = Flask(__name__)
#CORS(app)

@app.errorhandler(404)
def custom404(error):
	'''
	response = flask.jsonify({'message':error.description})
	response.status_code = 404
	response.status = 'error:Resource not found'
	return response'''
	response = {}
	response['error'] = True
	response['message'] =error.description
	response['status_code'] = 404
	response['status'] = 'error:Resource not found, please see the log file'
	return flask.jsonify(response)
@app.errorhandler(400)
def custom400(error):
	'''
	response = flask.jsonify({'message':error.description})
	response.status_code = 400
	response.status = 'error:Bad Request'
	return response'''
	response = {}
	response['error'] = True
	response['message'] =error.description
	response['status_code'] = 400
	response['status'] = 'error:Bad request, please see the log file'
	return flask.jsonify(response)
@app.route('/')
@crossdomain(origin='*')
def greetThem():
    return "Hi guys"

@app.route('/sdp',methods=['GET'])
@crossdomain(origin='*')
def package():
    try:
        originplace= request.args.get('originplace')
        destinationplace = request.args.get('destinationplace')
        outbounddate= request.args.get('outbounddate')#yyyy/mm/dd format
        inbounddate = request.args.get('inbounddate')#yyyy/mm/dd format
        date_format = "%Y-%m-%d"
        a = datetime.strptime(outbounddate, date_format)
        b = datetime.strptime(inbounddate, date_format)
        delta = b - a
        interval=delta.days
        print("duration interval: {}".format(interval))
        attractionStr=request.args.get('attractions')
        if attractionStr == None or attractionStr == "":
            attractionStr = 'shop'
        print("attractionStr: {}".format(attractionStr))
        tfDuration=request.args.get('tfd')
        tfPrice = request.args.get('tfp')
        tfTransfer = request.args.get('tft')
        thRanking = request.args.get('thr')
        thPrice = request.args.get('thp')
        adultStr = request.args.get('adult')
        if adultStr == None or adultStr =="":
            adult = 1
        else:
            adult=int(request.args.get('adult'))
        childrenStr = request.args.get('children')
        if childrenStr == None or childrenStr=="":
            children = 0
        else:
            children = int(request.args.get('children'))
        print("Adult Count: {}".format(adultStr))
        budget=float(request.args.get('budget'))
        originplace = cityEncoder(originplace)
        destinationplace = cityEncoder(destinationplace)
    except:
        flask.abort(400, "Invalid arguments in the parameter")

    print("Origin:{} ".format(originplace))
    print("Destination {} ".format(destinationplace))
    print("Outbound date: {} ".format(outbounddate))
    print("Inbound date: {} ".format(inbounddate))
    print("Adult: {} ".format(adult))
    print("Children {} ".format(children))
    print("Budget {} ".format(budget))
    try:
        attractionList=attractionStr.split(',')
        attraction=getAttractions(destinationplace,attractionList)
        vaccination=getVaccination(destinationplace)
        av = attraction.copy()
        av.update(vaccination)

        data_f=getFlightData(originplace, destinationplace, outbounddate, inbounddate,adult,children)
        # data_f = getFlightData('Helsinki', 'Paris', '2016-11-08', '2016-11-9')
        data_h = getHotelsForDestinationCity(destinationplace, outbounddate, inbounddate)

        options = combine(data_f, data_h)
        dic = trade_off(options,tfPrice,tfDuration,tfTransfer,thPrice,thRanking)
        print(dic)
        front = analysis(dic)
        results=packages(options,front,data_f,data_h,av,budget,adult,children,interval)
        print(results)
        response={'results':results}

        return flask.jsonify(response)
    except:
        flask.abort(400, "Sorry, an error has occured. ")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)