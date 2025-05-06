from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_view, name='home'),

    # Аутентификация
    path('login/',    views.login_view,    name='login'),
    path('register/', views.register_view, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('logout/',   views.logout_view,   name='logout'),

    # Расписание
    path('schedule/', views.schedule_view, name='schedule'),

    # Домашние задания
    path('homework/',                     views.homework_view,   name='homework'),
    path('homework/add/',                 views.add_homework,    name='add_homework'),
    path('homework/<int:hw_id>/submit/',  views.submit_homework, name='submit_homework'),

    # Оценки
    path('grades/',    views.grades_view, name='grades'),
    path('grades/add/',views.add_grade,   name='add_grade'),

    # Посещаемость
    path('attendance/mark/',   views.mark_attendance,   name='mark_attendance'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),

    # Профиль
    path('profile/',      views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
