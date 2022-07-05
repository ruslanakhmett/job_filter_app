from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from parsers_and_bot.models import Global_Users
from datetime import datetime


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='user name', help_text='max 150 characters', widget=forms.TextInput(attrs={"class": "form-control", 'autocomplete': "off"}))
    password1 = forms.CharField(label='pass', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='pass again', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={"class": "form-control"}))


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользвателя', widget=forms.TextInput(attrs={"class": "form-control", 'autocomplete': "off"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))



class AddSearch(forms.Form):
    vacancy_name = forms.CharField(label='Наименование вакансии, например Системный администратор, Java Junior и т.д', widget=forms.TextInput(attrs={"class": "form-control"}))
    sity = forms.CharField(label='Город', initial='Москва', widget=forms.TextInput(attrs={"class": "form-control"}))
    salary_min = forms.IntegerField(label='желаемая зарплата от(если не важна, оставь 0)', initial=0, widget=forms.TextInput(attrs={"class": "form-control"}))
    salary_max = forms.IntegerField(label='желаемая зарплата до(если не важна, оставь 0)', initial=0, widget=forms.TextInput(attrs={"class": "form-control"})) 
    start_when = forms.CharField(label='все опубликованные с', initial=str(datetime.now().date()), widget=forms.TextInput(attrs={"class": "form-control"}))
    only_with_salary = forms.CharField(label='ищем только с указанной зарплатой', initial=False, widget=forms.TextInput(attrs={"class": "form-control"}))