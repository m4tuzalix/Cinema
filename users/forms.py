from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.TextInput(attrs={
        "max_length":"20"
    })
    last_name = forms.TextInput(attrs={
        "max_length":"20"
    })

    class Meta():
        model = User
        fields = ['username', "first_name", "last_name", 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = "Max 20 characters"
        self.fields['first_name'].help_text = "Max 20 characters"
        self.fields['last_name'].help_text = "Max 20 characters"