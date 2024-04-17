import pandas as pd
import numpy as np
import pickle
import date1

#loading historical data
df = pd.read_csv('Mumbai_1990_2022_Santacruz.csv')
df['time'] = pd.to_datetime(df['time'], format='%d-%m-%Y')

#date
# todays_date = datetime.date.today()  # Get the current date as a datetime.date object
# todays_datetime = datetime.datetime.combine(todays_date, datetime.time())  # Convert to datetime.datetime



def max(dates_s):
    with open('mumbai_max_model.pkl', "rb") as f:
        mumbai_max = pickle.load(f)
    mumbai_max.restore_trainer()
    tmax = []
    data = df[['time', 'tmax']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = mumbai_max.make_future_dataframe(data, periods=1500)
    forecast = mumbai_max.predict(future)

    for i in range(0, 4):  # Changed the loop to run for 4 days
        date = np.datetime64(date_s) + np.timedelta64(i, 'D')
        desired_row = forecast[forecast['ds'] == date]
        if not desired_row.empty:
            max_val = desired_row['yhat1'].values[0]
            tmax.append(max_val)

    print(tmax)  # values are for the current date to the next 4 days
    return tmax

def min(date_s):
    with open('mumbai_min_model.pkl', "rb") as f:
        mumbai_min = pickle.load(f)
    mumbai_min.restore_trainer()
    tmin = []
    d = []
    data = df[['time', 'tmin']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = mumbai_min.make_future_dataframe(data, periods=1500)
    forecast = mumbai_min.predict(future)

    for i in range(0, 4):
        date = np.datetime64(date_s) + np.timedelta64(i, 'D')
        desired_row = forecast[forecast['ds'] == date]
        if not desired_row.empty:
            min_val = desired_row['yhat1'].values[0]
            tmin.append(min_val)

    print(tmin)  # values are for the current date to the next 4 days
    return tmin

def avg(date_s):
    with open('mumbai_avg_model.pkl', "rb") as f:
        mumbai_avg = pickle.load(f)
    mumbai_avg.restore_trainer()
    tavg = []
    data = df[['time', 'tavg']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = mumbai_avg.make_future_dataframe(data, periods=1500)
    forecast = mumbai_avg.predict(future)

    for i in range(0, 4):
        date = np.datetime64(date_s) + np.timedelta64(i, 'D')
        desired_row = forecast[forecast['ds'] == date]
        if not desired_row.empty:
            avg_val = desired_row['yhat1'].values[0]
            tavg.append(avg_val)

    print(tavg)  # values are for the current date to the next 4 days
    return tavg

def prec(date_s):
    with open('mumbai_prec_model.pkl', "rb") as f:
        mumbai_prec = pickle.load(f)
    mumbai_prec.restore_trainer()
    tprec = []
    data = df[['time', 'prcp']]
    data.dropna(inplace=True)
    data.columns = ['ds', 'y']
    future = mumbai_prec.make_future_dataframe(data, periods=1500)
    forecast = mumbai_prec.predict(future)

    for i in range(0, 4):
        date = np.datetime64(date_s) + np.timedelta64(i, 'D')
        desired_row = forecast[forecast['ds'] == date]
        if not desired_row.empty:
            prec_val = desired_row['yhat1'].values[0]
            tprec.append(prec_val)

    print(tprec)
    return tprec


date_s =date1.spec_date(0) # Get the initial date
# max()
# min()
# avg()
# prec()






