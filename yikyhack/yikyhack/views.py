from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from forms import YakUserCreationForm
from userprofile.models import UserProfile

def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/accounts/loggedin/')
	else:
		return HttpResponseRedirect('/accounts/invalid/')

def loggedin(request):
	user = UserProfile.objects.get(user=request.user)
	user.login_count = user.login_count + 1
	user.save()
	return HttpResponseRedirect('/accounts/blog/yaks/')

def invalid_login(request):
	return render_to_response('invalid_login.html')

def logout(request):
	auth.logout(request)
	return render_to_response('logout.html')

def register_user(request):
	if request.method == 'POST':
		form = YakUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/register_success/')
		else:
			args = {}
			args.update(csrf(request))
			args['registerForm'] = form
			return render_to_response('register.html',args)
	else:
		# first time on register page
		args = {}
		args.update(csrf(request))
		args['registerForm'] = YakUserCreationForm()
		return render_to_response('register.html',args)

def register_success(request):
	return render_to_response('register_success.html')

def register_failure(request):
	return render_to_response('register_failure.html')
