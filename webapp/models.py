from __future__ import unicode_literals
from datetime import datetime
from django.contrib.auth.models import User
import time
from registration.signals import user_registered

from django.db import models

# Create your models here.

def user_created(sender, user, request, **kwargs):
    user.first_name=request.POST.get('first_name')
    user.last_name=request.POST.get('last_name')
    user.save()

user_registered.connect(user_created)


class UserProfile(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    lol_mmr = models.IntegerField(default=0)
    lol_mmr_last_updated = models.BigIntegerField(default=time.time())
    lol_summoner_name = models.CharField(max_length=255, blank=True, null=True)
    primary_role = models.IntegerField(default=0)
    secondary_role = models.IntegerField(default=0)

    def __str__(self):
        return self.lol_summoner_name or "No User Profile"

    def _get_primary_role(self):
            return {
                0: 'Fill',
                1: 'Top',
                2: 'Jungle',
                3: 'Mid',
                4: 'Bottom',
                5: 'Support',
            }[self.primary_role]

    def _get_secondary_role(self):
            return {
                0: 'Fill',
                1: 'Top',
                2: 'Jungle',
                3: 'Mid',
                4: 'Bottom',
                5: 'Support',
            }[self.secondary_role]

    primary_role_name = property(_get_primary_role)
    secondary_role_name = property(_get_secondary_role)


class Tournament(models.Model):
    teams_created = models.BooleanField(default=False)
    main_user = models.ForeignKey(User,null=True, blank=True, related_name="main_user")
    tournament_name = models.CharField(max_length=255, blank=True, null=True)
    players = models.ManyToManyField('UserProfile',blank=True, related_name="tournament_players")
    deadline = models.DateTimeField(auto_now_add=True, blank=True)
    tournament_key = models.CharField(max_length=255, blank=True, null=True)
    teams = models.ManyToManyField('Team', blank=True, related_name="tournament_teams")
    bracket_json = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.tournament_name

    def _get_number_of_teams(self):
        counter = 0
        for item in self.teams.all():
            counter += 1
        return counter

    number_of_teams = property(_get_number_of_teams)


class Team(models.Model):
    members = models.ManyToManyField('UserProfile')
    team_name = models.CharField(max_length=255, blank=True, null=True)
    ranking = models.IntegerField(default=0)

    def __str__(self):
        return self.team_name
