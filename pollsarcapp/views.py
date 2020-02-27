from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import PollFormValidation
from .models import Proposition, Poll, PollUser, PropositionUser
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
import html

# Create your views here.
def home(request):
    polls = Poll.objects.order_by('created_at').reverse()[:5]
    return render(request, 'home.html', {'latest_polls' : polls})

@require_http_methods("GET")
@login_required(login_url='login')
def showPoll(request, id):
    try:
        poll = Poll.objects.get(pk=id)
        propositions = Proposition.objects.filter(poll=poll)
        return render(request, 'showPoll.html', {'poll' : poll, 'propositions' : propositions, 'already_answered' : request.user.hasAlreadyAnswered(id)})
    except Poll.DoesNotExist:
        return Http404

@require_http_methods("GET")
@login_required(login_url='login')
def createPollForm(request):
    return render(request, 'createPoll.html')

@require_http_methods("GET")
def searchUsers(request, name):
    users = User.objects.filter(username__contains=name).exclude(is_superuser=True)
    list_users = []
    for user in users:
        list_users.append({'id' : user.id, 'label' : user.username})
    return JsonResponse({'users' : list_users})

@require_http_methods("GET")
def searchPolls(request, name):
    polls = list(Poll.objects.filter(name__contains=name))
    list_polls = []
    for poll in polls:
        list_polls.append({'id' : poll.id, 'name' : poll.name, 'description' : poll.description})
    return JsonResponse({'polls' : list_polls})

@require_http_methods("POST")
@login_required(login_url='login')
def createPoll(request):
    poll_form = PollFormValidation(request.POST or None)

    if poll_form.is_valid():
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
            #Todo send email when user is add to a poll

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

@require_http_methods("POST")
@login_required(login_url='login')
def addUserVote(request):
    if request.method == 'POST':

        try:
            proposition = Proposition.objects.get(id=request.POST.get("proposition_id", ""))
            poll_id = proposition.poll.id

            if not request.user.hasAlreadyAnswered(poll_id):
                PropositionUser(user=request.user, proposition=proposition).save()
                return redirect('poll', id=poll_id)
            else :
                return redirect('poll', id=poll_id)
        except Proposition.DoesNotExist:
            return redirect('')

