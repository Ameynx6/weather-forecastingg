# import pandas as pd
# import pickle
# import datetime
# import numpy as np
#
# df = pd.read_csv('Mumbai_1990_2022_Santacruz.csv')
# df['time'] = pd.to_datetime(df['time'], format='%d-%m-%Y')
# data = df[['time', 'tmax']].copy()  # Make a copy of the DataFrame
# data.dropna(inplace=True)
# data.columns = ['ds', 'y']
# data.head()
#
# with open('mumbai_max_model.pkl', "rb") as f:
#     mumbai_max = pickle.load(f)
#
# mumbai_max.restore_trainer()
#
# future = mumbai_max.make_future_dataframe(data, periods=500)
# forecast = mumbai_max.predict(future)
# y=forecast.tail()
# print(y)
#
# todays_date = datetime.date.today()  # Get the current date as a datetime.date object
# todays_datetime = datetime.datetime.combine(todays_date, datetime.time())  # Convert to datetime.datetime
# todays_datetime64 = np.datetime64(todays_datetime)  # Convert to datetime64[ns]
#
# print(todays_datetime64)
# desired_row = forecast[forecast['ds'] == todays_datetime64]
#
# # Check if the row exists
# if not desired_row.empty:
#     print("Row for",todays_datetime64, "is:")
#     print(desired_row)
# else:
#     print("No data found for",todays_datetime64)

import mumbai
date_s='2023-06-11'
x=mumbai.prec(date_s)
print(x)