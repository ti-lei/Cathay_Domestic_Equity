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
path = "/home/ec2-user/Cathay_Domestic_Equity/Data.csv"
Data = pd.read_csv(path)
Data.to_csv(path,encoding='utf_8_sig', index=False)
print("ok")