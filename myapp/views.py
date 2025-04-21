from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Schedule, Grade, Homework  # если есть такие модели

# 👤 ЛОГИН
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('schedule')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# 👤 РЕГИСТРАЦИЯ
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('schedule')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# 🏠 ГЛАВНАЯ
def landing_view(request):
    return render(request, 'index.html')

# 📅 РАСПИСАНИЕ
@login_required
def schedule_view(request):
    schedule = Schedule.objects.all()  # можно фильтровать по пользователю
    return render(request, 'schedule.html', {'schedule': schedule})

# 📊 ОЦЕНКИ
@login_required
def grades_view(request):
    grades = Grade.objects.all()  # если есть модель Grade
    return render(request, 'grades.html', {'grades': grades})

# 📝 ДОМАШКА
@login_required
def homework_view(request):
    homework = Homework.objects.all()  # если есть модель Homework
    return render(request, 'homework.html', {'homework': homework})

# 👤 ПРОФИЛЬ
@login_required
def profile_view(request):
    return render(request, 'profile.html')
