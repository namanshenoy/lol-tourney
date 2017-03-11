from __future__ import unicode_literals
from datetime import datetime
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User)
    lol_mmr = models.IntegerField(default=0)
    lol_summoner_name = models.CharField(max_length=255, blank=True, null=True)
    primary_role = models.IntegerField(default=0)
    secondary_role = models.IntegerField(default=0)


class Tournament(models.Model):
    main_user = models.ForeignKey('UserProfile', related_name="main_user")
    tournament_name = models.CharField(max_length=255, blank=True, null=True)
    players = models.ManyToManyField('UserProfile', related_name="tournament_players")
    deadline = models.DateTimeField(auto_now_add=True, blank=True)
    tournament_key = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return tournament_name

class Team(models.Model):
    tournament = models.ForeignKey('Tournament')
    members = models.ManyToManyField('UserProfile')
    team_name = models.CharField(max_length=255, blank=True, null=True)
    ranking = models.IntegerField(default=0)
