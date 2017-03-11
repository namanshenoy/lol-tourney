from models import *
from django.forms import ModelForm
import webapp.models

class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['tournament_name', 'tournament_key', ]

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['lol_summoner_name', ]
