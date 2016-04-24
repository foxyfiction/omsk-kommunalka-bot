# -*- coding: utf-8 -*-
import datetime

import psycopg2
import telebot

import config

month_dict = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'бобобря',
    11: 'ноября',
    12: 'декабря'
}


connect = psycopg2.connect(database='d1eam1hffgoggg',
                           user='ravnyccawkzsbx',
                           host='ec2-54-235-246-67.compute-1.amazonaws.com',
                           password='0lo2zjah68Y2pHef7jRrh9KjqO')
cursor = connect.cursor()

bot = telebot.TeleBot(config.token)

if __name__ == '__main__':

    date = datetime.date.today()
    today_day = date.day
    month = date.month
    year = date.year

    cursor.execute("select id_user,days from users")
    for id_user_days in cursor:
        id_user = id_user_days[0]
        days = id_user_days[1]
        cursor_ticket = connect.cursor()
        cursor_ticket.execute("select all_tickets.ticket_name," \
                                          " user_tickets.finish_date " \
                                          "from user_tickets " \
                                          "right outer join all_tickets " \
                                          "on user_tickets.id_ticket=all_tickets.id_ticket " \
                                          "where id_user =" + str(id_user))


        connect_option=False

        cursor_for_option = connect.cursor()
        cursor_for_option.execute("select id_user from user_notification where id_user ="+str(id_user))
        for row in cursor_for_option:
            connect_option=True
        if connect_option:
            optimal_date=31
            for ticket_data in cursor_ticket:
                ticket_name = ticket_data[0]
                finish_date = ticket_data[1]
                if int(finish_date)<int(optimal_date):
                    optimal_date=finish_date
            try:
                day_of_date = datetime.date(year, month, int(optimal_date))
            except ValueError:
                if (month == 2):
                    day_of_date = datetime.date(year, month + 1, int(optimal_date) - 3)
                else:
                    day_of_date = datetime.date(year, month, int(optimal_date) - 1)

            try:
                day_of_date_before_month = datetime.date(year, month + 1, int(optimal_date))
            except ValueError:
                if (month == 2):
                    day_of_date_before_month = datetime.date(year, month + 1, int(optimal_date) - 3)
                else:
                    day_of_date_before_month = datetime.date(year, month + 1, int(optimal_date) - 1)

            if int(today_day) <= int(optimal_date):
                if (day_of_date - datetime.timedelta(days=int(days)) <= date) and (date <= day_of_date):
                    bot.send_message(int(id_user), "Необходимо оплатить квитанции до " +
                                     str(optimal_date) + " " + month_dict[month])

            if int(today_day) > int(optimal_date):
                if (day_of_date_before_month - datetime.timedelta(days=int(days)) <= date) and (
                            date <= day_of_date_before_month):
                    bot.send_message(int(id_user), "Необходимо оплатить квитанции до " +
                                     str(optimal_date) + " " + month_dict[month+1])



        else:
            for ticket_data in cursor_ticket:
                ticket_name = ticket_data[0]
                finish_date = ticket_data[1]
                try:
                    day_of_date = datetime.date(year, month, int(finish_date))
                except ValueError:
                    if (month == 2):
                        day_of_date = datetime.date(year, month + 1, int(finish_date) - 3)
                    else:
                        day_of_date = datetime.date(year, month, int(finish_date) - 1)

                try:
                    day_of_date_before_month = datetime.date(year, month + 1, int(finish_date))
                except ValueError:
                    if (month == 2):
                        day_of_date_before_month = datetime.date(year, month + 1, int(finish_date) - 3)
                    else:
                        day_of_date_before_month = datetime.date(year, month + 1, int(finish_date) - 1)

                if int(today_day) <= int(finish_date):
                    if (day_of_date - datetime.timedelta(days=int(days)) <= date) and (date <= day_of_date):
                        bot.send_message(int(id_user), "Необходимо оплатить квитанцию \"" + ticket_name.strip() + "\"" +
                                         " до " + str(finish_date) + " " + month_dict[month])

                if int(today_day) > int(finish_date):
                    if (day_of_date_before_month - datetime.timedelta(days=int(days)) <= date) and (
                                date <= day_of_date_before_month):
                        bot.send_message(int(id_user), "Необходимо оплатить квитанцию \"" + ticket_name.strip() + "\"" +
                                         " до " + str(finish_date) + " " + month_dict[month + 1])

connect.close()
