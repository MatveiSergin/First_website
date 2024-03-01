from django.urls import path

from .views import *

urlpatterns = [
    path('', progress, name='lessons'),
    path('accounts/login/', StudentsLoginView.as_view(), name='login'),
    path('accounts/logout/', StudentsLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/add/choice_student', choice_student, name='choice'),
    path('accounts/profile/add/', lesson_add, name='lesson_add'),
    path('accounts/profile/add/student/', student_add, name='student_add'),
    path('delete-student/', deleteStudent, name='deleteStudent'),
    path('delete-lesson/', deleteLesson, name='deleteLesson'),
    path('choice-lesson/', choiceLesson, name='choiceLesson'),
    path('edit-lesson/', editLesson, name='editLesson'),
    path('edit-student/', editStudent, name='editStudent'),
    #path('tests/', tests, name='tests'),
    path('homework/', homework, name='homework'),
]