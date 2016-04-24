# -*- coding: utf-8 -*-
# imports: libraries
import psycopg2
import telebot
from telebot import types

# imports: modules and configuration files
import config
import meter_reading_module
import meter_data_graphics


# connection to database on Heroku (Heroku Postgres)
connect = psycopg2.connect(database='d1eam1hffgoggg',
                           user='ravnyccawkzsbx',
                           host='ec2-54-235-246-67.compute-1.amazonaws.com',
                           password='0lo2zjah68Y2pHef7jRrh9KjqO')
cursor = connect.cursor()

# create a bot (token was generated by BotFather)
bot = telebot.TeleBot(config.token)


# start method - run when user send start
# There is description of bot's functionality
@bot.message_handler(commands=['start'])
def show_start_message(message):
    user_is_not_alive = True
    cursor.execute("select id_user " +
                   "from users " +
                   "where id_user=" + str(message.chat.id))
    for row in cursor:
        user_is_not_alive = False
    if user_is_not_alive:
        cursor.execute("insert into users (id_user, days) values (" + str(message.chat.id) + ",5)")
        connect.commit()
    hello_message = "Добро пожаловать!\n" \
                    "/help - команды\n" \
                    "/bills_types - доступные квитанции\n"
    bot.send_message(message.chat.id, hello_message)


# Send list of all commands with descriptions
@bot.message_handler(commands=['help'])
def show_start_message(message):
    help_message = "/bills_types - показать список существующих квитанций \n" \
                   "/active_bills - просмотр активных квитанций \n" \
                   "/days - установка числа - за сколько дней необходимо начать присылать напоминание \n" \
                   "/clear - удалить все активные квитанции\n" \
                   "/help - список всех команд "
    bot.send_message(message.chat.id, help_message)


# Send 'days' and offer to enter new value
# 'days' is a number, if finish date is 12 and days is 3, then bot will send notifications since 10 to 12 days of month
# or since 9 to 11 ???????
@bot.message_handler(commands=['days'])
def show_start_message(message):
    cursor.execute("select days from users where id_user=" + str(message.chat.id))
    days = None
    for row in cursor:
        days = row[0]
    days_message = "В течении " + str(days) + " дней будет приходить напоминание об оплате квитанции."
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('Да')
    markup.row('Нет')
    msg = bot.send_message(message.chat.id, days_message + "Хотите изменить это число?", reply_markup=markup)
    bot.register_next_step_handler(msg, response_change_days)


def response_change_days(message):
    if message.text == 'Да':
        msg = bot.send_message(message.chat.id, "Введите число: ")
        bot.register_next_step_handler(msg, change_days)


def change_days(message):
    if message.text.isdigit():
        if int(message.text > 0 and int(message.text) < 25):
            cursor.execute("Update users set days=" + str(message.text) + " where id_user=" + str(message.chat.id))
            connect.commit()
            bot.send_message(message.chat.id, "Число изменено.")
            return
        else:
            msg = bot.send_message(message.chat.id, "Days может быть в пределах от 0 до 25 :( \nВведите число: ")
    else:
        msg = bot.send_message(message.chat.id, "Вы уверены, что ввели число? \nВведите число: ")
    bot.register_next_step_handler(msg, change_days)


# Show all bill's types, which is available in database
@bot.message_handler(commands=['bills_types'])
def show_start_message(message):
    cursor.execute("SELECT ticket_name, active_row FROM all_tickets;")
    bills_types_message = ""
    for row in cursor:
        bills_types_message = bills_types_message + row[0].strip() + " " + row[1] + "\n"
    bot.send_message(message.chat.id, bills_types_message)


# Show all active bills
# Active bills is a bills, that the user added
@bot.message_handler(commands=['active_bills'])
def show_start_message(message):
    cursor.execute("select all_tickets.active_row, " +
                   "all_tickets.ticket_name, " +
                   "user_tickets.finish_date " +
                   "from all_tickets " +
                   "left outer join user_tickets " +
                   "on user_tickets.id_ticket=all_tickets.id_ticket " +
                   "where user_tickets.id_user=" + str(message.chat.id))
    active_bills_message = ""
    for row in cursor:
        active_bills_message = active_bills_message + row[0].strip() + " " + row[1].strip() + " оплатить до " + \
                               str(row[2]) + " числа"+"\n"
    if active_bills_message != "":
        bot.send_message(message.chat.id, "Список ваших активных квитанций: \n" + active_bills_message)
    else:
        bot.send_message(message.chat.id, "Вы еще не подключили ни одной квитанции." +
                                          " Для того, чтобы активировать квитанцию, перейдите в /bills_types")


# Send a message: delete or add a bill
@bot.message_handler(commands=['t_1', 't_2', 't_3', 't_4', 't_5', 't_6', 't_7', 't_8', 't_9', 't_10', 't_11'])
def add_ticket(message):
    cursor.execute("select user_tickets.id_user, all_tickets.active_row " +
                   "from user_tickets " +
                   "left outer join all_tickets " +
                   "on all_tickets.id_ticket=user_tickets.id_ticket " +
                   "where user_tickets.id_user=" + str(message.chat.id))
    for row in cursor:
        if (str(row[0]) == str(message.chat.id)) and (str(row[1]).strip() == str(message.text)):
            bot.send_message(message.chat.id, "Квитанция " + message.text + " у вас есть")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.row('Удалить ' + message.text)
            markup.row('Нет ')
            msg = bot.send_message(message.chat.id, "Удалить квитанцию?", reply_markup=markup)
            bot.register_next_step_handler(msg, delete_active_bill)
            return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('Добавить ' + message.text)
    markup.row('Нет ')
    msg = bot.send_message(message.chat.id, "Добавить квитанцию?", reply_markup=markup)
    bot.register_next_step_handler(msg, add_available_bill)


def delete_active_bill(message):
    try:
        answer, bill = message.text.split()
    except ValueError:
        return
    if answer == "Нет":
        return
    if answer == "Удалить":
        cursor.execute("select id_ticket from all_tickets where active_row =" + "\'" + bill + "\'")
        id_bill = None
        for new_row in cursor:
            id_bill = new_row[0]
        cursor.execute(
                "delete from user_tickets where id_user=" + str(message.chat.id) + " and id_ticket=" + str(id_bill))
        connect.commit()
        bot.send_message(message.chat.id, "Квитанция " + bill + " удалена!")


def add_available_bill(message):
    try:
        answer, bill = message.text.split(' ')
    except ValueError:
        return
    if answer == "Нет":
        return
    if answer == "Добавить":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row('Да')
        markup.row('Нет')
        msg = bot.send_message(message.chat.id,
                               "По умолчанию до 10го числа каждого месяца будут приходить напоминания.\n" +
                               "Хотите изменить эту дату?",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, lambda message: add_available_bill_with_finish_data(message, bill))


def add_available_bill_with_finish_data(message, bill):
    answer = message.text
    if answer == "Нет":
        cursor.execute("select id_ticket from all_tickets where active_row =" + "\'" + bill + "\'")
        id_bill = None
        for new_row in cursor:
            id_bill = new_row[0]
        cursor.execute("insert into user_tickets "
                       "(id_user, id_ticket, finish_date) "
                       "values (" + str(message.chat.id) + ","
                       + str(id_bill) + "," + str(10) + ")")
        connect.commit()
        bot.send_message(message.chat.id, "Квитанция " + bill + " добавлена!")
    if answer == "Да":
        msg = bot.send_message(message.chat.id, "Введите число: ")
        bot.register_next_step_handler(msg, lambda message: finish_day(bill, message))


def finish_day(bill, message):
    if message.text.isdigit():
        if 1 <= int(message.text) <= 31:
            cursor.execute("select id_ticket from all_tickets where active_row =" + "\'" + bill + "\'")
            id_bill = None
            for new_row in cursor:
                id_bill = new_row[0]
            cursor.execute("insert into user_tickets " +
                           "(id_user, id_ticket, finish_date) "
                           "values (" + str(message.chat.id) + "," +
                           str(id_bill) + "," + str(message.text) + ")")
            connect.commit()
            bot.send_message(message.chat.id, "Квитанция " + bill + " добавлена!")
            return
        else: msg = bot.send_message(message.chat.id, "Число должно быть в пределах от 1 до 31!" + "\nВведите число: ")
    else:
        msg = bot.send_message(message.chat.id, "Не обижай ботю, в следующий раз введи число!" + "\nВведите число: ")
    bot.register_next_step_handler(msg, lambda message: finish_day(bill, message))


# Delete all user's active bills
@bot.message_handler(commands=['clear'])
def show_start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row('Да')
    markup.row('Нет')
    msg = bot.send_message(message.chat.id, "Хотите удалить все активные квитанции?", reply_markup=markup)
    bot.register_next_step_handler(msg, clear)


def clear(message):
    if message.text == 'Да':
        cursor.execute("delete from user_tickets where id_user=" + str(message.chat.id))
        connect.commit()
        bot.send_message(message.chat.id, "Ваши активные квитанции удалены")


@bot.message_handler(commands=['graphics'])
def send_graphics(message):
    graphic = open(meter_data_graphics.draw_meter_data_gas(), 'rb')
    bot.send_photo(message.chat.id, graphic)
    graphic.close()


if __name__ == '__main__':
    bot.polling(none_stop=True)


connect.close()
