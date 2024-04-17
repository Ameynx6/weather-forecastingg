import pandas as pd
import datetime
import numpy as np
import pickle

#loading of trained models

with open('Bhubneshwar_max_model.pkl', "rb") as f:
    Bhubneshwar_max = pickle.load(f)
Bhubneshwar_max.restore_trainer()

with open('Bhubneshwar_min_model.pkl', "rb") as f:
    Bhubneshwar_min = pickle.load(f)
Bhubneshwar_min.restore_trainer()

with open('Bhubneshwar_avg_model.pkl', "rb") as f:
    Bhubneshwar_avg = pickle.load(f)
Bhubneshwar_avg.restore_trainer()

with open('Bhubneshwar_prec_model.pkl', "rb") as f:
    Bhubneshwar_prec = pickle.load(f)
Bhubneshwar_prec.restore_trainer()

#loading historical data
df = pd.read_csv('weather_Bhubhneshwar_formatted.csv')
df['time'] = pd.to_datetime(df['time'], format='%d-%m-%Y')

#date
todays_date = datetime.date.today()  # Get the current date as a datetime.date object
todays_datetime = datetime.datetime.combine(todays_date, datetime.time())  # Convert to datetime.datetime


def max():
    date = todays_datetime
    tmax = []
    data = df[['time', 'tmax']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = Bhubneshwar_max.make_future_dataframe(data, periods=500)
    forecast = Bhubneshwar_max.predict(future)
    for i in range(0,4):
       date = np.datetime64(date) + np.timedelta64(1, 'D')
       desired_row = forecast[forecast['ds'] == date - np.timedelta64(1, 'D')]
       if not desired_row.empty:
           max = desired_row['yhat1'].values[0]
           tmax.append(max)
    print(tmax)  # values are like current date to next 10 days


def min():
    date = todays_datetime
    tmin = []
    data = df[['time', 'tmin']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = Bhubneshwar_min.make_future_dataframe(data, periods=500)
    forecast = Bhubneshwar_min.predict(future)
    for i in range(0,4):
       date = np.datetime64(date) + np.timedelta64(1, 'D')
       desired_row = forecast[forecast['ds'] == date - np.timedelta64(1, 'D')]
       if not desired_row.empty:
           min = desired_row['yhat1'].values[0]
           tmin.append(min)
    print(tmin)  # values are like current date to next 10 days

def avg():
    date = todays_datetime
    tavg = []
    data = df[['time', 'tavg']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = Bhubneshwar_avg.make_future_dataframe(data, periods=500)
    forecast = Bhubneshwar_avg.predict(future)
    for i in range(0, 4):
        date = np.datetime64(date) + np.timedelta64(1, 'D')
        desired_row = forecast[forecast['ds'] == date - np.timedelta64(1, 'D')]
        if not desired_row.empty:
            avg = desired_row['yhat1'].values[0]
            tavg.append(avg)
    print(tavg)  # values are like current date to next 10 days
def prec():
    date = todays_datetime
    tprec = []
    data = df[['time', 'prcp']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = Bhubneshwar_prec.make_future_dataframe(data, periods=500)
    forecast = Bhubneshwar_prec.predict(future)
    for i in range(0, 4):
        date = np.datetime64(date) + np.timedelta64(1, 'D')
        desired_row = forecast[forecast['ds'] == date - np.timedelta64(1, 'D')]
        if not desired_row.empty:
            prec = desired_row['yhat1'].values[0]
            tprec.append(prec)
    print(tprec)

max()
min()
avg()
prec()
