from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
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
