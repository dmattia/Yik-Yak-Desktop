from django.db import models
from django.contrib.auth.models import User

#class UserProfile(models.Model):
class UserProfile(User):
	user = models.OneToOneField(User)
	userID = models.CharField(max_length=50)
	latitude = models.FloatField()
	longitude = models.FloatField()

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
