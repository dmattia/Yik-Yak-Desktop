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
	return render(request, 'index.html', {'yakker': setup()})

def top(request):
	return render(request, 'tops.html', {'yakker': setup()})
