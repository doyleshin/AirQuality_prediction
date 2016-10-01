# -*- conding: utf-8 -*-

import os
import csv
import pandas as pd
import numpy as np
from random import random

"""
    GET DATA LIST ON FOLDER
    * Input value   : folder
    * Process       : open .csv files from folder, get sensor list and sort
    * Return value  : Pandas DataFrame
"""
def get_data_list_on_folder(folder, complete_set=False):
    folder_list = os.listdir(folder)
    data_list = []

    # get item list from folder
    for csvs in folder_list:
        with open(str(folder + '/' + csvs), 'r') as csvfile:
            i = 0
            sensor_data = csv.reader(csvfile, quotechar='"')
            for data in sensor_data:
                data_list.append(data)
                i += 1
                if (i % 100000 == 0):
                    print('Load %dK list from %s.' % (i/1000, csvs))
            print('%s done.' % (csvs))

    # print & sort data / Sort by a time
    print('Sorting...')
    data_list = sorted(data_list, key=lambda data_list:data_list[1])
    print('Set Dataframe...')
    # set dataframe on pandas
    Dust = []
    Light = []
    VoC = []
    Co2 = []
    Temp = []
    Humid =[]
    # uncertain value
    E = []
    Oxy = []
    X = []
    R = []
    M = []
    for sensor in data_list:
        kind = sensor[6] # D,L,V,C,T,H
        value = sensor[4]
        if (kind == "D"):
            Dust.append(value)
        elif (kind == "L"):
            Light.append(value)
        elif (kind == "V"):
            VoC.append(value)
        elif (kind == "C"):
            Co2.append(value)
        elif (kind == "T"):
            Temp.append(value)
        elif (kind == "H"):
            Humid.append(value)
        elif (kind == "E"):
            E.append(value)
        elif (kind == "O"):
            Oxy.append(value)
        elif (kind == "X"):
            X.append(value)
        elif (kind == "R"):
            R.append(value)
        elif (kind == "M"):
            M.append(value)
        else:
            print("[Warning] sensor error in %s. Please check commons.py 58 line." % str(sensor))
    print("[Note] Result <D: %d, L: %d, V: %d, C: %d, T: %d, H: %d, E: %d, O: %d, X: %d, R: %d, M: %d>" %
          (len(Dust), len(Light), len(VoC), len(Co2), len(Temp), len(Humid), len(E), len(Oxy), len(X), len(R), len(M)))

    # Setting Data
    if (complete_set is False):
        min_line = min(len(Dust), len(Light), len(VoC), len(Co2), len(Temp), len(Humid))
        min_line -= 1
        data = pd.DataFrame({"D": Dust[:min_line], "L": Light[:min_line], "V": VoC[:min_line], "C": Co2[:min_line],
                            "T": Temp[:min_line], "H": Humid[:min_line]})
    elif (complete_set is True):
        min_line = min(len(Dust), len(Light), len(VoC), len(Co2), len(Temp), len(Humid), len(E), len(Oxy), len(X), len(R), len(M))
        min_line -= 1
        data = pd.DataFrame({"D": Dust[:min_line], "L": Light[:min_line], "V": VoC[:min_line], "C": Co2[:min_line],
                            "T": Temp[:min_line], "H": Humid[:min_line], "E": E[:min_line], "O": Oxy[:min_line],
                            "X": X[:min_line], "R": R[:min_line], "M": M[:min_line]})

    print('[DONE] Returned %d items from %s' % (len(data_list), folder))
    return data

"""
    _load_data
    * Note: Data should be pd.DataFrame()
    * Input value:
        - data = pd.DataFrame()
        - n_prev = # of previous consider value (Default is 100) as a Learning Set (like corpus)
    * Output value:
        - training matrix(numpy array)
"""
def _load_data(data, n_prev = 100):
    docX, docY = [], []
    for i in range(len(data)-n_prev):
        docX.append(data.iloc[i:i+n_prev].as_matrix())
        docY.append(data.iloc[i+n_prev].as_matrix())
    alsX = np.array(docX)
    alsY = np.array(docY)

    return alsX, alsY

"""
    train_test_split
"""
def train_test_split(df, fold_size=0.1, time_steps=100):
    print('[Note] Setting Train/Test set separation.')
    ntrn = round(len(df) * (1 - fold_size))
    X_train, y_train = _load_data(df.iloc[0:ntrn], n_prev=time_steps)
    X_test, y_test = _load_data(df.iloc[ntrn:], n_prev=time_steps)
    print('X_train.shape: %s' % str(X_train.shape))
    print('y_train.shape: %s' % str(y_train.shape))
    print('[DONE] Train/Test set ready.')
    return (X_train, y_train), (X_test, y_test)