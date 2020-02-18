from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def createPoll(request):
    return render(request, 'createPoll.html')

def searchUsers(request, name):
    users = User.objects.filter(username__contains=name).exclude(is_superuser=False)
    list_users = []
    for user in users:
        list_users.append((user.id, user.username))
    return JsonResponse({'users' : list_users})


