from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms



class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )


class CreateUserForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'image']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }