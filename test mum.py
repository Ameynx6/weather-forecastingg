import pandas as pd
import models
import datetime
import numpy as np
import pickle

with open('mumbai_max_model.pkl', "rb") as f:
    mumbai_max = pickle.load(f)
mumbai_max.restore_trainer()

df = pd.read_csv('Mumbai_1990_2022_Santacruz.csv')
df['time'] = pd.to_datetime(df['time'], format='%d-%m-%Y')

data = df[['time', 'tmax']]
data.dropna(inplace=True)
data.columns = ['ds', 'y']
future = mumbai_max.make_future_dataframe(data, periods=500)
forecast = mumbai_max.predict(future)
