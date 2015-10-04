from registration.backends.default.views import RegistrationView
from forms import UserProfileRegistrationForm
from models import UserProfile
from registration.forms import RegistrationFormUniqueEmail

class MyRegistrationView(RegistrationView):
	form_class = UserProfileRegistrationForm
	
	def register(self, request, form_class):
		new_user = super(MyRegistrationView, self).register(request, form_class)
		user_profile.user = new_user
		user_profile.save()
