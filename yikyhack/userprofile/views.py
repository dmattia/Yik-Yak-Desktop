from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from forms import UserProfileForm
from userprofile.models import UserProfile
from django.contrib.auth.decorators import login_required
from blog import pygeocoder

@login_required
def user_profile(request):
	currentUser = UserProfile.objects.get(user_id=request.user.id)
	if request.method == 'POST':
		form = UserProfileForm(request.POST)
		if form.is_valid():
			if currentUser.userID != '22CC671C-99CC-4DC3-A145-1779E32A05E1':
				currentUser.userID = form.cleaned_data['userID']
			location = form.cleaned_data['location']
			try:
				pyLocation = pygeocoder.Geocoder.geocode(location)
				currentUser.latitude = pyLocation.latitude
				currentUser.longitude = pyLocation.longitude
			except:
				pass
			currentUser.save()
			return HttpResponseRedirect('/accounts/loggedin/')
	else:
		user = request.user
		profile = user.profile
		try:
			locationStr = pygeocoder.Geocoder.reverse_geocode(currentUser.latitude,currentUser.longitude)
		except:
			locationStr = ""
		if user.username != 'guest':
			userID = currentUser.userID
		else:
			userID = "guest"
		initialValues = {
			'userID': userID,
			'location': locationStr
		}
		form = UserProfileForm(initial=initialValues)	

	args = {}
	args.update(csrf(request))
	args['userForm'] = form
	args['user'] = request.user
	args['showSearch'] = False
	args['active'] = 'update'
	return render_to_response('profile.html', args)
