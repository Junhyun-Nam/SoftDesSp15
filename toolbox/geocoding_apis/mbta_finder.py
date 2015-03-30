"""
Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

import urllib   # urlencode function
import urllib2  # urlopen function (better than urllib version)
import json


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib2.urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    place = place_name.split()
    url = "https://maps.googleapis.com/maps/api/geocode/json?address="
    for elem in place:
        url += elem + "+"
    url = url[:-1]
    json = get_json(url)
    lat = json[u'results'][0][u'geometry'][u'location'][u'lat']
    lng = json[u'results'][0][u'geometry'][u'location'][u'lng']
    return (lat, lng)


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    url = MBTA_BASE_URL+'?api_key='+MBTA_DEMO_API_KEY+'&lat='+str(latitude)+'&lon='+str(longitude)+'&format=json'
    json = get_json(url)
    station_name = json[u'stop'][0][u'stop_name']
    distance = json[u'stop'][0][u'distance']
    return (station_name, distance)



def find_stop_near(place_name):
    """
    Given a place name or address, print the nearest MBTA stop and the 
    distance from the given place to that stop.
    """
    coordinate = get_lat_long(place_name)
    near_station = get_nearest_station(coordinate[0], coordinate[1])
    print "The nearest MBTA stop from " + str(place_name) + " is " + str(near_station[0]) + " and distance is " + str(near_station[1])

find_stop_near("Fenway Park")