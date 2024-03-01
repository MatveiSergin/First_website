import json

import os

import telebot

from telebot import types

from telebot.types import Message, CallbackQuery

from Bot.config import TOKEN, ADMIN_CHAT_ID, STAFF_ID

bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(commands=["start"])
def start(message: Message):
    with open('data.json', 'r') as jsonFile:
        dta = json.load(jsonFile)

    user_id = message.chat.id
    print(user_id, message.from_user.id)
    username = message.chat.username

    if user_id in STAFF_ID:
        for staff in STAFF_ID:
            if user_id == staff:
                kb = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text='Загрузка дз', callback_data='download_dz')
                kb.add(button1)
                bot.send_message(message.chat.id, text='Выбери нужное действие:', reply_markup=kb)


    elif str(user_id) not in dta:

        dta[user_id] = {'username': username, 'name': None, "dz-task": [], "dz_answers": []}
        sent = bot.send_message(message.chat.id, text="Введите имя и фамилию. \n\n <b>Например: </b> <i>Иван Иванов</i>", parse_mode='HTML')
        bot.register_next_step_handler(sent, registration)
    else:
        bot.send_message(message.chat.id, text='Вы уже зарегистрированы!')
        navigation(message)
    with open('data.json', 'w') as jsonFile:
        json.dump(dta, jsonFile, indent=4, ensure_ascii=True)

def choice_dz_for_answer(message: Message):
    with open('data.json', 'r') as jsonFile:
        dta = json.load(jsonFile)

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    dz_tasks = dta[str(message.chat.id)]['dz-task']

    if len(dz_tasks) > 5:
        for i in range(5):
            file_name = dz_tasks[i][:-4]
            button = types.InlineKeyboardButton(text=file_name, callback_data=file_name)
            keyboard.add(button)
    else:
        for task in dz_tasks:
            file_name = task[:-4]
            button = types.InlineKeyboardButton(text=file_name, callback_data=file_name)
            keyboard.add(button)

    bot.send_message(message.chat.id, text='Выбери к какой домашке хочешь дать ответ', reply_markup=keyboard)

@bot.message_handler(commands=["nav"])
def navigation(message: Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton(text='Последнее дз', callback_data='last_dz')
    button2 = types.InlineKeyboardButton(text='Полный список дз', callback_data='all_dz')
    button3 = types.InlineKeyboardButton(text='Проверка дз', callback_data='check_dz')
    button4 = types.InlineKeyboardButton(text='Инструкция по отправке дз', callback_data='instuctins_for_sending_dz')
    keyboard.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, text=str(f'Привет! Этот бот создан для автоматической рассылки и проверки '
                                               f'домашней работы. \n\n Здесь ты будешь получать уведомления при '
                                               f'поступлении новой домашки! \n \n После выполнения заданий, тебе '
                                               f'необходимо отправить их на проверку также через этого бота. \n\n '
                                               f'Выбери свое дальнейшее действие:'), reply_markup=keyboard)


@bot.message_handler(commands=["download_dz"])
def download_dz(message: Message):
    os.chdir('C:/Users/matve/PycharmProjects/CreateSite/Bot')
    with open('data.json', 'r') as jsonFile:
        dta = json.load(jsonFile)

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    for user in dta:
        button = types.InlineKeyboardButton(text=dta[user]['name'], callback_data=user)
        keyboard.add(button)

    button_back = types.InlineKeyboardButton(text='Назад', callback_data='Back')
    keyboard.add(button_back)
    if message.chat.id in STAFF_ID:
        bot.send_message(message.chat.id, text='Какой ученик?', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def check_callback_data(callback: CallbackQuery):
    with open('C:/Users/matve/PycharmProjects/CreateSite/Bot/data.json', 'r') as jsonFile:
        dta = json.load(jsonFile)

    if callback.data == 'last_dz':
        user_id = str(callback.message.chat.id)
        user_name = dta[user_id]["name"]

        if str(user_id) in dta:
            if len(dta[user_id]["dz-task"]) != 0:
                file_name = dta[user_id]["dz-task"][-1]
                os.chdir('C:/files/bot/' + user_name + '/')
                file = open(file_name, 'rb')
                bot.send_message(callback.message.chat.id, text='Вот твое дз')
                bot.send_document(callback.message.chat.id, file)
                os.chdir('C:/Users/matve/PycharmProjects/CreateSite/Bot')
            else:
                bot.send_message(callback.message.chat.id, text='Для тебя еще нету домашек!')
        else:
            bot.send_message(callback.message.chat.id,
                             text=f'{user_id}, Сначала тебе нужно ввести команду "/start"!')

    if callback.data == 'check_dz':
        choice_dz_for_answer(callback.message)

    if callback.data == 'all_dz':
        user_id = str(callback.message.chat.id)
        user_name = dta[user_id]["name"]
        dz_tasks = dta[user_id]["dz-task"]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        for dz_task in dz_tasks:
            button = types.InlineKeyboardButton(text=dz_task, callback_data='download'+dz_task)
            keyboard.add(button)
        bot.send_message(callback.message.chat.id, text='Выбери нужный файл:', reply_markup=keyboard)

    if callback.data[:10] == 'downloaddz':
        user_name = dta[str(callback.message.chat.id)]["name"]
        os.chdir('C:/files/bot/' + user_name + '/')
        file_name = callback.data[8:]
        with open(file_name, 'rb') as dz_file:
            bot.send_document(callback.message.chat.id, dz_file)
            os.chdir('C:/Users/matve/PycharmProjects/CreateSite/Bot')


    if callback.data[:2] == 'dz':
        dz_number = int(callback.data[3:]) - 1

        try:
            answers = dta[str(callback.message.chat.id)]["dz_answers"][dz_number]
            sent = bot.send_message(callback.message.chat.id, text=f'Вводи ответы для работы {callback.data}')
            bot.register_next_step_handler(sent, check_answers, answers, callback.data)
        except Exception:
            bot.send_message(ADMIN_CHAT_ID, text=f'{callback.message.chat.id} не сходится номер дз и количество ответов')
            bot.send_message(callback.message.chat.id, text='Проблема на стороне сервера')
    if callback.data == 'download_dz':
        download_dz(callback.message)

    for user in dta:
        if callback.data == user:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            button_back = types.InlineKeyboardButton(text='Назад', callback_data='Back')
            keyboard.add(button_back)

            user_name = dta[user]['name']
            sent = bot.send_message(callback.message.chat.id,
                                    text='Загрузка домашней работы для <b>' + user_name + "</b>!" + '\n\n' + 'Отправьте мне файл с дз!',
                                    parse_mode='HTML', reply_markup=keyboard)
            bot.register_next_step_handler(sent, downloader_task, user)

    if callback.data == 'Back':
        navigation(callback.message)

    if callback.data == 'input_answer_again':
        choice_dz_for_answer(callback.message)

    if callback.data == 'len_answers_not_correct':
        bot.send_message(ADMIN_CHAT_ID, text=f'len_answers_not_correct у пользователя {callback.message.chat.id}')
        bot.send_message(callback.message.chat.id, text='Попытаемся исправить ошибку! Проверим домашнюю работу на занятиии.')

def check_answers(message: Message, correct_answers, file_name):
    with open('data.json', 'r') as jsonFile:
        dta = json.load(jsonFile)

    student_answers = message.text.split()

    if len(student_answers) != len(correct_answers):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(text='Попробовать ввести ответ еще раз', callback_data='input_answer_again')
        button2 = types.InlineKeyboardButton(text='Какая-то ошибка', callback_data='len_answers_not_correct')
        keyboard.add(button1, button2)
        bot.send_message(message.chat.id,
                         text='Количество ответов не совпадает с количеством заданий. '
                              'Перепроверь себя или нажми кнопку: "Какая-то ошибка?"',
                         reply_markup=keyboard)
    else:
        counter_corrent_answers = 0
        wrong_asnwers = []
        answer_not_given = []
        for num in range(len(correct_answers)):
            if correct_answers[num] == student_answers[num]:
                counter_corrent_answers += 1
            elif student_answers[num] == '-':
                answer_not_given.append(num + 1)
            else:
                wrong_asnwers.append(num + 1)
        keyboard = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='Назад', callback_data='Back')
        bot.send_message(ADMIN_CHAT_ID, text=f'<b>{dta[str(message.chat.id)]["name"]}</b> дал ответ на {file_name}.'
                                             f'Ответ верно дан на {counter_corrent_answers} из {len(correct_answers)}, '
                                             f'ошибся в {str([number for number in wrong_asnwers])[1:-1]}.', parse_mode='HTML')
        bot.send_message(message.chat.id, text=f'Домашняя работа проверена! Ответ верно дан на {counter_corrent_answers}'
                                               f' из {len(correct_answers)}. Ты ошибся в '
                                               f'{str([number for number in wrong_asnwers])[1:-1]}.', reply_markup=keyboard)
def downloader_answers(message: Message, user):
    with open('data.json', 'r') as jsonFile:
        dta = json.load(jsonFile)

    answers = message.text.split()
    dta[user]['dz_answers'].append(list(answer for answer in answers))

    with open('data.json', 'w') as jsonFile:
        json.dump(dta, jsonFile, indent=4, ensure_ascii=True)

    bot.send_message(message.chat.id, text='Ответы загружены!')


def registration(message: Message):
    fio = message.text.split()
    user_id = str(message.from_user.id)
    if len(fio) == 2:
        with open('data.json', 'r') as jsonFile:
            dta = json.load(jsonFile)

        dta[user_id]['name'] = fio[0] + ' ' + fio[1][0]

        with open('data.json', 'w') as jsonFile:
            json.dump(dta, jsonFile, indent=4, ensure_ascii=True)

        navigation(message)
    else:
        bot.send_message(message.chat.id,
                         text="Данные введены неверно. Сообщение должно состоять из двух слов: Имя и Фамилия!")
        sent = bot.send_message(message.chat.id,
                                text="Введите имя и фамилию. \n\n <b>Например: </b> <i>Иван Иванов</i>",
                                parse_mode='HTML')
        bot.register_next_step_handler(sent, registration)


def downloader_task(message: Message, user):
    os.chdir('C:/Users/matve/PycharmProjects/CreateSite/Bot')
    with open('data.json', 'r') as jsonFile:
        dta = json.load(jsonFile)

    user_name = dta[user]['name']

    try:
        file_info = bot.get_file(message.document.file_id)
        downloded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name

        os.chdir('C:/files/bot/')
        if not os.path.isdir(user_name):
            os.mkdir(user_name)

        os.chdir('C:/Users/matve/PycharmProjects/CreateSite/Bot')
        src = 'C:/files/bot/' + user_name + '/' + message.document.file_name

        with open(src, 'wb') as new_file:
            new_file.write(downloded_file)

        os.chdir('C:/files/bot/' + user_name + '/')
        new_file_name = 'dz-' + str(len(dta[user]['dz-task']) + 1) + '.pdf'
        os.rename(file_name, new_file_name)


        dta[user]['dz-task'].append(new_file_name)
        os.chdir('C:/Users/matve/PycharmProjects/CreateSite/Bot')
        with open('data.json', 'w') as jsonFile:
            json.dump(dta, jsonFile, indent=4, ensure_ascii=True)

        sent = bot.send_message(message.chat.id,
                                text='Супер! Домашняя работа загрузилась и уже доставлена ученику! Пора загрузить ответы. \n\n Ответы вводятся <b>одной</b> строкой, разделяются <b>одним</b> пробелом. Количество ответов должно совпадать с количеством заданий!',
                                parse_mode='HTML')
        #scr = 'C:/files/bot/' + user_name + '/' + new_file_name
        #with open(scr, 'r') as file:
        #    dz_file = json.load(file)
        #os.chdir('C:/Users/matve/PycharmProjects/CreateSite/Bot')
        bot.send_message(user, text='У вас новое домашнее задание!')
        #bot.send_document(user, document=dz_file)
        bot.register_next_step_handler(sent, downloader_answers, user)
    except Exception as e:
        bot.send_message(message.chat.id, 'Ошибка! Уже ее исправляем.')
        bot.send_message(ADMIN_CHAT_ID, e)
        download_dz(message)

bot.polling()
