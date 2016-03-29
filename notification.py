# -*- coding: utf-8 -*-
import telebot
import config
import psycopg2
import time
from telebot import types

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
        print(id_user)
        print(days)
       # bot.send_message(int(id_user), 'I Love you very much! Take you money!')
        cursor_ticket = connect.cursor()
        cursor_ticket.execute("select all_tickets.ticket_name," \
                       " user_tickets.finish_date " \
                       "from user_tickets " \
                       "right outer join all_tickets " \
                       "on user_tickets.id_ticket=all_tickets.id_ticket " \
                       "where id_user =" + str(id_user))
        for ticket_data in cursor_ticket:
            ticket_name=ticket_data[0]
            finish_date=ticket_data[1]
            print(ticket_name,finish_date)
            if (int(finish_date)-int(days) <= int(time.strftime("%d")) and
            int(time.strftime("%d")) < int(finish_date)):
                bot.send_message(int(id_user), "Необходимо оплатить квитанцию \""+ ticket_name.strip() + "\"")

connect.close()