
from django.contrib import admin
from django.urls import path
from myapp import views as myapp_views
from django.contrib.auth.views import LogoutView
from myapp.views import BasePreviewView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', BasePreviewView.as_view(), name='base_preview'),
    path('', myapp_views.landing_view, name='home'),  # ← главная страница
    path('login/', myapp_views.login_view, name='login'),
    path('register/', myapp_views.register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('schedule/', myapp_views.schedule_view, name='schedule'),
    path('grades/', myapp_views.grades_view, name='grades'),
    path('homework/', myapp_views.homework_view, name='homework'),

]
