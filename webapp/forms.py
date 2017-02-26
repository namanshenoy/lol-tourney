from django import forms
from models import *

class TournamentForm(forms.ModelForm):
  class Meta:
    model = Tournament
    exclude = ['teams']