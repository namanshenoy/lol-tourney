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


def get_mmr(user_name):
	print user_name
	page = requests.get('https://na.op.gg/summoner/ajax/mmr/summonerName=' + user_name)
	tree = html.fromstring(page.content)
	mmr = str(tree.xpath('//td[@class="MMR"]/text()'))
	if not mmr == '[]':
		try:
			print mmr
			for ch in ['\\n', '\\t', '[', ']', '\'', ',']:
				mmr = mmr.replace(ch, '')
			return int(mmr)
		except Exception, e:
			print str(e)
			return -2
	else:
		return -1


def new_tournament_view(request):
	context = dict()
	print('New Tournament View\n')

	if 'submit_tournament' in request.POST:
		print request.POST
		form = TournamentForm(request.POST)

		if form.is_valid():
			saved = form.save()
			print ('\nSaved: ' + str(saved.tournament_name))
	elif 'submit_key' in request.POST:
		print request.POST
		form = TournamentForm()
		try:
			tournament = Tournament.objects.get(id=int(request.POST.get('tournament_id')))
			print tournament.tournament_key
			if tournament.tournament_key == str(request.POST.get('tournament_key')):
				tournament.players.add(UserProfile.objects.get(user=request.user))
			else:
				context['tournament_notification'] = 'Wrong tournament ID or notification'
			print tournament.id
		except ObjectDoesNotExist:
			print "ObjectDoesNotExist"
			context['tournament_notification'] = 'The Tournament you were looking for is not found: ' + request.POST.get('tournament_key')
			pass
	else:
		form = TournamentForm()

	tournaments = Tournament.objects.all()
	context['tournaments'] = tournaments
	context['form'] = form

	return render(request, 'tournament.html', context)


def tournament_detail_view(request, tournament_id):
	print 'Tournament id: ' + tournament_id
	tournament = get_object_or_404(Tournament, id=int(tournament_id))
	return render(request, 'tournament_detail.html', {'tournament':tournament})


def user_profile_view(request):
	print('User Profile View\n')
	instance = get_object_or_404(UserProfile, user=request.user)

	if request.POST:
		print request.POST
		form = UserProfileForm(request.POST or None, instance=instance)
		if form.is_valid():
			saved = form.save(commit = False)
			saved.user = request.user
			saved.save()
	else:
		form = UserProfileForm(instance=instance)
	profile = get_object_or_404(UserProfile, user=request.user)
	return render(request, 'my_profile.html', {'form': form, 'profile': profile})
