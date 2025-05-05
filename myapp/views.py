from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone

from .forms import (
    CustomUserCreationForm,
    HomeworkForm,
    GradeForm,
    ProfileForm,
    SubmissionForm,
    AttendanceForm,
)
from .models import (
    CustomUser,
    Schedule,
    Grade,
    Homework,
    HomeworkSubmission,
    Attendance,
)

# Декоратор: доступ только для учителей
def teacher_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return HttpResponseForbidden("Доступ только для учителей")
        return view_func(request, *args, **kwargs)
    return _wrapped

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

# 👋 ВЫХОД
def logout_view(request):
    logout(request)
    return redirect('login')

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

# 🏠 ЛАНДИНГ
def landing_view(request):
    return render(request, 'index.html')

# 📅 РАСПИСАНИЕ
@login_required
def schedule_view(request):
    schedule = Schedule.objects.all()
    return render(request, 'schedule.html', {'schedule': schedule})

# 📊 ОЦЕНКИ (список)
@login_required
def grades_view(request):
    grades = Grade.objects.all()
    return render(request, 'grades.html', {'grades': grades})

# 📝 ДОМАШКА (список)
@login_required
def homework_view(request):
    homework = Homework.objects.all()
    return render(request, 'homework.html', {'homework': homework})

# ➕ ДОБАВИТЬ ДОМАШНЕЕ ЗАДАНИЕ
@login_required
@teacher_required
def add_homework(request):
    form = HomeworkForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        hw = form.save(commit=False)
        hw.teacher = request.user
        hw.save()
        messages.success(request, "Домашнее задание создано")
        return redirect('homework')
    return render(request, 'add_homework.html', {'form': form})

# ➕ ДОБАВИТЬ ОЦЕНКУ
@login_required
@teacher_required
def add_grade(request):
    form = GradeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Оценка выставлена")
        return redirect('grades')
    return render(request, 'add_grade.html', {'form': form})

# 👤 ПРОФИЛЬ (просмотр)
@login_required
def profile_view(request):
    return render(request, 'profile.html')

# 👤 РЕДАКТИРОВАНИЕ ПРОФИЛЯ
@login_required
def profile_edit(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён")
            return redirect('profile')
        messages.error(request, "Проверьте форму и исправьте ошибки.")
    return render(request, 'profile_edit.html', {'form': form})

# ✍️ СДАЧА ДОМАШНЕГО ЗАДАНИЯ
@login_required
def submit_homework(request, hw_id):
    hw = get_object_or_404(Homework, id=hw_id)
    if request.user.role != 'student':
        return HttpResponseForbidden("Только ученики могут сдавать ДЗ")
    if hw.due_date < timezone.localdate():
        messages.error(request, "Срок сдачи истёк")
        return redirect('homework')
    submission = HomeworkSubmission.objects.filter(homework=hw, student=request.user).first()
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.homework = hw
            obj.student = request.user
            obj.submitted = timezone.now()
            obj.save()
            messages.success(request, "Ответ успешно отправлен")
            return redirect('homework')
        messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = SubmissionForm(instance=submission)
    return render(request, 'submit_homework.html', {
        'homework': hw,
        'form': form,
        'submission': submission,
    })

# 📝 ОТМЕТКА ПОСЕЩАЕМОСТИ
@login_required
@teacher_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            lesson = form.cleaned_data['schedule_item']
            present_students = form.cleaned_data['students']
            Attendance.objects.filter(schedule_item=lesson, date=date).delete()
            for student in CustomUser.objects.filter(role='student'):
                Attendance.objects.create(
                    schedule_item=lesson,
                    student=student,
                    date=date,
                    present=(student in present_students)
                )
            messages.success(request, f"Посещаемость за {date} сохранена")
            return redirect('mark_attendance')
    else:
        form = AttendanceForm()
    return render(request, 'mark_attendance.html', {'form': form})

# 🗂️ ОТЧЁТ ПО ПОСЕЩАЕМОСТИ
@login_required
@teacher_required
def attendance_report(request):
    date = request.GET.get('date', timezone.localdate())
    records = Attendance.objects.filter(date=date).select_related('student', 'schedule_item')
    return render(request, 'attendance_report.html', {
        'records': records,
        'date': date,
    })
