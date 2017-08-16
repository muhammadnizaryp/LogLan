from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from .gmail import send_mail_gmail
from django.template import loader
from django.utils.translation import gettext, gettext_lazy as _



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

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)

        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        for to in [to_email]:
            if html_email_template_name is not None:
                body = loader.render_to_string(html_email_template_name, context)
            send_mail_gmail(subject, body, from_email, to)


class SetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(
        label='Kata Sandi Baru',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Kata Sandi Baru'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Konfirmasi Kata Sandi Baru',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Konfirmasi Kata Sandi Baru'}),
        strip=False,
)
