from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PollFormValidation(forms.Form):
    is_private = forms.BooleanField(initial=True, required=False)
    poll_name = forms.CharField(required=True, max_length=100)
    poll_description = forms.CharField(required=True, max_length=255)
    expiration_date = forms.DateField(required=True)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
