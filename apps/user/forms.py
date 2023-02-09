from apps.user.models import User
from django import forms
from datetime import timedelta
from django.utils import timezone
from apps.user.models import EmailVerification
import uuid
from apps.user.tasks import send_verification_email
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите имя', 'class':'login-input' }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите фамилию', 'class':'login-input' }))
    username= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Имя пользователя', 'class':'login-input' }))
    email= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите электронную почту','class':'login-input', 'type':'email'}))
    password1= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите пароль', 'class':'login-input', 'type':'password'}))
    password2= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Потвердите пароль', 'class':'login-input', 'type':'password'}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        # user = super(UserRegistrationForm, self).save(commit=True)
        # expiration = timezone.now() + timedelta(hours=48)
        # record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        send_verification_email.delay(user.id)
        return user



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Имя пользователя', 'class':'login-input' }))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите пароль', 'class':'login-input', 'type':'password'}))
    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите имя', 'class':'form-control' }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите фамилию', 'class':'form-control' }))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control' }), required=False)
    username= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Имя пользователя', 'class':'form-control' , 'readonly': True}))
    email= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите электронную почту','class':'form-control', 'type':'email','readonly': True}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image', 'username', 'email']