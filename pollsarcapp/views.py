import json
import html
import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mass_mail
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from pollsarcapp.forms import PollFormValidation, RegisterForm
from pollsarcapp.models import Proposition, Poll, PollUser, PropositionUser


def home(request):
    latest_polls = Poll.objects.filter(
        is_private=False).order_by('created_at').reverse()[:4]
    return render(request, 'home.html', {'latest_polls': latest_polls})


@login_required(login_url='login')
def show_poll(request, id):
    """
    Display poll from an id, verifify poll expiration date, if poll is private verify user is invited 

    Arguments:
        request {Request} -- Django request object
        id {int} -- id of the poll

    Raises:
        Http404: Raised when user is not invited to a private poll
        Http404: Raised when the poll doesn't exist

    Returns:
        Template -- Django poll template
    """

    try:
        poll = Poll.objects.get(pk=id)

        is_expired = True
        if poll.expiration_date > datetime.date.today():
            is_expired = False

        if poll.is_private:
            if request.user.has_invited_to_poll(id):
                propositions = Proposition.objects.filter(poll=poll)
                return render(request, 'show_poll.html', {'poll': poll, 'propositions': propositions, 'is_expired': is_expired, 'already_answered': request.user.has_already_answered(id)})
            else:
                raise Http404
        else:
            propositions = Proposition.objects.filter(poll=poll)
            return render(request, 'show_poll.html', {'poll': poll, 'propositions': propositions, 'is_expired': is_expired, 'already_answered': request.user.has_already_answered(id)})

    except Poll.DoesNotExist:
        raise Http404


@require_http_methods("GET")
@login_required(login_url='login')
def create_poll_form(request):
    return render(request, 'create_poll.html')


@require_http_methods("GET")
def search_users(request, name):
    """
    Search user by username

    Arguments:
        request {Request} -- Django request object
        name {string} -- username to search

    Returns:
        JsonResponse -- Return all finded user with the given username in the JSON format
    """

    users = User.objects.filter(
        username__contains=name).exclude(is_superuser=True)
    list_users = []
    for user in users:
        list_users.append({'id': user.id, 'label': user.username})
    return JsonResponse({'users': list_users})


@require_http_methods("GET")
def search_polls(request, name):
    """
    Search poll by name

    Arguments:
        request {Request} -- Django request
        name {string} -- poll to serach

    Returns:
        JsonResponse -- Return all finded poll iwth the given poll name in the JSON format
    """

    polls = list(Poll.objects.filter(
        name__contains=name).filter(is_private=False))
    list_polls = []
    for poll in polls:
        list_polls.append({'id': poll.id, 'name': poll.name,
                           'description': poll.description})
    return JsonResponse({'polls': list_polls})


@require_http_methods("POST")
@login_required(login_url='login')
def create_poll(request):
    """
    Create a poll from the poll creation form, add all invited user to the poll, and create propositions

    Arguments:
        request {Request} -- Django request 

    Returns:
        Template -- Poll page template
    """

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

        poll.create_propositions(propositions)

        #id_users.append(request.user.id)
        if poll.add_users(request, id_users):
            return redirect('poll/' + str(poll.id))

    return render(request, 'create_poll.html')


def add_users_to_poll(id_users, poll):
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
    """
    Validate the register form, save and log the user

    Arguments:
        request {Request} -- Django request

    Returns:
        redirect -- If the form is valid, redirect to the home page as connected user
        redirect -- If the form is not valid, redirect to the registration form with errors
    """

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


@login_required(login_url='login', redirect_field_name=None)
def user_profile(request, username):
    """
    Create the profile page of the user, and build a paginator for the polls

    Arguments:
        request {Request} -- Django request
        username -- parameter from url

    Returns:
        redirect -- If user connected request his own profile page, return his profile page
        redirect -- If the requested user profile is not coresponding to the connected user, then the user is redirected to the home page
    """

    if request.user.username == username:
        user = User.objects.get(username=username)
        polls_list = user.get_invited_polls()

        page = request.GET.get('page', 1)

        paginator = Paginator(polls_list, 5)
        try:
            polls = paginator.page(page)
        except PageNotAnInteger:
            polls = paginator.page(1)
        except EmptyPage:
            polls = paginator.page(paginator.num_pages)

        return render(request, 'user/user_profile.html', {"user": user, "created_polls": polls})
    else:
        return redirect('home')


@require_http_methods("POST")
@login_required(login_url='login')
def add_user_vote(request):
    """
    Add a user proposition for a poll

    Arguments:
        request {Request} -- Django request

    Returns:
        redirect -- If sucess redirect to poll page, otherwise redirect to home page
    """

    if request.method == 'POST':
        try:
            proposition = Proposition.objects.get(
                id=request.POST.get("proposition_id", ""))
            poll_id = proposition.poll.id

            if not request.user.has_already_answered(poll_id):
                PropositionUser(user=request.user,
                                proposition=proposition).save()
                return redirect('poll', id=poll_id)
            else:
                return redirect('poll', id=poll_id)
        except Proposition.DoesNotExist:
            return redirect('')
