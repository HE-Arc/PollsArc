from django import forms

class PollFormValidation(forms.Form):
    is_private = forms.BooleanField()
    #users = forms.MultipleChoiceField()
    poll_name = forms.CharField()
    poll_description = forms.CharField()
    expiration_date = forms.DateField()
    #propositions = forms.MultipleChoiceField()