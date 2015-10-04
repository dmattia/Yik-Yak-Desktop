from django.db import models
from django.contrib import admin

class UserProfile(models.Model):
	latitude = models.FloatField()
	longitude = models.FloatField()
	userID = models.CharField(max_length=255)

admin.site.register(UserProfile)
