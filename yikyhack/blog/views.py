from django.shortcuts import render
import API as pk
import pygeocoder
import requests
import random

def setup(lat=41.7055716, longt=-86.2353388):
	geocoder = pygeocoder.Geocoder("AIzaSyAGeW6l17ATMZiNTRExwvfa2iuPA1DvJqM")

	# Location Setup
	#currentlatitude = 41.7055716
	# currentlongitude = -86.2353388
	coordlocation = pk.Location(lat, longt)

	# User Setup
	remoteyakker = pk.Yakker("842E2854-0147-472A-A146-EC1D5C9EB572", coordlocation, False)

	return remoteyakker 

# Create your views here.
def index(request):
	yakker = setup()
	p = request.POST
	if p.has_key("latitude") and p.has_key("longtitude"):
		lat = float(p["latitude"])
		longt = float(p["longtitude"])
		yakker = setup(lat, longt)
	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': yakker.get_yaks
	}
	return render(request, 'yaksNoComments.html', params)

def top(request):
	yakker = setup()
	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': yakker.get_area_tops
	}
	return render(request, 'yaksNoComments.html', params)

def myTopYaks(request):
	yakker = setup()
	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': yakker.get_my_tops
	}
	return render(request, 'yaksNoComments.html', params)

def myYaks(request):
	yakker = setup()
	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': yakker.get_my_recent_yaks
	}
	return render(request, 'yaksNoComments.html', params)

def viewYak(request, yakNum):
	# find the yak cooresponding to yakNum
	yakker = setup()
	allYaks = yakker.get_yaks() + yakker.get_area_tops() + yakker.get_my_tops()
	desiredID = 'R/' + yakNum
	for yak in allYaks:
		if(yak.message_id == desiredID):
			return render(request, 'yak.html', {'yak': yak})	
	return render(request, 'yakNotFound.html');
