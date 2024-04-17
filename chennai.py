import pandas as pd
import numpy as np
import pickle
import date1

#loading historical data
df = pd.read_csv(r'C:\Users\Amey\PycharmProjects\weather forecasting\wdata\Temperature_And_Precipitation_Cities_IN\Chennai_1990_2022_Madras.csv')
df['time'] = pd.to_datetime(df['time'], format='%d-%m-%Y')



def max(date_s):
    with open('Chennai_max_model.pkl', "rb") as f:
        Chennai_max = pickle.load(f)
    Chennai_max.restore_trainer()
    tmax = []
    data = df[['time', 'tmax']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = Chennai_max.make_future_dataframe(data, periods=500)
    forecast = Chennai_max.predict(future)

    for i in range(0, 4):  # Changed the loop to run for 4 days
        date = np.datetime64(date_s) + np.timedelta64(i, 'D')
        desired_row = forecast[forecast['ds'] == date]
        if not desired_row.empty:
            max_val = desired_row['yhat1'].values[0]
            tmax.append(max_val)

    print(tmax)  # values are for the current date to the next 4 days
    return tmax


def min(date_s):
    with open('Chennai_min_model.pkl', "rb") as f:
        Chennai_min = pickle.load(f)
    Chennai_min.restore_trainer()
    tmin = []
    d = []
    data = df[['time', 'tmin']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = Chennai_min.make_future_dataframe(data, periods=500)
    forecast = Chennai_min.predict(future)

    for i in range(0, 4):
        date = np.datetime64(date_s) + np.timedelta64(i, 'D')
        desired_row = forecast[forecast['ds'] == date]
        if not desired_row.empty:
            min_val = desired_row['yhat1'].values[0]
            tmin.append(min_val)

    print(tmin)  # values are for the current date to the next 4 days
    return tmin


def avg(date_s):
    with open('Chennai_avg_model.pkl', "rb") as f:
        Chennai_avg = pickle.load(f)
    Chennai_avg.restore_trainer()
    tavg = []
    data = df[['time', 'tavg']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = Chennai_avg.make_future_dataframe(data, periods=500)
    forecast = Chennai_avg.predict(future)

    for i in range(0, 4):
        date = np.datetime64(date_s) + np.timedelta64(i, 'D')
        desired_row = forecast[forecast['ds'] == date]
        if not desired_row.empty:
            avg_val = desired_row['yhat1'].values[0]
            tavg.append(avg_val)

    print(tavg)  # values are for the current date to the next 4 days
    return tavg


def prec(date_s):
    with open('Chennai_prcp_model.pkl', "rb") as f:
        Chennai_prec = pickle.load(f)
    Chennai_prec.restore_trainer()
    tprec = []
    data = df[['time', 'prcp']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = Chennai_prec.make_future_dataframe(data, periods=500)
    forecast = Chennai_prec.predict(future)

    for i in range(0, 4):
        date = np.datetime64(date_s) + np.timedelta64(i, 'D')
        desired_row = forecast[forecast['ds'] == date]
        if not desired_row.empty:
            prec_val = desired_row['yhat1'].values[0]
            tprec.append(prec_val)

    print(tprec)
    return tprec


date_s = date1.spec_date(0) # Get the initial date
# max(date_s)
# min(date_s)
# avg(date_s)
# prec(date_s)
