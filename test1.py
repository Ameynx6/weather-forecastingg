# import pandas as pd
# import datetime
# import numpy as np
# import pickle
#
# #loading of trained models
#
# with open('Delhi_max_model.pkl', "rb") as f:
#     Delhi_max = pickle.load(f)
# Delhi_max.restore_trainer()#loading historical data
# df = pd.read_csv('Delhi_NCR_1990_2022_Safdarjung.csv')
# df['time'] = pd.to_datetime(df['time'], format='%d-%m-%Y')
#
# #date
# todays_date = datetime.date.today()  # Get the current date as a datetime.date object
# todays_datetime = datetime.datetime.combine(todays_date, datetime.time())  # Convert to datetime.datetime

import gui


#
# def max():
#     date = todays_datetime
#     tmax = []
#     data = df[['time', 'tmax']]
#     data.dropna(inplace=True)
#     data.columns = ['ds', 'y']
#     future = Delhi_max.make_future_dataframe(data, periods=500)
#     forecast = Delhi_max.predict(future)
#     for i in range(0,4):
#        date = np.datetime64(date) + np.timedelta64(1, 'D')
#        desired_row = forecast[forecast['ds'] == date - np.timedelta64(1, 'D')]
#        if not desired_row.empty:
#            max = desired_row['yhat1'].values[0]
#            tmax.append(max)
#     print(tmax)  # values are like current date to next 10 days
# max()
from gui import date_var

def process_date():
    date = date_var.get()
    print("Most recent date:", date)

process_date()
x=type(date_var)
print(x)

def check_city():
    user_input=textfield.get()
    if user_input.lower() == 'mumbai':
        mum = Label(root, text="mum", font=("Helvetica", 20), fg="white", bg="#57adff")
        mum.place(x=500, y=60)
    else:
        mum1 = Label(root, text="mum1", font=("Helvetica", 20), fg="white", bg="#57adff")
        mum1.place(x=500, y=60)