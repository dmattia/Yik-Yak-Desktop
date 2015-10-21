from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from forms import UserProfileForm
from userprofile.models import UserProfile
from django.contrib.auth.decorators import login_required
from blog import pygeocoder

@login_required
def user_profile(request):
	if request.method == 'POST':
		form = UserProfileForm(request.POST)
		if form.is_valid():
			currentUser = UserProfile.objects.get(user_id=request.user.id)
			currentUser.userID = form.cleaned_data['userID']
			location = form.cleaned_data['location']
			pyLocation = pygeocoder.Geocoder.geocode(location)
			currentUser.latitude = pyLocation.latitude
			currentUser.longitude = pyLocation.longitude
			currentUser.save()
			return HttpResponseRedirect('/accounts/loggedin/')
	else:
		user = request.user
		profile = user.profile
		form = UserProfileForm()	

	args = {}
	args.update(csrf(request))
	args['userForm'] = form
	args['user'] = request.user
	args['showSearch'] = False
	args['active'] = 'update'
	return render_to_response('profile.html', args)
