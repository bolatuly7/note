from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Ученик'),
        ('teacher', 'Учитель'),
        ('parent', 'Родитель'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    photo = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Grade(models.Model):
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.subject.name}: {self.value}"


class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'}
    )
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return f"{self.subject.name} - до {self.due_date}"


class Schedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)  # Пн, Вт, Ср и т.д.
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'}
    )

    def __str__(self):
        return f"{self.subject.name} ({self.day_of_week} {self.start_time}-{self.end_time})"


class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(
        Homework,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    answer = models.TextField(verbose_name='Ответ студента')
    file = models.FileField(
        upload_to='submissions/',
        blank=True,
        null=True,
        verbose_name='Файл ответа'
    )
    submitted = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('homework', 'student')

    def __str__(self):
        return f"{self.student.username} → {self.homework.subject.name} ({self.submitted:%Y-%m-%d %H:%M})"


class Attendance(models.Model):
    schedule_item = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='attendances'
    )
    date = models.DateField(default=timezone.localdate)
    present = models.BooleanField(default=False, verbose_name='Присутствовал')

    class Meta:
        unique_together = ('schedule_item', 'student', 'date')
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещаемость'

    def __str__(self):
        status = '✔' if self.present else '✘'
        return f"{self.date} | {self.student.username} | {self.schedule_item.subject.name} — {status}"


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        preview = (self.text[:17] + '...') if len(self.text) > 20 else self.text
        return f"{self.author.username}: {preview}"
