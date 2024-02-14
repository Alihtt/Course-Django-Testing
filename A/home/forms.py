from django.contrib.auth.models import User
from django import forms


class UserRegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise forms.ValidationError('email already exists')
        return email

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('passwords does not match')
