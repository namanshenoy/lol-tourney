from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from forms import *


# Create your views here.

@login_required
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
        form = TournamentForm()
        return render(request, 'index.html', {'form': form, })
      

