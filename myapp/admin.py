
from django.contrib import admin
from .models import CustomUser, Subject, Grade, Homework, Schedule
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_('Дополнительно'), {'fields': ('role',)}),
    )
    list_display = ['username', 'email', 'role', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Homework)
admin.site.register(Schedule)
