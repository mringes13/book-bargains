from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Book, Message

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {"username": "Email",}

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'major': forms.TextInput(attrs={'class':'form-control'}),
            'housing': forms.TextInput(attrs={'class':'form-control'}),
            'field':forms.Select(attrs={'class':'form-control'}),
        }
        labels = {'field': "Most Interested In:"}

class ListBookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('user','uuid','reported')
        widgets = {
            'selldonate': forms.Select(attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'author': forms.TextInput(attrs={'class':'form-control'}),
            'ISBN13': forms.TextInput(attrs={'class':'form-control'}),
            'ISBN13Conf': forms.TextInput(attrs={'class':'form-control'}),
            'edition': forms.TextInput(attrs={'class':'form-control'}),
            'condition': forms.Select(attrs={'class':'form-control'}),
            'field': forms.Select(attrs={'class':'form-control'}),
            'price': forms.TextInput(attrs={'class':'form-control'})
            
        }
        labels = {'selldonate': "Selling or Donating?", 'ISBN13Conf':'Confirm ISBN'}

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('text',)
        widgets = {'text': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Type message here.'})}
        labels = {'text': 'New message:',}

class AddRatingForm(forms.Form):
    addedrating = forms.FloatField(label="Rating", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter a rating from 1.0-5.0."}))
