from django import forms

class PollFormValidation(forms.Form):
    is_private = forms.BooleanField(initial=True, required=False)
    poll_name = forms.CharField(required=True, max_length=100)
    poll_description = forms.CharField(required=True, max_length=255)
    expiration_date = forms.DateField(required=True)