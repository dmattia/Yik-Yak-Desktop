from django.db import models
from django.contrib import admin
from django import forms

class searchForm(forms.Form):
	searchText = forms.CharField(max_length=100, required = False)
