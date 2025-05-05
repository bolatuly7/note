from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import (
    CustomUser,
    Subject,
    Homework,
    Grade,
    HomeworkSubmission,
    Attendance,
    Schedule,
    Comment
)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'input-custom',
                'placeholder': field.label,
            })

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'input-custom',
                'placeholder': field.label,
            })

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'description', 'due_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'input-custom',
                'placeholder': field.label if hasattr(field, 'label') else '',
            })

class GradeForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='student'),
        label='Ученик'
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        label='Предмет'
    )

    class Meta:
        model = Grade
        fields = ['student', 'subject', 'value']
        widgets = {
            'value': forms.NumberInput(attrs={
                'min': 1,
                'max': 100,
                'class': 'input-custom',
                'placeholder': 'Оценка'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] = 'input-custom'
            else:
                field.widget.attrs.update({
                    'class': 'input-custom',
                })
            field.widget.attrs['placeholder'] = field.label

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ['answer', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'input-custom',
                'placeholder': field.label,
            })

class AttendanceForm(forms.Form):
    date = forms.DateField(
        label='Дата',
        initial=timezone.localdate,
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'input-custom'}
        )
    )
    schedule_item = forms.ModelChoiceField(
        queryset=Schedule.objects.all(),
        label='Урок',
        widget=forms.Select(attrs={'class': 'input-custom'})
    )
    students = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='student'),
        widget=forms.CheckboxSelectMultiple,
        label='Присутствующие ученики',
        required=False
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'input-custom',
                    'placeholder': 'Ваш комментарий',
                    'rows': 3
                }
            )
        }
