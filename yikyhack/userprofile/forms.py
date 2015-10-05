from django import forms
from django.forms import ModelForm
from models import UserProfile

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('userID',)
