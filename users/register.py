from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
import uuid

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        if not user.username:
            user.username = f'user_{uuid.uuid4().hex[:8]}'  # Generate a default username
        if commit:
            user.save()
        return user
    