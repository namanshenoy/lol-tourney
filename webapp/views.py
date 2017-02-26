from django.shortcuts import render  
from forms import *

# Create your views here.
def index(request):
  if request.POST:
    form = TournamentForm(request.POST)
    if form.is_valid():
      form.save()
    return render(request, 'index.html', {'form':form,})
  else:
    form = TournamentForm()
    return render(request, 'index.html', {'form':form,})