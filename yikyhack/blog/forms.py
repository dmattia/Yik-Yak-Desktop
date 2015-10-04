from registration.forms import RegistrationFormUniqueEmail  
from django import forms

class UserProfileRegistrationForm(RegistrationFormUniqueEmail):   
	userID = forms.CharField()

class InviteForm(forms.Form):
	invite_email = forms.EmailField(max_length=128, help_text="sending invitation to the email address")  
