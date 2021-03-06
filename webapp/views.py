from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from lxml import html
from forms import *
import requests
from webapp.models import *
from django.core.exceptions import *
import pytz
import team_generator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.

def text_to_mmr(text):
    return {
		'Bronze': 1000,
		'Silver': 1150,
		'Gold': 1500,
		'Platinum': 1850,
		'Diamond': 2200,
		'Master': 2700,
		'Challenger': 2900
	}[text]


def get_mmr(user_name):
	user_name=user_name.replace(' ','')
	print "Getting MMR for: "+user_name
	page = requests.get('https://na.op.gg/summoner/ajax/mmr/summonerName=' + user_name)
	tree = html.fromstring(page.content)

	mmr = str(tree.xpath('//td[@class="MMR"]/text()'))
	if not mmr == '[]':
		print "MMR found!"
		try:
			for ch in ['\\n', '\\t', '[', ']', '\'', ',']:
				mmr = mmr.replace(ch, '')
			print("MMR is "+str(mmr)+" for summoner "+user_name)
			return int(mmr)
		except Exception, e:
			print str(e)
			return -1
	else:
		try:
			page2 = requests.get('https://na.op.gg/summoner/userName=' + user_name)
			tree2 = html.fromstring(page2.content)
			lastMMR = tree2.xpath('//div[@class="PastRank"]/ul/li/text()')
			currentRank=str(tree2.xpath('//span[@class="tierRank"]/text()'))
			print currentRank
			for ch in ['\\n', '\\t', '[', ']', '\'', ',']:
				currentRank = currentRank.replace(ch, '')

			if currentRank != 'Unranked':
				print 'Found rank = '+currentRank
				currentRank = currentRank.split()
				if currentRank[0] == 'Bronze':
					mmr = text_to_mmr(currentRank[0]) + 230*(int(currentRank[1]))
				elif currentRank[0] == 'Master':
					mmr = text_to_mmr('Master')
				elif currentRank[0] == 'Challenger':
					mmr = text_to_mmr('Challenger')
				else:
					mmr = text_to_mmr(currentRank[0]) + 70*(int(currentRank[1]))
				print ("MMR calculated : " + str(mmr))
				return mmr

			level = str(tree2.xpath('//div[@class="ProfileIcon"]/span/text()'))
			print level
			for ch in ['\\n', '\\t', '[', ']', '\'', ',']:
				level = level.replace(ch, '')
			if int(level) == 30 or len(lastMMR) > 0:
				if len(lastMMR) > 0:
					lastMMR = str(lastMMR[-1]).replace(' ','')

				else:
					print ("MMR is 1150. Player has not ranked yet")
					return 1150
			elif int(level) < 30:
				print("MMR is 950. Player has not reached level 30")
				return 950
		except Exception, e:
			print str(e)
			print("Player not found")
			return -2
		final_mmr = text_to_mmr(lastMMR)
		print("MMR is "+str(final_mmr)+" for summoner "+user_name)
		return final_mmr

def tournament_create_teams(request, tournament_id):
	try:
		tournament = Tournament.objects.get(id=tournament_id)
		teams = team_generator.make_teams(tournament.players)
		tournament.teams.add(*teams)
		tournament.save()
		return True
	except Exception, e:
		print('Error while Making teams')
		print str(e)
		pass
		return False

def bootstrap_index(request):
	return render(request, 'bootstrap_test/index.html',)

@method_decorator(csrf_exempt, name='dispatch')
def home(request):
	if request.POST:
		submitted = Submitted.objects.create(name=request.POST.get('response_id'))
	contextDict = dict()
	return_survey = Submitted.objects.all()
	contextDict['return_survey'] = return_survey
	return render(request, 'home.html', context=contextDict)

def new_tournament_view(request):
	context = dict()
	print('New Tournament View\n')

	if 'submit_tournament' in request.POST:
		print ("Submitted new tournament\nPost:\n" + str(request.POST))

		form = TournamentForm(request.POST)

		if form.is_valid():
			saved = form.save(commit=False)
			saved.main_user = request.user
			saved.save()
			print ('\nSaved: ' + str(saved.tournament_name))
	elif 'submit_key' in request.POST:
		form = TournamentForm()
		try:
			try:
				user_profile = UserProfile.objects.get(user=request.user)
			except ObjectDoesNotExist:
				raise ValueError
				pass
			submitted_tournament_id = request.POST.get('tournament_id')
			tournament = None
			try:
				tournament = Tournament.objects.get(id=int(request.POST.get('tournament_id')))
			except ValueError:
				print "Wrong tournament"
				context['tournament_notification'] = 'Please enter a correct tournament number'
				pass

			if user_profile.lol_mmr == None or user_profile.lol_mmr == 0:
				raise ValueError
			if tournament.tournament_key == str(request.POST.get('tournament_key')):
				tournament.players.add(user_profile)
				context['tournament_notification'] = 'You have registered for the tournament: ' + str(tournament)
			else:
				context['tournament_notification'] = 'Wrong tournament ID or notification'
			print tournament.id
		except ObjectDoesNotExist:
			print "ObjectDoesNotExist"
			context['tournament_notification'] = 'The Tournament you were looking for is not found: ' + request.POST.get('tournament_id')
			pass
		except ValueError:
			print "User has no profile"
			context['tournament_notification'] = 'You have not set a valid summoner name. Please check!'
			print "HI!"
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
    context = dict()
    print 'Tournament Detail View\nTournament id: ' + tournament_id
    tournament = get_object_or_404(Tournament, id=int(tournament_id))

    if not tournament.teams_created:
        if request.POST:
            if 'create_teams' in request.POST:
                tournament.teams_created = tournament_create_teams(request, tournament_id)
                print('Teams Made!')
                tournament.save()
        context['tournament'] = tournament
        print 'Here'
        if (tournament.main_user == request.user):
            is_main_user = True
        else:
            is_main_user = False
        print is_main_user
        context['main_user'] = is_main_user
    else:
        context['tournament'] = tournament
    return render(request, 'tournament_detail.html', context=context)


def remove_from_tournament(request, tournament_id):
	print "Removing "+ str(request.user) + " from tournament "+  str(tournament_id)
	try:
		Tournament.objects.get(id=tournament_id).players.remove(UserProfile.objects.get(user=request.user))
	except Exception, e:
		print str(e)
	return redirect('tournament_detail', tournament_id=tournament_id)


def user_profile_view(request):
	print 'User profile view'
	context = dict()
	if not request.user.is_authenticated:
		return redirect('auth_login')
	instance, found = UserProfile.objects.get_or_create(user=request.user)

	if request.POST:
		print 'POST Submitted: ' + str(request.POST)
		form = UserProfileForm(request.POST or None, instance=instance)
		if form.is_valid():
			saved = form.save(commit = False)
			saved.user = request.user
			lol_mmr = get_mmr(saved.lol_summoner_name)
			if lol_mmr > 0:
				saved.lol_mmr = lol_mmr
				saved.save()
			else:
				context['user_profile_notification'] = "Summoner not found. Please check your Summoner name and try again!"
	else:
		form = UserProfileForm(instance=instance)

	tournaments = Tournament.objects.filter(players=instance)

	profile = get_object_or_404(UserProfile, user=request.user)
	context['form']=form
	context['tournaments']=tournaments
	context['profile']=profile
	return render(request, 'my_profile.html', context)
