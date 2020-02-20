from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Poll(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=True)
    description = models.CharField(max_length=255)
    expiration_date = models.DateField()

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
