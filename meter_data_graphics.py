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
    meter_data = ["112.31",
                  "114.09",
                  "115.76",
                  "116.98",
                  "117.76",
                  "118.88",
                  "119.56",
                  "120.45"]

    delta_meter_data = []
    i = len(meter_data) - 1
    while i:
        delta_meter_data.append(float(meter_data[i]) - float(meter_data[i - 1]))
        i -= 1
    return draw_graphics(delta_meter_data)
    # close cursor


def draw_graphics(delta_meter_data):
    fig = plt.figure()   # Создание объекта Figure
    plt.plot(delta_meter_data)
    name = '1'
    fmt = 'png'
    save(name, fmt)
    return '%s.%s' % (name, fmt)


def save(name='', fmt='png'):
    pwd = os.getcwd()
    plt.savefig('%s.%s' % (name, fmt), fmt='png')
    os.chdir(pwd)
    #plt.close()