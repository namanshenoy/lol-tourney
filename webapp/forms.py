from django import forms
from models import *


class TournamentForm(forms.ModelForm):
	class Meta:
		model = Tournament
		exclude = ['tournament_id', 'teams']
