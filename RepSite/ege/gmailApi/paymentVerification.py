from .gmailApi import requestForGmail
from ..models import Student, Lesson


def paymetVerification(name, amountOfMoney):
    student = Student.objects.get(name=name)
    price = student.price
    lessons = Lesson.objects.filter(student=student)
    Unpaidlessons = lessons.filter(is_paid=False).order_by('number')
    numberOfUnpaidLessons = len(Unpaidlessons)

    if amountOfMoney == price and numberOfUnpaidLessons != 0:
        firstUnpaidlesson = Unpaidlessons[0]
        firstUnpaidlesson.is_paid = True
        firstUnpaidlesson.save()

    elif amountOfMoney == price and numberOfUnpaidLessons == 0:
        print(f"Переплата у {student.name}")
        student.overpayment += 1
        student.save()

    elif amountOfMoney > price:
        paidLessons = amountOfMoney // price

        while paidLessons != 0 and numberOfUnpaidLessons != 0:
            firstUnpaidlesson = Unpaidlessons[0]
            firstUnpaidlesson.is_paid = True
            firstUnpaidlesson.save()
            Unpaidlessons = lessons.filter(is_paid=False).order_by('number')
            numberOfUnpaidLessons = len(Unpaidlessons)
            paidLessons = paidLessons - 1

        if paidLessons != 0:
            student.overpayment += paidLessons
            student.save()
            print(f"Переплата у {student.name} на {student.overpayment} занятий")

    elif amountOfMoney < price:
        print(f"Переплата у {student.name} на {amountOfMoney} рублей")


def getNewPayments():
    request = requestForGmail()
