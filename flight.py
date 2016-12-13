import json
import requests
from city_code import *

# def ManageCity(city):
#     link = "https://iatacodes.org/api/v6/cities?api_key=5276c2c4-0d42-4423-b758-733794c23f1e"
#     r = requests.get(link)
#     data = json.loads(r.text)
#     result_list = data['response']
#     for result in result_list:
#         if (result['name'] == city):
#             return result['code']

def getFlightData(origin, destination, dateOfDeparture, dateOfreturn,adultCount=1,childrenCount=0):
    api_key = "AIzaSyCFe4aroUT5mXbLx450-AvAQYC5GLPBwYk"
    url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + api_key
    headers = {'content-type': 'application/json'}
    destCity = city(destination)
    originCity = 	city(origin)
    if destCity==None or originCity == None:
        result = {"Error": "City not found in IATA city list"}													
        print("Desination-City {} Origin-City {}\nError {}".format(destCity,originCity,result))
        return None
								
    flight_From = {'origin': originCity, 'destination': destCity, 'date': dateOfDeparture}
    flight_Return={'origin': destCity, 'destination': originCity, 'date': dateOfreturn}
    flightInfo=[flight_From,flight_Return]

    params = {'request': {'slice': flightInfo, 'passengers': {'adultCount': adultCount,'childCount':childrenCount}, 'solutions': 3, 'refundable': False}}
    print(params)
    try:
        request = requests.post(url, data=json.dumps(params), headers=headers)
        data = json.loads(request.text)
    except:
        result = {"Error": "No result found from flight"}
        print(result)								
        return result
    try:
        #print("data {}".format(data))
        options = data['trips']['tripOption']
        carriersDict = {}
        carriers = data['trips']['data']['carrier']
        for carrier in carriers:
            carriersDict[carrier['code']] = carrier['name']
        airportName = {}
        airports = data['trips']['data']['airport']
        for airport in airports:
            airportName[airport['code']] = airport['name']

        flightList = []
        count=1
        for option in options:
            flight_package={}
            price = {'Currency': option['saleTotal'][:3], 'Price': float(option['saleTotal'][3:])}
            flight = {}
            flight['price']=price
            flight['id']=count
            slices = option['slice']
            twoWay=[]
            for slice in slices:
                oneWay_package={}
                segments = slice['segment']
                duration=slice['duration']
                oneWay_package['duration']=duration
                oneWay = []
                for segment in segments:
                    detail={}
                    flight_Number=segment['flight']['number']
                    carrierName = carriersDict[segment['flight']['carrier']]
                    legs = segment['leg']
                    for leg in legs:

                        detail['departureTime']=leg['departureTime']
                        detail['arrivalTime'] = leg['arrivalTime']
                        detail['origin']=airportName[leg['origin']]
                        detail['destination'] = airportName[leg['destination']]
                        detail['carrier'] = carrierName
                        detail['flightNumber'] = flight_Number
                    oneWay.append(detail)
                oneWay_package['info']=oneWay
                twoWay.append(oneWay_package)
            flight['flight_info']=twoWay

            flight_package['flight']=flight
            count=count+1
            flightList.append(flight_package)

        return flightList
    except:
        result = {"Error":"Error Parsing the result"}
        print(result)								
        return result


# def getTradeOff(flightList):
#     trade_f = []
#     for i in range(len(flightList)):
#         package={}
#         result={}
#         flight = flightList[i]['flight' + str(i + 1)]
#         price = flight['price']['Price']
#
#         durations = flight['flight_info']
#         durationList = []
#         for duration in durations:
#             durationList.append(duration['duration'])
#
#         time = 0
#         for j in range(len(durationList)):
#             time += durationList[j]
#
#         package['flight_price']=price
#         package['duration']=time
#         result['flight'+str(i+1)]=package
#         trade_f.append(result)
#     print(trade_f)
# data=getFlightData('Helsinki','Paris','2016-11-08','2016-11-9')
# print(data)
# getTradeOff(data)



