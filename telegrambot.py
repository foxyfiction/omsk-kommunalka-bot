# -*- coding: utf-8 -*-
import psycopg2
import telebot
from telebot import types

import config

connect = psycopg2.connect(database='d1eam1hffgoggg',
                           user='ravnyccawkzsbx',
                           host='ec2-54-235-246-67.compute-1.amazonaws.com',
                           password='0lo2zjah68Y2pHef7jRrh9KjqO')
cursor = connect.cursor()

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def show_start_message(message):
    user_is_not_alive = True
    cursor.execute("select id_user " \
                   "from users " \
                   "where id_user=" + str(message.chat.id))
    for row in cursor:
        user_is_not_alive = False
    if (user_is_not_alive):
        cursor.execute("insert into users (id_user, days) values (" + str(message.chat.id) + ",5)")
        connect.commit()
    hello_message = "Добро пожаловать! \n " \
                    "/help - команды \n" \
                    "/list_all_tickets - доступные квитанции\n"
    bot.send_message(message.chat.id, hello_message)


@bot.message_handler(commands=['help'])
def show_start_message(message):
    help_message = "/list_all_tickets - показать список существующих квитанций \n" \
                   "/list_tickets - просмотр активных квитанций \n" \
                   "/days - установка числа - за сколько дней необходимо начать присылать напоминание \n" \
                   "/clear - удалить все активные квитанции\n" \
                   "/help - список всех команд "
    bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=['days'])
def show_start_message(message):
    cursor.execute("select days from users where id_user=" + str(message.chat.id))
    for row in cursor:
        days = row[0]
    days_message = "В течение " + str(days) + " дней будет приходить напоминание об оплате квитанции. "
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('да')
    markup.row('нет')
    msg = bot.send_message(message.chat.id, days_message + "Хотите изменить это число?", reply_markup=markup)
    bot.register_next_step_handler(msg, response_change_days)


def response_change_days(message):
    if (message.text == 'да'):
        msg = bot.send_message(message.chat.id, "Введите число: ")
        bot.register_next_step_handler(msg, change_days)


def change_days(message):
    cursor.execute("Update users set days=" + str(message.text) + " where id_user=" + str(message.chat.id))
    connect.commit()
    bot.send_message(message.chat.id, "Число изменено.")


@bot.message_handler(commands=['list_all_tickets'])
def show_start_message(message):
    cursor.execute("SELECT ticket_name, active_row FROM all_tickets;")
    list_all_tickets_message = ""
    for row in cursor:
        list_all_tickets_message = list_all_tickets_message + row[0].strip() + " " + row[1] + "\n"
    bot.send_message(message.chat.id, list_all_tickets_message)


@bot.message_handler(commands=['list_tickets'])
def show_start_message(message):
    cursor.execute("select all_tickets.ticket_name, " \
                   "all_tickets.active_row " \
                   "from all_tickets " \
                   "left outer join user_tickets " \
                   "on user_tickets.id_ticket=all_tickets.id_ticket " \
                   "where user_tickets.id_user=" + str(message.chat.id))
    list_tickets_message = ""
    for row in cursor:
        list_tickets_message = list_tickets_message + row[0].strip() + " " + row[1] + "\n"
    if list_tickets_message != "":
        bot.send_message(message.chat.id, "Список ваших активных квитанций: \n" + list_tickets_message)
    else:
        bot.send_message(message.chat.id, "Вы еще не подключили ни одной квитанции." \
                                          " Для того, что бы активировать квитанцию, перейдите в /list_all_tickets")


@bot.message_handler(commands=['t_1', 't_2', 't_3', 't_4', 't_5', 't_6', 't_7', 't_8', 't_9', 't_10', 't_11'])
def add_ticket(message):
    cursor.execute("select user_tickets.id_user, all_tickets.active_row " \
                   "from user_tickets " \
                   "left outer join all_tickets " \
                   "on all_tickets.id_ticket=user_tickets.id_ticket " \
                   "where user_tickets.id_user=" + str(message.chat.id))
    for row in cursor:
        if ((str(row[0]) == str(message.chat.id)) and (str(row[1]).strip() == str(message.text))):
            bot.send_message(message.chat.id, "Квитанция " + message.text + " у вас есть")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.row('Удалить ' + message.text)
            markup.row('Нет ')
            msg = bot.send_message(message.chat.id, "Удалить квитанцию?", reply_markup=markup)
            bot.register_next_step_handler(msg, delete_active_ticket)
            return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('Добавить ' + message.text)
    markup.row('Нет ')
    msg = bot.send_message(message.chat.id, "Добавить квитанцию?", reply_markup=markup)
    bot.register_next_step_handler(msg, add_active_ticket)


def delete_active_ticket(message):
    try:
        answer, ticket = message.text.split()
    except ValueError:
        return
    if answer == "Нет":
        return
    if answer == "Удалить":
        cursor.execute("select id_ticket from all_tickets where active_row =" + "\'" + ticket + "\'")
        for new_row in cursor:
            id_ticket = new_row[0]
        cursor.execute(
                "delete from user_tickets where id_user=" + str(message.chat.id) + " and id_ticket=" + str(id_ticket))
        connect.commit()
        bot.send_message(message.chat.id, "Квитанция " + ticket + " удалена!")


def add_active_ticket(message):
    try:
        answer, ticket = message.text.split(' ')
    except ValueError:
        return
    if answer == "Нет":
        return
    if answer == "Добавить":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row('Да ' + ticket)
        markup.row('Нет ' + ticket)
        msg = bot.send_message(message.chat.id,
                               "По умолчанию до 10го числа каждого месяца будут приходит напоминания. Хотите изменить эту дату? ",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, add_user_ticket_with_finish_data)


def add_user_ticket_with_finish_data(message):
    try:
        answer, ticket = message.text.split(' ')
    except ValueError:
        return
    if answer == "Нет":
        cursor.execute("select id_ticket from all_tickets where active_row =" + "\'" + ticket + "\'")
        for new_row in cursor:
            id_ticket = new_row[0]
        cursor.execute("insert into user_tickets "
                       "(id_user, id_ticket, finish_date) "
                       "values (" + str(message.chat.id) + ","
                       + str(id_ticket) + "," + str(10) + ")")
        connect.commit()
        bot.send_message(message.chat.id, "Квитанция " + ticket + " добавлена!")
    if answer == "Да":
        msg = bot.send_message(message.chat.id, "Введите число: ")
        bot.register_next_step_handler(msg, lambda message: finish_day(ticket, message))


def finish_day(ticket, message):
    cursor.execute("select id_ticket from all_tickets where active_row =" + "\'" + ticket + "\'")
    for new_row in cursor:
        id_ticket = new_row[0]
    cursor.execute("insert into user_tickets "
                       "(id_user, id_ticket, finish_date) "
                       "values (" + str(message.chat.id) + ","
                       + str(id_ticket) + "," + str(message.text) + ")")
    connect.commit()
    bot.send_message(message.chat.id, "Квитанция " + ticket + " добавлена!")


@bot.message_handler(commands=['clear'])
def show_start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('да')
    markup.row('нет')
    msg = bot.send_message(message.chat.id, "Хотите удалить все активные квитанции?", reply_markup=markup)
    bot.register_next_step_handler(msg, clear)


def clear(message):
    if (message.text == 'да'):
        cursor.execute("delete from user_tickets where id_user=" + str(message.chat.id))
        connect.commit()
        bot.send_message(message.chat.id, "Ваши активные квитанции удалены")


if __name__ == '__main__':
    bot.polling(none_stop=True)

connect.close()
