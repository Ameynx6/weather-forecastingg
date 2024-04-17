import pandas as pd
import numpy as np
import pickle
import date1
#loading historical data
df = pd.read_csv('Delhi_NCR_1990_2022_Safdarjung.csv')
df['time'] = pd.to_datetime(df['time'], format='%d-%m-%Y')



def max(date_s):
    with open('delhi_max_model.pkl', "rb") as f:
        delhi_max = pickle.load(f)
    delhi_max.restore_trainer()

    tmax = []
    data = df[['time', 'tmax']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = delhi_max.make_future_dataframe(data, periods=500)
    forecast = delhi_max.predict(future)

    for i in range(0, 4):  # Changed the loop to run for 4 days
        date = np.datetime64(date_s) + np.timedelta64(i, 'D')
        desired_row = forecast[forecast['ds'] == date]
        if not desired_row.empty:
            max_val = desired_row['yhat1'].values[0]
            tmax.append(max_val)

    print(tmax)  # values are for the current date to the next 4 days
    return tmax


def min(date_s):
    with open('delhi_min_model.pkl', "rb") as f:
        delhi_min = pickle.load(f)
    delhi_min.restore_trainer()

    tmin = []
    d = []
    data = df[['time', 'tmin']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = delhi_min.make_future_dataframe(data, periods=500)
    forecast = delhi_min.predict(future)

    for i in range(0, 4):
        date = np.datetime64(date_s) + np.timedelta64(i, 'D')
        desired_row = forecast[forecast['ds'] == date]
        if not desired_row.empty:
            min_val = desired_row['yhat1'].values[0]
            tmin.append(min_val)

    print(tmin)  # values are for the current date to the next 4 days
    return tmin


def avg(date_s):
    with open('delhi_avg_model.pkl', "rb") as f:
        delhi_avg = pickle.load(f)
    delhi_avg.restore_trainer()

    tavg = []
    data = df[['time', 'tavg']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = delhi_avg.make_future_dataframe(data, periods=500)
    forecast = delhi_avg.predict(future)

    for i in range(0, 4):
        date = np.datetime64(date_s) + np.timedelta64(i, 'D')
        desired_row = forecast[forecast['ds'] == date]
        if not desired_row.empty:
            avg_val = desired_row['yhat1'].values[0]
            tavg.append(avg_val)

    print(tavg)  # values are for the current date to the next 4 days
    return tavg



def prec(date_s):
    with open('delhi_prec_model.pkl', "rb") as f:
        delhi_prec = pickle.load(f)
    delhi_prec.restore_trainer()

    tprec = []
    data = df[['time', 'prcp']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = delhi_prec.make_future_dataframe(data, periods=500)
    forecast = delhi_prec.predict(future)

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