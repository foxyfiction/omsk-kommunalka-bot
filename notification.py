# -*- coding: utf-8 -*-
import datetime

import psycopg2
import telebot

import config

connect = psycopg2.connect(database='d1eam1hffgoggg',
                           user='ravnyccawkzsbx',
                           host='ec2-54-235-246-67.compute-1.amazonaws.com',
                           password='0lo2zjah68Y2pHef7jRrh9KjqO')
cursor = connect.cursor()

bot = telebot.TeleBot(config.token)

if __name__ == '__main__':
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
        for ticket_data in cursor_ticket:
            ticket_name = ticket_data[0]
            finish_date = ticket_data[1]

            date = datetime.date.today()
            today_day = date.day
            month = date.month
            year = date.year

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
                    bot.send_message(int(id_user), "Необходимо оплатить квитанцию \"" + ticket_name.strip() + "\"")

            if int(today_day) > int(finish_date):
                if (day_of_date_before_month - datetime.timedelta(days=int(days)) <= date) and (
                            date <= day_of_date_before_month):
                    bot.send_message(int(id_user), "Необходимо оплатить квитанцию \"" + ticket_name.strip() + "\"")

connect.close()
