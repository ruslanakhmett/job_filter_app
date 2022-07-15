from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm, AddSearch
from django.contrib import messages
from django.contrib.auth import login, logout
import time
from parsers_and_bot.models import Global_Users, Vacancy


def home(request):
    return render(request, 'webface/index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            add_user = Global_Users(name=user.username, tg_chat_id=0, salary_min=0, salary_max=0, email=user.email)
            add_user.save()
            messages.success(request, 'success!')
            return redirect('cabinet')
        else:
            messages.error(request, 'registration error!')
    else:
        form = UserRegisterForm()
    return render(request, 'webface/register.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('home')


def singin(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('cabinet')
    else:
        form = UserLoginForm()

    return render(request, 'webface/singin.html', {"form": form})


def cabinet(request):
    the_user = Global_Users.objects.get(name=request.user.username)
    if len(the_user.vacancy_name) > 2:
        data = {"vacancy_name": the_user.vacancy_name, "sity": the_user.sity, "salary_min": the_user.salary_min, "salary_max": the_user.salary_max, "start_when": the_user.start_when, "only_with_salary": the_user.only_with_salary}
    else:
        data = {"vacancy_name": '', "sity": '', "salary_min": '', "salary_max": '', "start_when": '', "only_with_salary": ''}
    return render(request, 'webface/cabinet.html', context=data)


def add_search(request):
    result_string = ''
    name_array = []
    if request.method == 'POST':
        form = AddSearch(request.POST)
        if form.is_valid():
            Global_Users.objects.filter(name=request.user.username).update(**form.cleaned_data)
            for user in Global_Users.objects.all():
                if user.name == request.user.username:
                    name_array = user.vacancy_name.split()
                    for item in name_array:
                        if len(item) > 2:  # исключаем из списка ключевых слов предлоги и всякое такое
                            result_string += item + ' AND '
                        else:
                            continue

            Global_Users.objects.filter(name=request.user.username).update(vacancy_name_durty='NAME:(' + result_string[:-5] + ')')  # формируем специальную строку для поиска на хх по названию
            Global_Users.objects.filter(name=request.user.username).update(start_when_unix=int(time.mktime(time.strptime(user.start_when, '%Y-%m-%d'))))  # формируем дату в unix формате для superjob надо

            for vac in Vacancy.objects.all():
                if vac.for_user == request.user.username:
                    vac.delete()
            return redirect('cabinet')
    else:
        form = AddSearch()
    return render(request, 'webface/add_search.html', {"form": form})
