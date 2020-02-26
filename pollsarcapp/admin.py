from django.contrib import admin
from .models import Poll, PollUser, Proposition, PropositionUser

# Register your models here.
admin.site.register(Poll)
admin.site.register(PollUser)
admin.site.register(Proposition)
admin.site.register(PropositionUser)