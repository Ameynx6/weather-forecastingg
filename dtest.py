import numpy as np
from datetime import datetime

def spec_date(index):
    date_arr = []

    # Ask the user for a date in YYYY-MM-DD format
    date_str = '2023-11-05'

    try:
        # Parse the input date string into a datetime object
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        print(f"Date stored as datetime object: {date_obj}")

        # Convert the datetime object to a datetime64 and store it in the date_arr
        date_arr = np.array([np.datetime64(date_obj)])

    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")

    if index < len(date_arr):
        return date_arr[index]
    else:
        return None


#t_date()

# s_date()
spec_date(0)