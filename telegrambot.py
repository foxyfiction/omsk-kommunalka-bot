# -*- coding: utf-8 -*-
# this file contains a code
import telebot
import config

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def show_start_message(message):
    hello_message = "Добро пожаловать! \n " \
                    "Базовые команды \n" \
                    "/list_all_tickets \n" \
                    "/help"
    bot.send_message(message.chat.id, hello_message)


@bot.message_handler(commands=['help'])
def show_start_message(message):
    help_message = "АХТУНГ!!! \n" \
                   "/list_all_tickets - показать список существующих квитанций \n" \
                   "/list_tickets - просмотр активных квитанций \n" \
                   "/days - установка числа - за сколько дней необходимо начать присылать напоминание \n" \
                   "/clear - сброс параметров\n" \
                   "/help - список всех команд "
    bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=['list_all_tickets'])
def show_start_message(message):
    list_all_tickets_message = "1. Интернет /t_1 \n" \
                               "2. Домофон /t_2 \n" \
                               "3. Антенна (ТВ) /t_3 \n" \
                               "4. Газ /t_4 \n" \
                               "5. Электроэнергия /t_5 \n" \
                               "6. Холодная вода /t_6 \n" \
                               "7. Горячая вода /t_7 \n" \
                               "8. Отопление /t_8 \n" \
                               "9. Управляющие компании (ТСЖ, ЖКО) /t_9 \n" \
                               "10. Капитальный ремонт /t_10 \n" \
                               "11. Стоянка /t_11 \n" \
                               "12. Телефон /t_12 \n" \
                               "13. Охрана /t_13 \n" \
                               "14. Кабельное/спутниковое ТВ /t_14 \n" \
                               "15. Арендная плата /t_15 \n" \
                               "16. Штраф /t_16 \n" \
                               "17. Мобильная связь /t_17 \n" \
                               "18. Садик /t_18 \n" \
                               "19. Школа /t_19 \n"
    bot.send_message(message.chat.id, list_all_tickets_message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
