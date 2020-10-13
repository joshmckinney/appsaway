from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUser(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CreateUser, self).__init__(*args, **kwargs)
        # make user email field required
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class Login(ModelForm):
    class Meta:
        model = User
        password = forms.CharField(widget=forms.PasswordInput)
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={
        'style':'resize:both;', 'cols':'auto', 'rows': '5'}))
