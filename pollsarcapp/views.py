from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from .forms import PollFormValidation

# Create your views here.
def home(request):
    return render(request, 'home.html')

def createPollForm(request):
    return render(request, 'createPoll.html')

def searchUsers(request, name):
    users = User.objects.filter(username__contains=name)#.exclude(is_superuser=False)
    list_users = []
    for user in users:
        list_users.append({'id' : user.id, 'label' : user.username})
    return JsonResponse({'users' : list_users})

def createPoll(request):
    poll_form = PollFormValidation(request.POST or None)
    msg = ""
    if poll_form.is_valid():
        msg = "ok"
    else :
        msg ="none"
    return JsonResponse(request.POST)