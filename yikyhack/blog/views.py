from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
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

	searchTerm = False
	if request.method == 'POST':
		if "upvote" in request.POST:
			remoteyakker.upvote_yak(p["upvote"])
		if "searchTerm" in request.POST:
			searchTerm = p["searchTerm"]

	return remoteyakker, searchTerm 

def search(request):
	yakker, searchTerm = setup(request)
	matchingYaks = set([])
	yaks = yakker.get_yaks() + yakker.get_area_tops() + yakker.get_my_tops()
	for yak in yaks:
		if(searchTerm in yak.message):
			matchingYaks.add(yak) 

	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': matchingYaks,
		'yakCount': len(matchingYaks)
	}
	return render(request, 'yaksNoComments.html', params)

def index(request):
	yakker, searchTerm = setup(request)
	yaks = yakker.get_yaks()
	searchedYaks = []
	if searchTerm:
		for yak in yaks:
			if(searchTerm in yak.message):
				searchedYaks.append(yak) 
	else:
		searchedYaks = yaks
	
	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': searchedYaks,
		'yakCount': len(searchedYaks)
	}
	return render(request, 'yaksNoComments.html', params)

def top(request):
	yakker, searchTerm = setup(request)
	yaks = yakker.get_area_tops()
	searchedYaks = []
	if searchTerm:
		for yak in yaks:
			if(searchTerm in yak.message):
				searchedYaks.append(yak) 
	else:
		searchedYaks = yaks

	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': searchedYaks,
		'yakCount': len(searchedYaks)
	}
	return render(request, 'yaksNoComments.html', params)

def myTopYaks(request):
	yakker, searchTerm = setup(request)
	yaks = yakker.get_my_tops()
	searchedYaks = []
	if searchTerm:
		for yak in yaks:
			if(searchTerm in yak.message):
				searchedYaks.append(yak) 
	else:
		searchedYaks = yaks

	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': searchedYaks,
		'yakCount': len(searchedYaks)
	}
	return render(request, 'yaksNoComments.html', params)

def myYaks(request):
	yakker, searchTerm = setup(request)
	yaks = yakker.get_my_recent_yaks()
	searchedYaks = []
	if searchTerm:
		for yak in yaks:
			if(searchTerm in yak.message):
				searchedYaks.append(yak) 
	else:
		searchedYaks = yaks

	params = {
		'yakarma': yakker.get_yakarma,
		'yakList': searchedYaks,
		'yakCount': len(searchedYaks)
	}
	return render(request, 'yaksNoComments.html', params)

def findYak(yakID):
	yakker, searchTerm = setup(request)
	yaks = yakker.get_yaks() + yakker.get_area_tops() + yakker.get_my_tops()
	for yak in yaks:
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
