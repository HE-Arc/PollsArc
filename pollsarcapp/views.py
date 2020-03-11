from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import PollFormValidation, RegisterForm
from .models import Proposition, Poll, PollUser
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
import json
import html
from django.core.mail import send_mass_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

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
        if addUsersToPoll(request, id_users, poll):
            return redirect('/')

    return render(request, 'createPoll.html')

def addUsersToPoll(request, id_users, poll):
    try:
        users = []
        mails = ()

        for id in id_users:
            users.append(User.objects.get(id=id))

        for user in users:
            PollUser(poll=poll, user=user).save()
            link = ''.join([get_current_site(request).domain, reverse('poll', args=[poll.id])])
            message = 'You has been added to the poll :  {}. You can access the poll using this link : {}'.format(poll.name, link)
            mail = ('Added to a poll', message, 'noreply@pollsarc', [user.email])
            mails = (mail,) + mails
        
        send_mass_mail(mails)

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

def createPropositions(props, poll):
    for prop in props:
        Proposition(label=html.escape(prop), poll=poll).save()

@login_required(login_url='/accounts/login/')
def user_profile(request, username):
    user = User.objects.get(username=username)
    polls_list = Poll.objects.filter(owner=user.id)

    page = request.GET.get('page', 1)

    paginator = Paginator(polls_list, 5)
    try:
        polls = paginator.page(page)
    except PageNotAnInteger:
        polls = paginator.page(1)
    except EmptyPage:
        polls = paginator.page(paginator.num_pages)

    return render(request, 'user/user_profile.html', {"user": user, "created_polls" : polls})