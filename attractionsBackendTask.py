import flask
import requests
from flask import Flask
import json
app = Flask(__name__)

@app.errorhandler(400)
def custom400(error):
	response = flask.jsonify({'message':error.description})
	response.status_code = 400
	response.status = 'error:Bad Request'
	return response
@app.route('/getattraction',methods=['GET'])
def combinedInputAttraction():
	url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
	API_KEY = "AIzaSyDJf6XiNsSQzWe-QXY_gT1yfa01W5PryZs"
	attractionList = []
	city = []
	queryStr = ""
	if len(flask.request.data)==0 and len(flask.request.args)!=0:
	#if parameters are passed as part of the url
		try:
			city = flask.request.args.getlist("city")
			attractionList = flask.request.args.getlist("attractions")
			print("My city: {} List of attractions: {}".format(city,attractionList))
		except:
			flask.abort(400,"Invalid arguments in the parameter")
	elif len(flask.request.data)!=0:
	#if parameters are passed as json data
		data = flask.request.get_json(force=True)
		print("Request data {}".format(data))
		try:
			attractionList = data.get("attractions")
			city.append(data.get("city"))
		except:
			flask.abort(400,"Invalid arguments in the parameter")
	else:
		flask.abort(400,"Invalid arguments in the parameter")
	#building multiple attraction names with connective word 'OR'
	try:
		queryStr = attractionList[0]
		for i in range(1,len(attractionList)):
			queryStr += " OR " + attractionList[i]
		
		#attractions only for a single city
		queryStr += " in " + city[0]
	except:
		flask.abort(400,"Invalid arguments in the parameter")
		
	url = url + queryStr+"&key="+API_KEY
	print("Url: {}".format(url))
	r = requests.get(url)
	resultset = json.loads(r.text)
	results = resultset["results"]
	resultFields = ['index','formatted_address','name','rating','types']
	#fields to be filtered from the reslut set
	resultDict = {}
	tempList = []
	for i in range(len(results)):
		tempDict = {}
		tempDict[resultFields[0]] = i
		tempDict[resultFields[1]] = results[i].get(resultFields[1])
		tempDict[resultFields[2]] = results[i].get(resultFields[2])
		tempDict[resultFields[3]] = results[i].get(resultFields[3])
		tempDict[resultFields[4]] = results[i].get(resultFields[4])
		tempList.append(tempDict.copy())
	resultDict["result"] = tempList
	return flask.jsonify(**resultDict)

	
@app.route('/')
def helloWorld():
	return "Hello man!"	
	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8484)
	
