from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
import requests
import json
import datetime
import pandas as pd
import os
import shutil
import datetime
import pymysql.cursors

Data = pd.read_csv("Data.csv")
# print(Data)
#把currently unavaliable 拿掉
#data_delete是抓出所有符合條件的 row

deletelist = ['Currently unavailable','暂未发售','暫未發售','現在注文できません'
				,'Derzeit nicht verfügbar','Non disponible actuellement','В настоящее время недоступно']

for i in deletelist:
	data_delete = Data[Data.Deliver == i]
	Data = Data.drop(data_delete.index, axis=0)

# print(Data)
# Data = Data[Data.Deliver != '暂未发售']
# Data = Data[Data.Deliver != '暫未發售']
# Data = Data[Data.Deliver != '現在注文できません']
# Data = Data[Data.Deliver != 'Derzeit nicht verfügbar']
# Data = Data[Data.Deliver != 'Non disponible actuellement']
# Data = Data[Data.Deliver != 'В настоящее время недоступно']

# print(Data)
#把新加坡拿掉
data_delete = Data[Data['Country'] == 'Sg']
Data = Data.drop(data_delete.index, axis=0)

#加入印度

# 將Color 的欄位改成 Colors
Data['Colors'] = Data['Color']
del Data['Color']
# print(Data)

Data.to_csv("Data.csv",index=False)