from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth
import html
from django.core.mail import send_mass_mail
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import sys


# Create your models here.
class Poll(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=True)
    description = models.CharField(max_length=255)
    expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def createPropositions(self, props):
        for prop in props:
            Proposition(label=html.escape(prop), poll=self).save()

    def addUsers(self, request, id_users):
        try:
            users = []
            mails = ()

            for id in id_users:
                users.append(User.objects.get(id=id))    

            PollUser(poll=self, user=request.user).save()

            for user in users:
                PollUser(poll=self, user=user).save()

                link = ''.join([get_current_site(request).domain, reverse('poll', args=[self.id])])
                message = 'You has been added to the poll :  {}. You can access the poll using this link : {}'.format(self.name, link)
                mail = ('Added to a poll', message, 'noreply@pollsarc', [user.email])
                mails = (mail,) + mails
            
            send_mass_mail(mails)

            return True
        except User.DoesNotExist:
            return False

    def stats(self, request):
        labels = []
        data = []

        propositions = Proposition.objects.filter(poll=self)
        for proposition in propositions:
            labels.append(proposition.label)
            data.append(proposition.votesNb())

        return {'labels' : labels, 'data' : data}

    def __str__(self):
        return "Poll -> " + self.name

    class Meta:
        verbose_name = "Poll"
        verbose_name_plural = "Polls"

class PollUser(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "PollUser -> poll : " + self.poll.name + ", user : " + self.user.username

    class Meta:
        verbose_name = "PollUser"
        verbose_name_plural = "PollUser"

class Proposition(models.Model):
    label = models.CharField(max_length=30)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def votesNb(self):
        return len(PropositionUser.objects.filter(proposition=self))

    def __str__(self):
        return "Proposition -> label : " + self.label + ", poll : " + self.poll.name

    class Meta:
        verbose_name = "Proposition"
        verbose_name_plural = "Propositions"

class PropositionUser(models.Model):
    proposition = models.ForeignKey(Proposition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "PropositionUser -> proposition : " + self.proposition.label + ", user : " + self.user.username

    class Meta:
        verbose_name = "PropositionUser"
        verbose_name_plural = "PropositionUser"

def hasAlreadyAnswered(self, poll_id):
    user_has_already_answered = False
    try: 
        answered_polls = list(PropositionUser.objects.filter(user=self))

        for answered_poll in answered_polls:
            if(answered_poll.proposition.poll.id == poll_id):
                user_has_already_answered = True
    except PropositionUser.DoesNotExist:
        user_has_already_answered = False

    return user_has_already_answered

def hasInvitedToPoll(self, poll_id):
    has_invited_to_poll = False 
    invited_poll = PollUser.objects.filter(user=self, poll=Poll(poll_id))

    if len(invited_poll) >= 1: 
        has_invited_to_poll = True
    else : 
        has_invited_to_poll = False
    return has_invited_to_poll

User.add_to_class("hasAlreadyAnswered", hasAlreadyAnswered)
User.add_to_class("hasInvitedToPoll", hasInvitedToPoll)