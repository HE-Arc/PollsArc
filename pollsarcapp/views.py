from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import PollFormValidation, RegisterForm
from .models import Proposition, Poll, PollUser, PropositionUser
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
import html
from django.core.mail import send_mass_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

def home(request):
    latest_polls = Poll.objects.filter(is_private=False).order_by('created_at').reverse()[:5]
    return render(request, 'home.html', {'latest_polls' : latest_polls})

@login_required(login_url='login')
def showPoll(request, id):
    
    try:
        poll = Poll.objects.get(pk=id)

        is_expired = True
        if poll.expiration_date > datetime.date.today():
            is_expired = False 

        if poll.is_private:
            if request.user.hasInvitedToPoll(id):
                propositions = Proposition.objects.filter(poll=poll)
                return render(request, 'showPoll.html', {'poll' : poll, 'propositions' : propositions, 'is_expired':is_expired, 'already_answered' : request.user.hasAlreadyAnswered(id)})
            else :
                raise Http404
        else : 
            propositions = Proposition.objects.filter(poll=poll)
            return render(request, 'showPoll.html', {'poll' : poll, 'propositions' : propositions, 'is_expired':is_expired, 'already_answered' : request.user.hasAlreadyAnswered(id)})
            
    except Poll.DoesNotExist:
        raise Http404

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
    polls = list(Poll.objects.filter(name__contains=name).filter(is_private=False))
    list_polls = []
    for poll in polls:
        list_polls.append({'id' : poll.id, 'name' : poll.name, 'description' : poll.description})
    return JsonResponse({'polls' : list_polls})

@require_http_methods("POST")
@login_required(login_url='login')
def createPoll(request):
    poll_form = PollFormValidation(request.POST or None)

    if poll_form.is_valid() and request.POST.get("proposed_prop", "") != "[]":
        id_users = json.loads(request.POST.get("selected_user", ""))
        propositions = json.loads(request.POST.get("proposed_prop", ""))

        poll = Poll(name=poll_form.cleaned_data['poll_name'],
                    description=poll_form.cleaned_data['poll_description'],
                    is_private=poll_form.cleaned_data['is_private'],
                    expiration_date=poll_form.cleaned_data['expiration_date'],
                    owner=request.user
        )
        poll.save()

        poll.createPropositions(propositions)
        
        id_users.append(request.user.id)
        if poll.addUsers(request, id_users):
            return redirect('poll/' +  str(poll.id))

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

      
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required(login_url='/accounts/login/')
def user_profile(request, username):
    user = User.objects.get(username=username)
    polls_list = user.getInvitedPolls()

    page = request.GET.get('page', 1)

    paginator = Paginator(polls_list, 5)
    try:
        polls = paginator.page(page)
    except PageNotAnInteger:
        polls = paginator.page(1)
    except EmptyPage:
        polls = paginator.page(paginator.num_pages)

    return render(request, 'user/user_profile.html', {"user": user, "created_polls" : polls})

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
