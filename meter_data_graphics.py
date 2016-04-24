# -*- coding: utf-8 -*-
import datetime
import psycopg2
import matplotlib as mpl
import os
import matplotlib.pyplot as plt

import config


# Method collect gas meter data from database
def draw_meter_data_gas():
    """
    it will be there if the future:
    connect to database
    create a cursor
    select from database and form list meter_data
    """
    # for experiments we use gas meter data
    meter_data = ["112.31", "114.09", "115.76", "116.98"]
    draw_graphics(meter_data)
    # close cursor
    pass


def draw_graphics(meter_data):
    for value in meter_data:
        pass
    fig = plt.figure()   # Создание объекта Figure
    print(fig.axes)   # Список текущих областей рисования пуст
    print(type(fig))   # тип объекта Figure
    plt.scatter(1.0, 1.0)   # scatter - метод для нанесения маркера в точке (1.0, 1.0)

    # После нанесения графического элемента в виде маркера
    # список текущих областей состоит из одной области
    print(fig.axes)

    plt.show()


def save(name='', fmt='png'):
    pwd = os.getcwd()
    os.chdir('./pictures/%s' % fmt)
    plt.savefig('%s.%s' % (name, fmt), fmt='png')
    os.chdir(pwd)
    #plt.close()

draw_meter_data_gas()