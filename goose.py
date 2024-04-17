import pandas as pd
import requests
import json
import matplotlib.pyplot as plt

# Reading the temperature data
df_temp = pd.read_csv("Weather Data in India from 1901 to 2017.csv.csv")
df_temp.set_index('YEAR', inplace=True)

# Reading the rainfall data
df_rainfall = pd.read_csv("district wise rainfall normal.csv")
df_rainfall.set_index('STATE_UT_NAME', inplace=True)
x=df_rainfall.head()
print (x)

def get_previous():
    print("*******************************PREVIOUS DATA*******************************")

    month_entered = 0
    year_entered = int(input("Enter the Year:"))

    if year_entered > 2017 or year_entered < 1901:
        print("Please enter a year between 1901 and 2017")
    else:
        month_entered = input("Enter the Month:").upper()
        try:
            specific_date = df_temp.loc[year_entered, month_entered]
            print(f'Temperature for {month_entered} in {year_entered}: {specific_date}C')
        except KeyError:
            print("Please enter a valid month")

def main_menu():
    print("1. Previous Data")
    print("2. Realtime")
    print("3. Graphs")
    print("4. Rainfall Data")
    choice = input("Enter your choice:")

    if choice == "1":
        get_previous()
    elif choice == "2":
        # Realtime weather data (unchanged)
        pass
    elif choice == "3":
        # Graphs (unchanged)
        pass
    elif choice == "4":
        print("*******************************RAINFALL DATA*******************************")
        state_ut_name = input("Enter State/UT Name:")
        district = input("Enter District:")

        # Filter the dataframe based on the provided state and district
        selected_data = df_rainfall[(df_rainfall['STATE_UT_NAME'] == state_ut_name) & (df_rainfall['DISTRICT'] == district)]

        if not selected_data.empty:
            print(selected_data)
        else:
            print("No data found for the specified state and district.")

    else:
        print("Please choose between Option 1, 2, 3, or 4.")

main_menu()