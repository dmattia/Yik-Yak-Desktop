from django import forms
#from django.contrib.auth.models import User
from userprofile.models import UserProfile
from django.contrib.auth.forms import UserCreationForm

class YakUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	latitude = forms.FloatField(required=True)
	longitude = forms.FloatField(required=True)
	userID = forms.CharField(max_length=36,min_length=36,required=True)

	class Meta:
		model = UserProfile
		fields = ('username', 'latitude', 'longitude', 'userID', 'email','password1', 'password2')

	def save(self, commit=True):
		user = super(YakUserCreationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.latitude = self.cleaned_data['latitude']
		user.longitude = self.cleaned_data['longitude']
		user.userID = self.cleaned_data['userID']
		if commit:
			user.save()
		return user
