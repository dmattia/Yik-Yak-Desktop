from django.db import models
from django.contrib import admin
from django import forms

class userForm(forms.Form):
	latitude = forms.FloatField(required = False)
	longitude = forms.FloatField(required = False)
	userID = forms.CharField(max_length = 50, required = False)	

class searchForm(forms.Form):
	searchText = forms.CharField(max_length=100, required = False)
