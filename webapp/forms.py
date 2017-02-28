from django import forms
from models import *


class TournamentForm(forms.ModelForm):
	class Meta:
		model = Tournament
		exclude = ['tournament_id', 'teams']


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		exclude = ['user', 'lol_mmr', 'username', 'date_joined']
