from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from lxml import html
from forms import *
import requests
from webapp.models import *
from django.core.exceptions import *
import pytz

# Create your views here.

def text_to_mmr(text):
    return {
        'Bronze': 1000,
        'Silver': 1300,
		'Gold': 1650,
		'Platinum': 2000,
		'Diamond': 2300,
		'Master': 2700,
		'Challenger': 2900
    }[text]

def get_mmr(user_name):
	print "Getting MMR for: "+user_name
	page = requests.get('https://na.op.gg/summoner/ajax/mmr/summonerName=' + user_name)
	tree = html.fromstring(page.content)

	mmr = str(tree.xpath('//td[@class="MMR"]/text()'))
	if not mmr == '[]':
		try:
			for ch in ['\\n', '\\t', '[', ']', '\'', ',']:
				mmr = mmr.replace(ch, '')
			print("MMR is "+str(mmr)+" for summoner "+user_name)
			return int(mmr)
		except Exception, e:
			print str(e)
			return -1
	else:
		page2 = requests.get('https://na.op.gg/summoner/userName=' + user_name)
		tree2 = html.fromstring(page2.content)
		lastMMR = tree2.xpath('//div[@class="PastRank"]/ul/li/text()')
		level = str(tree2.xpath('//div[@class="ProfileIcon"]/span/text()'))
		if int(level) == 30:
			if len(lastMMR) > 0:
				lastMMR = str(lastMMR[-1]).replace(' ','')
			else:
				print ("MMR is 1150. Player has not ranked yet")
				return 1150
		else:
			print("MMR is 950. Player has not reached level 30")
			return 950
		final_mmr = text_to_mmr(lastMMR)
		print("MMR is "+str(final_mmr)+" for summoner "+user_name)
		return final_mmr


def new_tournament_view(request):
	context = dict()
	print('New Tournament View\n')

	if 'submit_tournament' in request.POST:
		print ("Submitted new tournament\nPost:\n" + str(request.POST))
		form = TournamentForm(request.POST)

		if form.is_valid():
			saved = form.save()
			print ('\nSaved: ' + str(saved.tournament_name))
	elif 'submit_key' in request.POST:
		form = TournamentForm()
		try:
			submitted_tournament_id = request.POST.get('tournament_id')
			tournament = None
			tournament = Tournament.objects.get(id=int(request.POST.get('tournament_id')))

			if tournament.tournament_key == str(request.POST.get('tournament_key')):
				tournament.players.add(UserProfile.objects.get(user=request.user))
				context['tournament_notification'] = 'You have registered for the tournament: ' + str(tournament)
			else:
				context['tournament_notification'] = 'Wrong tournament ID or notification'
			print tournament.id
		except ObjectDoesNotExist:
			print "ObjectDoesNotExist"
			context['tournament_notification'] = 'The Tournament you were looking for is not found: ' + request.POST.get('tournament_key')
			pass
		except Exception, e:
			context['tournament_notification'] = 'Tournament ID is a number. Please try again'
			print e
			pass
	else:
		form = TournamentForm()

	tournaments = Tournament.objects.all()
	context['tournaments'] = tournaments
	context['form'] = form

	return render(request, 'tournament.html', context)


def tournament_detail_view(request, tournament_id):
	print 'Tournament Detail View\nTournament id: ' + tournament_id
	tournament = get_object_or_404(Tournament, id=int(tournament_id))
	return render(request, 'tournament_detail.html', {'tournament':tournament})


def user_profile_view(request):
	print 'User pofile view'
	context = dict()
	instance = get_object_or_404(UserProfile, user=request.user)

	if request.POST:
		print 'POST Submitted: ' + str(request.POST)
		form = UserProfileForm(request.POST or None, instance=instance)
		if form.is_valid():
			saved = form.save(commit = False)
			saved.user = request.user
			saved.lol_mmr = get_mmr(saved.lol_summoner_name)
			saved.save()
	else:
		form = UserProfileForm(instance=instance)

	tournaments = Tournament.objects.filter(players=instance)

	profile = get_object_or_404(UserProfile, user=request.user)
	context['form']=form
	context['tournaments']=tournaments
	context['profile']=profile
	return render(request, 'my_profile.html', context)
