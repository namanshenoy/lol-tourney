from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from forms import *
from lxml import html
import requests
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


def index(request):
	context = {}
	if request.POST:
		form = TournamentForm(request.POST)
		if form.is_valid():
			saved = form.save()
			context['team_name'] = saved.title
			context['form'] = form
			context['registered'] = True
		return render(request, 'index.html', context=context)
	else:
		if request.user.is_authenticated():
			try:
				context['user_profile'] = UserProfile.objects.get(user=request.user)
			except Exception, e:
				print str(e)
			finally:
				context['user_profile'] = None

		form = TournamentForm()
		return render(request, 'index.html', {'form': form, })


@login_required
def settings(request):
	context = {}
	if request.POST:
		form = UserProfileForm(request.POST)
		if form.is_valid():
			saved = form.save(commit=False)
			user_profile = UserProfile.objects.get_or_create(user=request.user)
			user_profile.user = request.user
			mmr = get_mmr(saved.lol_summoner_name)
			print mmr
			if mmr < 0:
				context['form'] = form
				context['summoner_not_found'] = True
				return render(request, 'settings.html', context=context)
			user_profile.lol_mmr = mmr
			user_profile.date_joined = pytz.utc.localize(datetime.now())
			user_profile.save()
			return HttpResponseRedirect('/')
	if UserProfile.objects.exists(user=request.user):
		form = UserProfileForm(instance=UserProfile.objects.get(user=request.user))
	else:
		form = UserProfileForm()
	context['form'] = form
	return render(request, 'settings.html', context=context)
