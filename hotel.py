#-*- coding: latin-1 -*-
from urllib.request import urlopen
#import requests
import json
from dateutil import parser
from datetime import datetime
#from datetime import timedelta
from city_code import *
import random


def ManageCity(city):
    # link = "https://iatacodes.org/api/v6/cities?api_key=5276c2c4-0d42-4423-b758-733794c23f1e"
    # r = requests.get(link)
    # data = json.loads(r.text)
    city = city.lower()
    city = city.replace("ä", "a")
    city = city.replace("ö", "o")
    # result_list = data['response']
    result_list = city_list()
    for result in result_list:
        if (result['Name'].lower() == city):
            # return result['code']
            return True
    return False


def getHotelsForDestinationCity(city, check_in, check_out):
    hotelUrl = 'http://api.tripexpert.com/v1/destinations?api_key='
    API_KEY = "3644ac54270d20d577ae19a86c698d1f"
    mycity = city
    LIMIT = 3
    if mycity == "":
        return {"Error": "City can not be empty"}
    validCity = ManageCity(mycity)
    if not validCity:
        return {"Error": "Invalid city name"}
    # making API call to trip expert to list destinations
    url = hotelUrl + API_KEY
    data = urlopen(url).read().decode('utf-8')
    jsonData = json.loads(data)
    jsonData = jsonData['response']['destinations']
    destIdList = []
    destId = ""
    # checking if our city is in the list of destinations
    for destDict in jsonData:
        if destDict["name"] == mycity:
            destId = destDict["id"]
            break
        else:
            destIdList.append(destDict["id"])
    # if our city is not in the trip-expert destinations list we'll pick a random destination
    if destId == "":
        destId = random.choice(destIdList)

    try:
        # DATE PARSING
        parseDate = str(parser.parse(str(check_in)))
        date = parseDate.split(' ')[0]
        checkInDate = datetime.strptime(date, '%Y-%m-%d')
        checkInDate = checkInDate.strftime('%m/%d/%Y')
        parseDate = str(parser.parse(str(check_out)))
        date = parseDate.split(' ')[0]
        checkOutDate = datetime.strptime(date, '%Y-%m-%d')
        checkOutDate = checkOutDate.strftime('%m/%d/%Y')

        url = 'http://api.tripexpert.com/v1/venues?destination_id=' + str(destId) + '&limit=' + str(
            LIMIT) + '&check_in=' + checkInDate + '&check_out=' + checkOutDate + '&api_key=' + API_KEY
        print("Url: {}".format(url))
        response = urlopen(url).read().decode('utf-8')
        response = json.loads(response)
        totalVenues = response['response']['venues']
        venueList = []
        id = 1
        for venue in totalVenues:
            hotelGeoLat = venue['latitude']
            hotelGeoLong = venue['longitude']
            hotelName = venue['name']
            pricePerDay = venue['low_rate']
            ranking = venue['tripexpert_score']
            price = random.randint(100, 350)
            venueList.append({"id": id, "name": hotelName, "latitude": hotelGeoLat, "longitude": hotelGeoLong,
                              "low_rate": pricePerDay, "ranking": ranking, "room_price": price})
            id += 1

        return venueList
    except:
        return {"Error": "Error in searching hotel details"}


# def extractForTradeOff(city, check_in, check_out):
#     myDestVenues = getHotelsForDestinationCity(city, check_in, check_out)
#     trade_h = []
#     for venue in myDestVenues:
#         hotel = {}
#         hotel['hotel' + str(venue["id"])] = {"ranking": venue["ranking"], "room_price": venue["room_price"]}
#         trade_h.append(hotel)
#     print(trade_h)


# loop = True
# while loop:
#     city = input("Enter a city: ")
#
#     myDest = extractForTradeOff(city, "2016-11-11", "2016-11-13")
#     print(myDest)
#     loopAgain = input("Loop again: ")
#     if loopAgain == "n":
#         loop = False