from django.shortcuts import render
import API as pk
import pygeocoder
import requests
import random

def setup():
	geocoder = pygeocoder.Geocoder("AIzaSyAGeW6l17ATMZiNTRExwvfa2iuPA1DvJqM")

	# Location Setup
	currentlatitude = 41.7055716
	currentlongitude = -86.2353388
	coordlocation = pk.Location(currentlatitude, currentlongitude)

	# User Setup
	remoteyakker = pk.Yakker("842E2854-0147-472A-A146-EC1D5C9EB572", coordlocation, False)

	return remoteyakker 

# Create your views here.
def index(request):
	yakker = setup()
	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': yakker.get_yaks
	}
	return render(request, 'yakList.html', params)

def top(request):
	yakker = setup()
	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': yakker.get_area_tops
	}
	return render(request, 'yakList.html', params)

def myTopYaks(request):
	yakker = setup()
	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': yakker.get_my_tops
	}
	return render(request, 'yakList.html', params)

def myYaks(request):
	yakker = setup()
	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': yakker.get_my_recent_yaks
	}
	return render(request, 'yakList.html', params)
