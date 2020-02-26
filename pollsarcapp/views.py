from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import PollFormValidation
from .models import Proposition, Poll, PollUser
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
import json
import html

# Create your views here.
def home(request):
    polls = Poll.objects.order_by('created_at').reverse()[:5]
    return render(request, 'home.html', {'latest_polls' : polls})

def showPoll(request, id):
    try:
        poll = Poll.objects.get(pk=id)
        propositions = Proposition.objects.filter(poll=poll)
        return render(request, 'showPoll.html', {'poll' : poll, 'propositions' : propositions})
    except Poll.DoesNotExist:
        return Http404

def createPollForm(request):
    return render(request, 'createPoll.html')

def searchUsers(request, name):
    users = User.objects.filter(username__contains=name)#.exclude(is_superuser=False)
    list_users = []
    for user in users:
        list_users.append({'id' : user.id, 'label' : user.username})
    return JsonResponse({'users' : list_users})

def searchPolls(request, name):
    polls = list(Poll.objects.filter(name__contains=name))
    list_polls = []
    for poll in polls:
        list_polls.append({'id' : poll.id, 'name' : poll.name, 'description' : poll.description})
    return JsonResponse({'polls' : list_polls})

def createPoll(request):
    poll_form = PollFormValidation(request.POST or None)

    if poll_form.is_valid() and request.user.is_authenticated:
        id_users = json.loads(request.POST.get("selected_user", ""))
        propositions = json.loads(request.POST.get("proposed_prop", ""))

        poll = Poll(name=poll_form.cleaned_data['poll_name'],
                    description=poll_form.cleaned_data['poll_description'],
                    is_private=poll_form.cleaned_data['is_private'],
                    expiration_date=poll_form.cleaned_data['expiration_date'],
                    owner=request.user
        )
        poll.save()

        createPropositions(propositions, poll)
        if addUsersToPoll(id_users, poll):
            return redirect('/')

    return render(request, 'createPoll.html')

def addUsersToPoll(id_users, poll):
    try:
        users = []
        for id in id_users:
            users.append(User.objects.get(id=id))

        for user in users:
            PollUser(poll=poll, user=user).save()

        return True
    except User.DoesNotExist:
        return False
      
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def createPropositions(props, poll):
    for prop in props:
        Proposition(label=html.escape(prop), poll=poll).save()