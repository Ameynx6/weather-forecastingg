
import pickle
import pandas as pd
def mumbai():
   with open('mumbai_max_model.pkl', "rb") as f:
     mumbai_max=pickle.load(f)
   mumbai_max.restore_trainer()
   with open('mumbai_min_model.pkl', "rb") as f:
     mumbai_min=pickle.load(f)
   mumbai_min.restore_trainer()
   with open('mumbai_avg_model.pkl',"rb") as f:
     mumbai_avg=pickle.load(f)
   mumbai_avg.restore_trainer()
   with open('mumbai_prec_model.pkl',"rb") as f:
     mumbai_prec=pickle.load(f)
   mumbai_prec.restore_trainer()
def jodhpur():
   with open('jodhpur_max_model.pkl', "rb") as f:
     jodhpur_max=pickle.load(f)
   jodhpur_max.restore_trainer()
   with open('jodhpur_min_model.pkl', "rb") as f:
     jodhpur_min=pickle.load(f)
   jodhpur_min.restore_trainer()
   with open('jodhpur_avg_model.pkl',"rb") as f:
     jodhpur_avg=pickle.load(f)
   jodhpur_avg.restore_trainer()
   with open('jodhpur_prec_model.pkl',"rb") as f:
     jodhpur_prec=pickle.load(f)
   jodhpur_prec.restore_trainer()
def lucknow():
   with open('lucknow_max_model.pkl', "rb") as f:
     lucknow_max=pickle.load(f)
   lucknow_max.restore_trainer()
   with open('lucknow_min_model.pkl', "rb") as f:
     lucknow_min=pickle.load(f)
   lucknow_min.restore_trainer()
   with open('lucknow_avg_model.pkl',"rb") as f:
     lucknow_avg=pickle.load(f)
   lucknow_avg.restore_trainer()
   with open('lucknow_prec_model.pkl',"rb") as f:
     lucknow_prec=pickle.load(f)
   lucknow_prec.restore_trainer()
def Bhubneshwar():
   with open('Bhubneshwar_max_model.pkl', "rb") as f:
     Bhubneshwar_max=pickle.load(f)
   Bhubneshwar_max.restore_trainer()
   with open('Bhubneshwar_min_model.pkl', "rb") as f:
     Bhubneshwar_min=pickle.load(f)
   Bhubneshwar_min.restore_trainer()
   with open('Bhubneshwar_avg_model.pkl',"rb") as f:
     Bhubneshwar_avg=pickle.load(f)
   Bhubneshwar_avg.restore_trainer()
   with open('Bhubneshwar_prec_model.pkl', "rb") as f:
       Bhubneshwar_prec = pickle.load(f)
   Bhubneshwar_prec.restore_trainer()

df=pd.read_csv('Mumbai_1990_2022_Santacruz.csv')
df['time'] = pd.to_datetime(df['time'], format='%d-%m-%Y')
data=df[['time','tmax']]
data.dropna(inplace=True)
data.columns=['ds','y']
data.head()
with open('mumbai_max_model.pkl', "rb") as f:
     mumbai_max=pickle.load(f)
mumbai_max.restore_trainer()
future=mumbai_max.make_future_dataframe(data, periods=900)
forecast=mumbai_max.predict(future)
forecast.head()

