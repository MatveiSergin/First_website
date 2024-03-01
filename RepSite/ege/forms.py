from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms

from .models import Lesson, Student


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'
        widgets = {'student': forms.HiddenInput}

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = {'name', 'typeOfExam', 'subject',
                  'perWeek', 'price', 'solvedTask',
                  'otherInformation', 'password', 'username'}
        widgets = {'password': forms.HiddenInput, 'username': forms.HiddenInput, 'solvedTask': forms.HiddenInput}


class GradeForm(forms.Form):
    newGreenTask = forms.IntegerField(required=False, label='Введите номер зеленого задания')
    newRedTask = forms.IntegerField(required=False, label='Введите номер красного задания')

class HomeworkForm(forms.Form):
    model = Lesson
    fileds = {'homework', 'is_ready'}
    widgets = {'is_ready': forms.HiddenInput}