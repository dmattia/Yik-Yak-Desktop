from django import forms
from django.forms import ModelForm
from models import UserProfile

class UserProfileForm(forms.Form):
	userID = forms.CharField(max_length=50)
	location = forms.CharField(max_length=255)

#class UserProfileForm(forms.ModelForm):
	#class Meta:
	#	model = UserProfile
	#	fields = ('userID','latitude','longitude')
