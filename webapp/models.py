from __future__ import unicode_literals
from datetime import datetime
from django.contrib.auth.models import User

from django.db import models

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    lol_summoner_name = models.CharField(max_length=128, null=True, blank=True)
    date_joined = models.DateTimeField(datetime.now())
    username = models.CharField(max_length=128, default=lol_summoner_name)
    lol_mmr = models.IntegerField(null=True, blank=True)

    
class Team(models.Model):
    team_id = models.CharField(max_length=128, null=True, blank=True)
    name = models.CharField(max_length=128, null=True, blank=True)
    players = models.ManyToManyField(UserProfile)
    team_wins = models.IntegerField(null=True, blank=True)
    team_losses = models.IntegerField(null=True, blank=True)


class Tournament(models.Model):
    tournament_id = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    teams = models.ForeignKey(Team, verbose_name='Teams')
