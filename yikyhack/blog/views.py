from django.contrib.auth.decorators import login_required
from models import userForm, searchForm
from django.http import HttpResponse
from django.shortcuts import render
import pygeocoder
import API as pk
import requests
import random

def loadFromSession(session):
	if 'latitude' in session:
		lat = session['latitude']
	else:
		lat = 41.7055716
		session['latitude'] = lat
	if 'longitude' in session:
		longt = session['longitude']
	else:
		longt = -86.2353388
		session['longitude'] = longt
	if 'userID' in session and len(session['userID']) > 1:
		userID = session['userID']
	else:
		userID = '70FB6DD23A2147CBC544154DAE8564D9'
		session['userID'] = userID
	return lat, longt, userID, session
	

def setup(request):
	#geocoder = pygeocoder.Geocoder("AIzaSyAGeW6l17ATMZiNTRExwvfa2iuPA1DvJqM")

	if request.method == 'POST':
		p = request.POST
		locationAndIdForm = userForm(p)
		search = searchForm(p)
		if 'userSubmit' in p:
			if locationAndIdForm.is_valid():
				if locationAndIdForm['latitude'] is not None and locationAndIdForm['longitude'] is not None:
					lat = locationAndIdForm.cleaned_data["latitude"] 
					request.session['latitude'] = lat
					longt = locationAndIdForm.cleaned_data["longitude"]
					request.session['longitude'] = longt
				if locationAndIdForm['userID'] is not None:
					userID = locationAndIdForm.cleaned_data['userID']
					request.session['userID'] = userID
		if 'searchSubmit' in p:
			if search.is_valid():
				searchTerm = search.cleaned_data['searchText']
				if len(searchTerm == 0): searchTerm = False
		else:
			searchTerm = False
		if "upvote" in p:
			lat, longt, userID, request.session = loadFromSession(request.session)
			coordlocation = pk.Location(lat, longt)
			remoteyakker = pk.Yakker(userID, coordlocation, False)
			remoteyakker.upvote_yak(p["upvote"])
		if "downvote" in p:
			lat, longt, userID, request.session = loadFromSession(request.session)
			coordlocation = pk.Location(lat, longt)
			remoteyakker = pk.Yakker(userID, coordlocation, False)
			remoteyakker.downvote_yak(p["downvote"])
	else:
		searchTerm = False
		locationAndIdForm = userForm()
		search = searchForm()

	lat, longt, userID, request.session = loadFromSession(request.session)
	coordlocation = pk.Location(lat, longt)
	remoteyakker = pk.Yakker(userID, coordlocation, False)

	return remoteyakker, searchTerm, locationAndIdForm, search

@login_required
def search(request):
	yakker, searchTerm, locationAndIdForm, search = setup(request)
	matchingYaks = set([])
	yaks = yakker.get_yaks() + yakker.get_area_tops() + yakker.get_my_tops()
	for yak in yaks:
		if(searchTerm.lower() in yak.message.lower()):
			matchingYaks.add(yak) 

	params = {
		'searchForm': search,
		'form': locationAndIdForm,
		'yakarma': yakker.get_yakarma,
		'yakList': matchingYaks,
		'yakCount': len(matchingYaks)
	}
	return render(request, 'yaksNoComments.html', params)

@login_required
def index(request):
	yakker, searchTerm, locationAndIdForm, search = setup(request)
	yaks = yakker.get_yaks()
	searchedYaks = []
	if searchTerm:
		for yak in yaks:
			if(searchTerm.lower() in yak.message.lower()):
				searchedYaks.append(yak) 
	else:
		searchedYaks = yaks
	
	params = {
		'searchForm': search,
		'form': locationAndIdForm,
		'yakarma': yakker.get_yakarma,
		'yakList': searchedYaks,
		'yakCount': len(searchedYaks)+1 if searchTerm else len(searchedYaks)
	}
	return render(request, 'yaksNoComments.html', params)

@login_required
def top(request):
	yakker, searchTerm, locationAndIdForm, search = setup(request)
	yaks = yakker.get_area_tops()
	searchedYaks = []
	if searchTerm:
		for yak in yaks:
			if(searchTerm.lower() in yak.message.lower()):
				searchedYaks.append(yak) 
	else:
		searchedYaks = yaks

	params = {
		'searchForm': search,
		'form': locationAndIdForm,
		'yakarma': yakker.get_yakarma,
		'yakList': searchedYaks,
		'yakCount': len(searchedYaks)+1 if searchTerm else len(searchedYaks)
	}
	return render(request, 'yaksNoComments.html', params)

@login_required
def myTopYaks(request):
	yakker, searchTerm, locationAndIdForm, search = setup(request)
	yaks = yakker.get_my_tops()
	searchedYaks = []
	if searchTerm:
		for yak in yaks:
			if(searchTerm.lower() in yak.message.lower()):
				searchedYaks.append(yak) 
	else:
		searchedYaks = yaks

	params = {
		'searchForm': search,
		'form': locationAndIdForm,
		'yakarma': yakker.get_yakarma,
		'yakList': searchedYaks,
		'yakCount': len(searchedYaks)+1 if searchTerm else len(searchedYaks)
	}
	return render(request, 'yaksNoComments.html', params)

@login_required
def myYaks(request):
	yakker, searchTerm, locationAndIdForm, search = setup(request)
	yaks = yakker.get_my_recent_yaks()
	searchedYaks = []
	if searchTerm:
		for yak in yaks:
			if(searchTerm.lower() in yak.message.lower()):
				searchedYaks.append(yak) 
	else:
		searchedYaks = yaks

	params = {
		'searchForm': search,
		'form': locationAndIdForm,
		'yakarma': yakker.get_yakarma,
		'yakList': searchedYaks,
		'yakCount': len(searchedYaks)+1 if searchTerm else len(searchedYaks)
	}
	return render(request, 'yaksNoComments.html', params)

def findYak(request, yakID):
	yakker, searchTerm, locationAndIdForm, search = setup(request)
	yaks = yakker.get_yaks() + yakker.get_area_tops() + yakker.get_my_tops()
	for yak in yaks:
		if(yak.message_id == yakID):
			return yak
	return False
	

@login_required
def viewYak(request, yakNum):
	# find the yak cooresponding to yakNum
	yak = findYak(request, 'R/' + yakNum)
	if yak:
		return render(request, 'yak.html', {'yak': yak})	
	return render(request, 'yakNotFound.html');
