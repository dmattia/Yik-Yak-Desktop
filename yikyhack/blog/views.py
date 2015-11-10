from django.contrib.auth.decorators import login_required
from userprofile.models import UserProfile
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.gis.geoip import GeoIP
from ipware.ip import get_ip
from django.shortcuts import render
from models import searchForm
import API as pk
import requests
import random

def setup(request):
	currentUser = UserProfile.objects.get(user_id=request.user.id)
	lat = currentUser.latitude
	longt = currentUser.longitude
	userID = currentUser.userID
	isGuestUser = False
	if currentUser.username == 'guest':
		isGuestUser = True

	# Find user location
	userIP = get_ip(request)
	g = GeoIP()
	if userIP is not None and g.lat_lon(userIP):
		userLatitude, userLongitude = g.lat_lon(userIP)
		foundIP = True
	else:
		userLatitude = lat
		userLongitude = longt
		foundIP = False

	if request.method == 'POST':
		p = request.POST
		search = searchForm(p)
		if 'searchSubmit' in p:
			if search.is_valid():
				searchTerm = search.cleaned_data['searchText']
			else:
				searchTerm = False
		else:
			searchTerm = False
		if "upvote" in p:
			coordlocation = pk.Location(lat, longt)
			remoteyakker = pk.Yakker(userID, coordlocation, False)
			if p["upvote-type"] == 'yak':
				remoteyakker.upvote_yak(p["upvote"])
			else:
				remoteyakker.upvote_comment(p["upvote"])
		if "downvote" in p:
			coordlocation = pk.Location(lat, longt)
			remoteyakker = pk.Yakker(userID, coordlocation, False)
			if p["upvote-type"] == 'yak':
				remoteyakker.downvote_yak(p["downvote"])
			else:
				remoteyakker.downvote_comment(p["downvote"])
	else:
		search = searchForm()
		searchTerm = False

	coordlocation = pk.Location(lat, longt)
	remoteyakker = pk.Yakker(userID, coordlocation, False)

	return remoteyakker, searchTerm, search, userLatitude, userLongitude, foundIP, isGuestUser

@login_required
def upvote(request, yakID, upvote_kind):
	yakker, temp, search, latitude, longitude, ip, isGuestUser = setup(request)
	if upvote_kind == 'yak':
		yakker.upvote_yak('R/' + yakID)
	else:
		yakker.upvote_comment('R/' + yakID)
	return HttpResponse("Hello")

@login_required
def downvote(request, yakID, downvote_kind):
	yakker, temp, search, latitude, longitude, ip, isGuestUser = setup(request)
	if downvote_kind == 'yak':
		yakker.downvote_yak('R/' + yakID)
	else:
		yakker.downvote_comment('R/' + yakID)
	return HttpResponse("Hello")

@login_required
def search(request, searchTerm):
	yakker, temp, search, latitude, longitude, ip, isGuestUser = setup(request)
	matchingYaks = set([])
	yaks = yakker.get_yaks() + yakker.get_area_tops() + yakker.get_my_tops()
	for yak in yaks:
		if(searchTerm.lower() in yak.message.lower()):
			matchingYaks.add(yak) 

	params = {
		'showSearch': True,
		'active': 'search',
		'searchForm': search,
		'yakarma': yakker.get_yakarma,
		'yakList': matchingYaks,
		'yakCount': len(matchingYaks)
	}
	return render(request, 'yaksNoComments.html', params)

@login_required
def index(request):
	yakker, searchTerm, search, latitude, longitude, ip, isGuestUser = setup(request)
	yaks = yakker.get_yaks()
	searchedYaks = []
	if searchTerm:
		for yak in yaks:
			if(searchTerm.lower() in yak.message.lower()):
				searchedYaks.append(yak) 
	else:
		searchedYaks = yaks
	
	params = {
		'showSearch': True,
		'active': 'recent',
		'searchForm': search,
		'yakarma': yakker.get_yakarma,
		'yakList': searchedYaks,
		'yakCount': len(searchedYaks)+1 if searchTerm else len(searchedYaks),
		'locations': yakker.get_featured_locations,
		'latitude': latitude,
		'longitude': longitude,
		'ip': ip,
		'isGuestUser': isGuestUser,
	}
	return render(request, 'yaksNoComments.html', params)

@login_required
def top(request):
	yakker, searchTerm, search, latitude, longitude, ip, isGuestUser = setup(request)
	yaks = yakker.get_area_tops()
	searchedYaks = []
	if searchTerm:
		for yak in yaks:
			if(searchTerm.lower() in yak.message.lower()):
				searchedYaks.append(yak) 
	else:
		searchedYaks = yaks

	params = {
		'showSearch': True,
		'active': 'top',
		'searchForm': search,
		'yakarma': yakker.get_yakarma,
		'yakList': searchedYaks,
		'locations': yakker.get_featured_locations,
		'yakCount': len(searchedYaks)+1 if searchTerm else len(searchedYaks),
		'latitude': latitude,
		'longitude': longitude,
		'ip': ip,
		'isGuestUser': isGuestUser,
	}
	return render(request, 'yaksNoComments.html', params)

@login_required
def myTopYaks(request):
	yakker, searchTerm, search, latitude, longitude, ip, isGuestUser = setup(request)
	yaks = yakker.get_my_tops()
	searchedYaks = []
	if searchTerm:
		for yak in yaks:
			if(searchTerm.lower() in yak.message.lower()):
				searchedYaks.append(yak) 
	else:
		searchedYaks = yaks

	params = {
		'showSearch': True,
		'active': 'myTop',
		'searchForm': search,
		'yakarma': yakker.get_yakarma,
		'yakList': searchedYaks,
		'locations': yakker.get_featured_locations,
		'yakCount': len(searchedYaks)+1 if searchTerm else len(searchedYaks),
		'latitude': latitude,
		'longitude': longitude,
		'ip': ip,
		'isGuestUser': isGuestUser,
	}
	return render(request, 'yaksNoComments.html', params)

@login_required
def myYaks(request):
	yakker, searchTerm, search, latitude, longitude, ip, isGuestUser = setup(request)
	yaks = yakker.get_my_recent_yaks()
	searchedYaks = []
	if searchTerm:
		for yak in yaks:
			if(searchTerm.lower() in yak.message.lower()):
				searchedYaks.append(yak) 
	else:
		searchedYaks = yaks

	params = {
		'showSearch': True,
		'active': 'myYaks',
		'searchForm': search,
		'yakarma': yakker.get_yakarma,
		'yakList': searchedYaks,
		'locations': yakker.get_featured_locations,
		'yakCount': len(searchedYaks)+1 if searchTerm else len(searchedYaks),
		'latitude': latitude,
		'longitude': longitude,
		'ip': ip,
		'isGuestUser': isGuestUser,
	}
	return render(request, 'yaksNoComments.html', params)

def findYak(request, yakID):
	yakker, searchTerm, search, latitude, longitude, ip, isGuestUser = setup(request)
	yaks = yakker.get_yaks() + yakker.get_area_tops() + yakker.get_my_tops()
	for yak in yaks:
		if(yak.message_id == yakID):
			return yak
	return False
	

@login_required
def viewYak(request, yakNum):
	# find the yak cooresponding to yakNum
	setup(request)
	yak = findYak(request, 'R/' + yakNum)
	yakker, searchTerm, search, latitude, longitude, ip, isGuestUser = setup(request)
	if yak:
		return render(request, 'yak.html', {'yak': yak, 'yakarma': yakker.get_yakarma, 'isGuestUser': isGuestUser})	
	return render(request, 'yakNotFound.html');

def changeLocation(request, latitude, longitude):
	currentUser = UserProfile.objects.get(user_id=request.user.id)
	currentUser.latitude = latitude
	currentUser.longitude = longitude
	currentUser.save()
	return HttpResponseRedirect('/accounts/blog/yaks/')
