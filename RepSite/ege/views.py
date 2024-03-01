import random
from transliterate import translit
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from .additionalFunctions import definitionSolvedTask
from .forms import GradeForm, LessonForm, StudentForm, HomeworkForm
from .gmailApi.paymentVerification import paymetVerification
from .models import *


# Create your views here.
@login_required
def progress(request):
    lessons = Lesson.objects.filter(student=request.user.pk).order_by('-number')
    username = request.user.name
    subject = request.user.subject
    if len(request.GET)==1:
        les_num = int(request.GET['num'])
        les = lessons.get(number=les_num)
    else:
        les = lessons[0]
    context = {'username': username, 'subject': subject, 'lessons': lessons, 'les':les}
    return render(request, 'ege/lessons.html', context)

class StudentsLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'ege/login.html'

class StudentsLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'ege/logout.html'

@login_required
def profile(request):
    lessons = Lesson.objects.filter(student=request.user.pk).order_by('-number')
    username = request.user.name
    subject = request.user.subject
    numberTask = list()
    for number in range(1, len(request.user.solvedTask) + 1):
        numberTask.append(number)
    solvedTask = request.user.solvedTask
    context = {'username': username, 'subject': subject, 'lessons': lessons,
               'solvedTask': solvedTask, 'numberTask': numberTask}
    return render(request, 'ege/profile.html', context)

@login_required
def lesson_add(request):
    lessons = Lesson.objects.filter(student=request.user.pk).order_by('-number')
    username = request.user.name
    subject = request.user.subject
    name = request.GET['student']
    student = Student.objects.get(name=name)

    if request.method == 'POST' and 'changeGrade' in request.POST:
        formGrade = GradeForm(request.POST, request.FILES)
        if formGrade.is_valid():
            if formGrade.cleaned_data['newGreenTask'] is not None:
                taskNum = int(formGrade.cleaned_data['newGreenTask'])
                if taskNum <= len(student.solvedTask):
                    student.solvedTask = student.solvedTask[:taskNum-1] + "1" + student.solvedTask[taskNum:]
                    student.save()
            if  formGrade.cleaned_data['newRedTask'] is not None:
                taskNum = int(formGrade.cleaned_data['newRedTask'])
                if taskNum <= len(student.solvedTask):
                    student.solvedTask = student.solvedTask[:taskNum - 1] + "0" + student.solvedTask[taskNum:]
                    student.save()
            return redirect('/accounts/profile/add/'+'?student='+student.name)

    elif request.method == 'POST' and 'addLes' in request.POST:
        formLes = LessonForm(request.POST, request.FILES)
        if formLes.is_valid():
            formLes.save()
            return redirect('profile')
    else:
        numberTask = list()
        for number in range(1, len(student.solvedTask) + 1):
            numberTask.append(number)
        solvedTask = student.solvedTask
        les = Lesson.objects.filter(student=student.pk).order_by('-number')
        formGrade = GradeForm()
        if len(les) != 0:
            newLes = les[0].number + 1
        else:
            newLes = 1
        formLes = LessonForm(initial={'number': newLes, 'student': student.pk})
        context = {'formLes': formLes, 'username': username,
                   'subject': subject, 'lessons': lessons, 'student': student,
                   'solvedTask': solvedTask, 'numberTask': numberTask,
                   'formGrade': formGrade}
        return render(request, 'ege/lesson_add.html', context)

@login_required
def choice_student(request):
    lessons = Lesson.objects.filter(student=request.user.pk).order_by('-number')
    username = request.user.name
    subject = request.user.subject
    students = Student.objects.all()
    action = request.GET['action']
    context = {'students': students, 'username': username,
               'subject': subject, 'lessons': lessons,
               'direction': action}
    return render(request, 'ege/choice_student.html', context)

@login_required
def student_add(request):
    lessons = Lesson.objects.filter(student=request.user.pk).order_by('-number')
    username = request.user.name
    subject = request.user.subject
    context = {'username': username,
               'subject': subject,
               'lessons': lessons,
               }
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            newStudent = form.save(commit=False)
            newStudent.username = translit(newStudent.name, language_code='ru', reversed=True).lower()
            login = newStudent.username
            password = newStudent.password
            newStudent.set_password(password)
            context['login'] = login
            context['password'] = password
            solvedTask = definitionSolvedTask(newStudent.subject, newStudent.typeOfExam)
            newStudent.solvedTask = solvedTask
            newStudent.save()
            return render(request, 'ege/student_add_successfull.html', context)
    else:
        password = ''
        newName = 'name'
        for i in range(5):
            password += random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
            newName += random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
        form = StudentForm(initial={'password': password, 'username': newName, 'solvedTask': '0'})
        context['form'] = form
        print(password, newName)
        return render(request, 'ege/student_add.html', context)

@login_required
def deleteStudent(request):
    nameStudent = request.GET['student']
    student = Student.objects.get(name=nameStudent)
    student.delete()
    return redirect('profile')
@login_required
def deleteLesson(request):
    lessons = Lesson.objects.filter(student=request.user.pk).order_by('-number')
    username = request.user.name
    subject = request.user.subject
    nameStudent = request.GET['student']
    student = Student.objects.get(name=nameStudent)
    if 'lesson' in request.GET:
        numLes = request.GET['lesson']
        lesson = Lesson.objects.filter(student=student).get(number=numLes)
        lesson.delete()
        return redirect('profile')
    else:
        lesForDelete = Lesson.objects.filter(student=student).order_by('-number')
        context = { 'username': username, 'subject': subject,
                    'lessons': lessons, 'lesForDelete': lesForDelete,
                    'student': student, }
        return render(request, 'ege/deleteLesson.html', context)
@login_required
def choiceLesson(request):
    lessons = Lesson.objects.filter(student=request.user.pk).order_by('-number')
    username = request.user.name
    subject = request.user.subject
    name = request.GET['student']
    student = Student.objects.get(name=name)
    lessonsThisStudent = Lesson.objects.filter(student=student).order_by('-number')
    context = {'username': username, 'subject': subject,
               'lessons': lessons, 'student': student,
               'lessonsThisStudent': lessonsThisStudent}
    return render(request, 'ege/choice_lesson.html', context)
@login_required
def editLesson(request):
    lessons = Lesson.objects.filter(student=request.user.pk).order_by('-number')
    username = request.user.name
    subject = request.user.subject
    number = request.GET['lesson']
    name = request.GET['student']
    student = Student.objects.get(name=name)
    lessonsThisStudent = Lesson.objects.filter(student=student)
    for les in lessonsThisStudent:
        if les.number == int(number):
            lesson = les
            break
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = LessonForm(instance=lesson)
        context = {'username': username, 'subject': subject,
               'lessons': lessons, 'form': form,
               'student': student}
        return render(request, 'ege/lessonEdit.html', context)

@login_required
def editStudent(request):
    lessons = Lesson.objects.filter(student=request.user.pk).order_by('-number')
    username = request.user.name
    subject = request.user.subject
    name = request.GET['student']
    student = Student.objects.get(name=name)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            solvedTask = definitionSolvedTask(student.subject, student.typeOfExam)
            student.solvedTask = solvedTask
            student.save()
            return redirect('profile')
    else:
        form = StudentForm(instance=student)
        context = {'username': username, 'subject': subject,
                   'lessons': lessons, 'form': form,
                   'student': student
                   }
        return render(request, 'ege/studentEdit.html', context)

def tests(request):
    return render(request, 'ege/tests.html')

@login_required
def homework(request):
    lessons = Lesson.objects.filter(student=request.user.pk).order_by('-number')
    username = request.user.name
    subject = request.user.subject
    name = request.GET['student']
    numles = request.GET['lesson']
    student = Student.objects.get(name=name)
    lesson = Lesson.objects.filter(student=student).get(number=numles)
    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES, instance=lesson)
        form.save()
        return redirect('profile')
    else:
        form = HomeworkForm(initial={'homework': lesson.homework})
        context = {
            'username': username, 'subject': subject,
            'lessons': lessons, 'form': form,
        }
        return render(request, 'ege/homework.html', context)