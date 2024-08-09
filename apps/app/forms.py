from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'description', 'category']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'inputTitle'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'inputImage'
            }),
            'description': SummernoteWidget(),
            'category': forms.CheckboxSelectMultiple()
        }


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

    
