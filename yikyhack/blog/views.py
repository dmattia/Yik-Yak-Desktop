from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
import API as pk
import pygeocoder
import requests
import random

def setup(request):
	geocoder = pygeocoder.Geocoder("AIzaSyAGeW6l17ATMZiNTRExwvfa2iuPA1DvJqM")

	p = request.POST
	try:
		lat = float(p["latitude"]) 
		longt = float(p["longitude"])
		request.session['latitude'] = lat
		request.session['longitude'] = longt
	except:
		if 'latitude' in request.session:
			lat = request.session['latitude']
		else:
			lat = 41.7055716
		if 'longitude' in request.session:
			longt = request.session['longitude']
		else:
			longt = -86.2353388
	if p.has_key("userID"):
		userID = p["userID"]
		request.session['userID'] = userID
	else:
		if 'userID' in request.session:
			userID = request.session['userID']
		else:
			userID = "random"

	# Location Setup
	coordlocation = pk.Location(lat, longt)

	# User Setup
	remoteyakker = pk.Yakker(userID, coordlocation, False)

	return remoteyakker 

def index(request):
	yakker = setup(request)
	yaks = yakker.get_yaks()
	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': yaks,
		'yakCount': len(yaks)
	}
	return render(request, 'yaksNoComments.html', params)

def top(request):
	yakker = setup(request)
	yaks = yakker.get_area_tops()
	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': yaks,
		'yakCount': len(yaks)
	}
	return render(request, 'yaksNoComments.html', params)

def myTopYaks(request):
	yakker = setup(request)
	yaks = yakker.get_my_tops()
	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': yaks,
		'yakCount': len(yaks)
	}
	return render(request, 'yaksNoComments.html', params)

def myYaks(request):
	yakker = setup(request)
	yaks = yakker.get_my_recent_yaks()
	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': yaks,
		'yakCount': len(yaks)
	}
	return render(request, 'yaksNoComments.html', params)

def findYak(yakID):
	yakker = setup(request)
	allYaks = yakker.get_yaks() + yakker.get_area_tops() + yakker.get_my_tops()
	for yak in allYaks:
		if(yak.message_id == yakID):
			return yak
	return False
	

def viewYak(request, yakNum):
	# find the yak cooresponding to yakNum
	desiredID = 'R/' + yakNum
	yak = findYak(desiredID)
	if yak:
		return render(request, 'yak.html', {'yak': yak})	
	return render(request, 'yakNotFound.html');
