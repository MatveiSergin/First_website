
def definitionSolvedTask(subject, typeOfExam):
    subject = subject.lower()
    if subject == "информатика":
        if typeOfExam == "егэ":
            solvedTask = '0'*27
        if typeOfExam == 'огэ':
            solvedTask = '0'*15

    if subject == "математика":
        if typeOfExam == "егэ-база":
            solvedTask = '0'*21
        if typeOfExam == 'егэ-профиль':
            solvedTask = '0'*18
        if typeOfExam == 'огэ':
            solvedTask = '0'*25
    return solvedTask