from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class UserProfile(User):
	user = models.OneToOneField(User)
	userID = models.CharField(max_length=50)
	latitude = models.FloatField()
	longitude = models.FloatField()
	login_count = models.IntegerField()

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

admin.site.register(UserProfile)
