from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError


class SignupForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'firtsname'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'lastname'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))
    password2 = forms.CharField(label='Re-Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 're-password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email yang anda masukan sudah terdaftar")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))

    def clean(self):
        try:
            self.cleaned_data["username"] = get_user_model().objects.get(email=self.data["username"])
        except ObjectDoesNotExist:
            self.cleaned_data["username"] = "a username that do not exists"
        return super(LoginForm, self).clean()

class EmailConfirmationForm(PasswordResetForm):
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email'}))

class reset_password_form(PasswordResetForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))
    password2 = forms.CharField(label='Re-Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 're-password'}))
