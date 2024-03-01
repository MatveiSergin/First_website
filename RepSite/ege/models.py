from django.db import models
from django.contrib.auth.models import AbstractUser
class Student(AbstractUser):
    name = models.CharField(null=True, max_length=100, verbose_name="Имя")
    typeOfExam = models.CharField(max_length=10, verbose_name="Название экзамена")
    subject = models.CharField(max_length=20, verbose_name="Название предмета")
    perWeek = models.IntegerField(null=True, blank=True, verbose_name="Количество занятий в неделю")
    price = models.IntegerField(null=True, blank=True, verbose_name="Цена за занятие")
    solvedTask = models.CharField(default=0, max_length=27, verbose_name="Решенные задачи")
    overpayment = models.IntegerField(default=0, verbose_name="Переплата")
    otherInformation = models.TextField(null=True, blank=True, verbose_name="Дополнительная информация")
    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return str(self.name)
class Lesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, verbose_name="Ученик")
    number = models.IntegerField(verbose_name="Номер урока")
    is_paid = models.BooleanField(default=False, verbose_name="Проверка оплаты")
    homework = models.FileField(blank=True, upload_to='Ivan/', verbose_name="Условие дз")
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата занятия')
    is_ready = models.SlugField(max_length=20, default="Not_completed", verbose_name='Готовность')

    def __str__(self):
        return str(self.number) + str(self.student)

class Payment(models.Model):
    id = models.CharField(verbose_name='Id', max_length=100, primary_key=True)
    sender = models.CharField(verbose_name='Отправитель', max_length=100)
    amount = models.IntegerField(verbose_name='сумма перевода', max_length=100)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата занятия')
