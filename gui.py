import datetime
from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import *
import pytz
from PIL import Image, ImageTk
import mumbai
import lucknow
import Jodhpur
import delhi
import banglore
import Bhubneshwar
import numpy as np
import chennai


root = Tk()
root.title("Weather Forecasting App")
root.geometry("890x600+300+500")
root.configure(bg="#57adff")
img = PhotoImage(file="Image/OIP.png")
root.iconphoto(False, img)
def both_commands():
    getweather()
    checkcity()
def cmd():
    checkcity()
    get_day()
    get_dates()
    getweather()

#date convs
def date_store():
    date_s = textfield2.get()
    try:
        #for day
        # Convert the input date string to a datetime64 object
        date_obj = datetime.strptime(date_s, "%d-%m-%Y")
        reform_date=date_obj.strftime("%Y-%m-%d")
        date64_obj = np.datetime64(reform_date)
        # print(f"Date stored as datetime64 object: {date64_obj}")
        date_strz = date64_obj
        print(f'entered date {date_strz}')
        return date_strz
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")
        labelde = Label(root, text='please enter in dd-mm-yyyy format', font=('Helvetica', 14), fg="red",bg="#57adff"
                        )
        labelde.place(x=430, y=243)
def get_dates():
    date_s = textfield2.get()
    date_format = "%d-%m-%Y"
    current_date = datetime.strptime(date_s, date_format)
    dates = [current_date.strftime(date_format)]
    for i in range(1, 4):
        next_date = current_date + timedelta(days=i)
        dates.append(next_date.strftime(date_format))
    label_date1=Label(root, text=dates[0], font=('Helvetica', 10), fg="white", bg="#000000")
    label_date1.place(x=174, y=70)
    label_date2 = Label(frame, text=dates[1], font=('Helvetica', 10), fg="white", bg="#272829")
    label_date2.place(x=362, y=50)
    label_date3 = Label(frame, text=dates[2], font=('Helvetica', 10), fg="white", bg="#272829")
    label_date3.place(x=535, y=50)
    label_date4 = Label(frame, text=dates[3], font=('Helvetica', 10), fg="white", bg="#272829")
    label_date4.place(x=710, y=50)
def suggestions():
    suggestion=["it's chilly, bundle up to keep warm.","a bit cold, grab a light jacket.",
                "cool and comfortable, perfect for a walk.","a pleasant day for outdoor activities.",
                " a moderate day, great for outdoor plans.","a warm day, enjoy the sunshine.",
                " scorching heat, stay indoors and hydrate.","it's sweltering, seek shade and stay hydrated."]
    return suggestion


def get_day():
    date_s = textfield2.get()
    day_obj = datetime.strptime(date_s, "%d-%m-%Y")
    day_of_week = day_obj.weekday()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    d1 = days[day_of_week]
    d2 = days[(day_of_week + 1) % len(days)]
    d3 = days[(day_of_week + 2) % len(days)]
    d4 = days[(day_of_week + 3) % len(days)]

    d = [d1, d2, d3, d4]

    labeld1 = Label(root, text=d[0], font=('Helvetica', 10), fg="white", bg="#000000")
    labeld1.place(x=98, y=70)
    labeld2 = Label(frame, text=d[1], font=('Helvetica', 10), fg="white", bg="#272829")
    labeld2.place(x=360, y=80)
    labeld3 = Label(frame, text=d[2], font=('Helvetica', 10), fg="white", bg="#272829")
    labeld3.place(x=532, y=80)
    labeld4 = Label(frame, text=d[3], font=('Helvetica', 10), fg="white", bg="#272829")
    labeld4.place(x=720, y=80)

def compare(xmax):
    i=0
    if xmax<=5:
        return i
    elif xmax<=10:
        return i+1
    elif xmax<=15:
        return i+2
    elif xmax<=20:
        return i+3
    elif xmax<=25:
        return i+4
    elif xmax<=32:
        return i+5
    elif xmax<=35:
        return i+6
    elif xmax<35:
        return i+7
def prec_sent(y_prec):
    if y_prec == 0:
        y = ' no probability '
        return y
    elif y_prec < 5:
        y = 'zero probability'
        return y
    elif y_prec < 10:
        y = ' less chances   '
        return y
    elif y_prec < 20:
        y = ' moderate chance'
        return y
    elif y_prec < 25:
        y = '  high chances   '
        return y
    else:
        y = '  high chances   '
        return y
def check_c():
    user_input = textfield.get()
    x=0
    if user_input.lower() == 'mumbai':
        return x
    elif user_input.lower() == 'lucknow':
        return x+1
    elif user_input.lower() == 'jodhpur':
        return x+2
    elif user_input.lower() == 'delhi':
        return x+3
    elif user_input.lower() == 'bangalore':
        return x+4
    elif user_input.lower() == 'bhubhneshwar':
        return x+5
    elif user_input.lower() == 'chennai':
        return x+6

def checkcity():
    user_input=textfield.get()
    date_str = date_store()
    if user_input.lower() == 'mumbai':
        x_max = mumbai.max(date_str)
        i=compare(x_max[0])
        suggestion=suggestions()
        suggest=suggestion[i]
        labels = Label(frame, wraplength=200, text=suggest, width=25, height=6,font=('Helvetica', 11), fg="white", bg="#272928")
        labels.place(x=35, y=70)
        max1 = Label(root, text=round(x_max[0]), font=("Helvetica", 12), fg="white", bg="black")
        max1.place(x=130, y=100)
        max2 = Label(frame, text=round(x_max[1]), font=("Helvetica", 10), fg="white", bg="#272829")
        max2.place(x=411, y=119)
        max3 = Label(frame, text=round(x_max[2]), font=("Helvetica", 10), fg="white", bg="#272829")
        max3.place(x=583, y=119)
        max4 = Label(frame, text=round(x_max[3]), font=("Helvetica", 10), fg="white", bg="#272829")
        max4.place(x=758, y=119)
        x_min = mumbai.min(date_str)
        min1 = Label(root, text=round(x_min[0]), font=("Helvetica", 12), fg="white", bg="black")
        min1.place(x=130, y=140)
        min2 = Label(frame, text=round(x_min[1]), font=("Helvetica", 10), fg="white", bg="#272829")
        min2.place(x=411, y=150)
        min3 = Label(frame, text=round(x_min[2]), font=("Helvetica", 10), fg="white", bg="#272829")
        min3.place(x=583, y=150)
        min4 = Label(frame, text=round(x_min[3]), font=("Helvetica", 10), fg="white", bg="#272829")
        min4.place(x=758, y=150)
        x_avg = mumbai.avg(date_str)
        y_avg = round(x_avg[0])
        avg = Label(root, text=y_avg, font=("Helvetica", 12), fg="white", bg="black")
        avg.place(x=130, y=180)
        x_prec = mumbai.prec(date_str)
        y_prec = round(x_prec[0])
        y=prec_sent(y_prec)
        prec = Label(root, text=y, font=("Helvetica", 10), fg="white", bg="black")
        prec.place(x=140, y=221)

    elif user_input.lower() == 'lucknow':
        x_max = lucknow.max(date_str)
        i = compare(x_max[0])
        suggestion = suggestions()
        suggest = suggestion[i]
        labels = Label(frame, wraplength=200, text=suggest, width=25, height=6, font=('Helvetica', 11), fg="white",
                       bg="#272928")
        labels.place(x=35, y=70)
        max1 = Label(root, text=round(x_max[0]), font=("Helvetica", 12), fg="white", bg="black")
        max1.place(x=130, y=100)
        max2 = Label(frame, text=round(x_max[1]), font=("Helvetica", 10), fg="white", bg="#272829")
        max2.place(x=411, y=119)
        max3 = Label(frame, text=round(x_max[2]), font=("Helvetica", 10), fg="white", bg="#272829")
        max3.place(x=583, y=119)
        max4 = Label(frame, text=round(x_max[3]), font=("Helvetica", 10), fg="white", bg="#272829")
        max4.place(x=758, y=119)
        x_min = lucknow.min(date_str)
        min1 = Label(root, text=round(x_min[0]), font=("Helvetica", 12), fg="white", bg="black")
        min1.place(x=130, y=140)
        min2 = Label(frame, text=round(x_min[1]), font=("Helvetica", 10), fg="white", bg="#272829")
        min2.place(x=411, y=150)
        min3 = Label(frame, text=round(x_min[2]), font=("Helvetica", 10), fg="white", bg="#272829")
        min3.place(x=583, y=150)
        min4 = Label(frame, text=round(x_min[3]), font=("Helvetica", 10), fg="white", bg="#272829")
        min4.place(x=758, y=150)
        x_avg = lucknow.avg(date_str)
        y_avg = round(x_avg[0])
        luck_avg = Label(root, text=y_avg, font=("Helvetica", 12), fg="white", bg="black")
        luck_avg.place(x=130, y=180)
        x_prec = lucknow.prec(date_str)
        y_prec = round(x_prec[0])
        y = prec_sent(y_prec)
        prec = Label(root, text=y, font=("Helvetica", 10), fg="white", bg="black")
        prec.place(x=140, y=221)
    elif user_input.lower() == 'jodhpur':
        x_max = Jodhpur.max(date_str)
        i = compare(x_max[0])
        suggestion = suggestions()
        suggest = suggestion[i]
        labels = Label(frame, wraplength=200, text=suggest, width=25, height=6, font=('Helvetica', 11), fg="white",
                       bg="#272928")
        labels.place(x=35, y=70)
        max1 = Label(root, text=round(x_max[0]), font=("Helvetica", 12), fg="white", bg="black")
        max1.place(x=130, y=100)
        max2 = Label(frame, text=round(x_max[1]), font=("Helvetica", 10), fg="white", bg="#272829")
        max2.place(x=411, y=119)
        max3 = Label(frame, text=round(x_max[2]), font=("Helvetica", 10), fg="white", bg="#272829")
        max3.place(x=583, y=119)
        max4 = Label(frame, text=round(x_max[3]), font=("Helvetica", 10), fg="white", bg="#272829")
        max4.place(x=758, y=119)

        x_min = Jodhpur.min(date_str)
        min1 = Label(root, text=round(x_min[0]), font=("Helvetica", 12), fg="white", bg="black")
        min1.place(x=130, y=140)
        min2 = Label(frame, text=round(x_min[1]), font=("Helvetica", 10), fg="white", bg="#272829")
        min2.place(x=411, y=150)
        min3 = Label(frame, text=round(x_min[2]), font=("Helvetica", 10), fg="white", bg="#272829")
        min3.place(x=583, y=150)
        min4 = Label(frame, text=round(x_min[3]), font=("Helvetica", 10), fg="white", bg="#272829")
        min4.place(x=758, y=150)
        x_avg = Jodhpur.avg(date_str)
        y_avg = round(x_avg[0])
        jodh_avg = Label(root, text=y_avg, font=("Helvetica", 12), fg="white", bg="black")
        jodh_avg.place(x=130, y=180)

        jodh_prec = Label(root, text='no data found', font=("Helvetica", 12), fg="white", bg="black")
        jodh_prec.place(x=140, y=221)

    elif user_input.lower() == 'delhi':
        x_max = delhi.max(date_str)
        i = compare(x_max[0])
        suggestion = suggestions()
        suggest = suggestion[i]
        labels = Label(frame, wraplength=200, text=suggest, width=25, height=6, font=('Helvetica', 11), fg="white",
                       bg="#272928")
        labels.place(x=35, y=70)
        max1 = Label(root, text=round(x_max[0]), font=("Helvetica", 12), fg="white", bg="black")
        max1.place(x=130, y=100)
        max2 = Label(frame, text=round(x_max[1]), font=("Helvetica", 10), fg="white", bg="#272829")
        max2.place(x=411, y=119)
        max3 = Label(frame, text=round(x_max[2]), font=("Helvetica", 10), fg="white", bg="#272829")
        max3.place(x=583, y=119)
        max4 = Label(frame, text=round(x_max[3]), font=("Helvetica", 10), fg="white", bg="#272829")
        max4.place(x=758, y=119)
        x_min = delhi.min(date_str)
        min1 = Label(root, text=round(x_min[0]), font=("Helvetica", 12), fg="white", bg="black")
        min1.place(x=130, y=140)
        min2 = Label(frame, text=round(x_min[1]), font=("Helvetica", 10), fg="white", bg="#272829")
        min2.place(x=411, y=150)
        min3 = Label(frame, text=round(x_min[2]), font=("Helvetica", 10), fg="white", bg="#272829")
        min3.place(x=583, y=150)
        min4 = Label(frame, text=round(x_min[3]), font=("Helvetica", 10), fg="white", bg="#272829")
        min4.place(x=758, y=150)
        x_avg = delhi.avg(date_str)
        y_avg = round(x_avg[0])
        delhi_avg = Label(root, text=y_avg, font=("Helvetica", 12), fg="white", bg="black")
        delhi_avg.place(x=130, y=180)
        x_prec = delhi.prec(date_str)
        y_prec = round(x_prec[0])
        y = prec_sent(y_prec)
        prec = Label(root, text=y, font=("Helvetica", 10), fg="white", bg="black")
        prec.place(x=140, y=221)
    elif user_input.lower() == 'bangalore':
        x_max = banglore.max(date_str)
        i = compare(x_max[0])
        suggestion = suggestions()
        suggest = suggestion[i]
        labels = Label(frame, wraplength=200, text=suggest, width=25, height=6, font=('Helvetica', 11), fg="white",
                       bg="#272928")
        labels.place(x=35, y=70)
        max1 = Label(root, text=round(x_max[0]), font=("Helvetica", 12), fg="white", bg="black")
        max1.place(x=130, y=100)
        max2 = Label(frame, text=round(x_max[1]), font=("Helvetica", 10), fg="white", bg="#272829")
        max2.place(x=411, y=119)
        max3 = Label(frame, text=round(x_max[2]), font=("Helvetica", 10), fg="white", bg="#272829")
        max3.place(x=583, y=119)
        max4 = Label(frame, text=round(x_max[3]), font=("Helvetica", 10), fg="white", bg="#272829")
        max4.place(x=758, y=119)
        x_min = banglore.min(date_str)
        min1 = Label(root, text=round(x_min[0]), font=("Helvetica", 12), fg="white", bg="black")
        min1.place(x=130, y=140)
        min2 = Label(frame, text=round(x_min[1]), font=("Helvetica", 10), fg="white", bg="#272829")
        min2.place(x=411, y=150)
        min3 = Label(frame, text=round(x_min[2]), font=("Helvetica", 10), fg="white", bg="#272829")
        min3.place(x=583, y=150)
        min4 = Label(frame, text=round(x_min[3]), font=("Helvetica", 10), fg="white", bg="#272829")
        min4.place(x=758, y=150)
        x_avg = banglore.avg(date_str)
        y_avg = round(x_avg[0])
        bang_avg = Label(root, text=y_avg, font=("Helvetica", 12), fg="white", bg="black")
        bang_avg.place(x=130, y=180)
        x_prec = banglore.prec(date_str)
        y_prec = round(x_prec[0])
        y = prec_sent(y_prec)
        prec = Label(root, text=y, font=("Helvetica", 10), fg="white", bg="black")
        prec.place(x=140, y=221)

    elif user_input.lower() == 'bhubhneshwar':
        x_max = Bhubneshwar.max(date_str)
        i = compare(x_max[0])
        suggestion = suggestions()
        suggest = suggestion[i]
        labels = Label(frame, wraplength=200, text=suggest, width=25, height=6, font=('Helvetica', 11), fg="white",
                       bg="#272928")
        labels.place(x=35, y=70)
        max1 = Label(root, text=round(x_max[0]), font=("Helvetica", 12), fg="white", bg="black")
        max1.place(x=130, y=100)
        max2 = Label(frame, text=round(x_max[1]), font=("Helvetica", 10), fg="white", bg="#272829")
        max2.place(x=411, y=119)
        max3 = Label(frame, text=round(x_max[2]), font=("Helvetica", 10), fg="white", bg="#272829")
        max3.place(x=583, y=119)
        max4 = Label(frame, text=round(x_max[3]), font=("Helvetica", 10), fg="white", bg="#272829")
        max4.place(x=758, y=119)
        x_min = Bhubneshwar.min(date_str)
        min1 = Label(root, text=round(x_min[0]), font=("Helvetica", 12), fg="white", bg="black")
        min1.place(x=130, y=140)
        min2 = Label(frame, text=round(x_min[1]), font=("Helvetica", 10), fg="white", bg="#272829")
        min2.place(x=411, y=150)
        min3 = Label(frame, text=round(x_min[2]), font=("Helvetica", 10), fg="white", bg="#272829")
        min3.place(x=583, y=150)
        min4 = Label(frame, text=round(x_min[3]), font=("Helvetica", 10), fg="white", bg="#272829")
        min4.place(x=758, y=150)
        x_avg = Bhubneshwar.avg(date_str)
        y_avg = round(x_avg[0])
        bhub_avg = Label(root, text=y_avg, font=("Helvetica", 12), fg="white", bg="black")
        bhub_avg.place(x=130, y=180)
        x_prec = Bhubneshwar.prec(date_str)
        y_prec = round(x_prec[0])
        y = prec_sent(y_prec)
        prec = Label(root, text=y, font=("Helvetica", 10), fg="white", bg="black")
        prec.place(x=140, y=221)
    elif user_input.lower() == 'chennai':
        x_max = chennai.max(date_str)
        i = compare(x_max[0])
        suggestion = suggestions()
        suggest = suggestion[i]
        labels = Label(frame, wraplength=200, text=suggest, width=25, height=6, font=('Helvetica', 11), fg="white",
                       bg="#272928")
        labels.place(x=35, y=70)
        max1 = Label(root, text=round(x_max[0]), font=("Helvetica", 12), fg="white", bg="black")
        max1.place(x=130, y=100)
        max2 = Label(frame, text=round(x_max[1]), font=("Helvetica", 10), fg="white", bg="#272829")
        max2.place(x=411, y=119)
        max3 = Label(frame, text=round(x_max[2]), font=("Helvetica", 10), fg="white", bg="#272829")
        max3.place(x=583, y=119)
        max4 = Label(frame, text=round(x_max[3]), font=("Helvetica", 10), fg="white", bg="#272829")
        max4.place(x=758, y=119)
        x_min = chennai.min(date_str)
        min1 = Label(root, text=round(x_min[0]), font=("Helvetica", 12), fg="white", bg="black")
        min1.place(x=130, y=140)
        min2 = Label(frame, text=round(x_min[1]), font=("Helvetica", 10), fg="white", bg="#272829")
        min2.place(x=411, y=150)
        min3 = Label(frame, text=round(x_min[2]), font=("Helvetica", 10), fg="white", bg="#272829")
        min3.place(x=583, y=150)
        min4 = Label(frame, text=round(x_min[3]), font=("Helvetica", 10), fg="white", bg="#272829")
        min4.place(x=758, y=150)
        x_avg = chennai.avg(date_str)
        y_avg = round(x_avg[0])
        bhub_avg = Label(root, text=y_avg, font=("Helvetica", 12), fg="white", bg="black")
        bhub_avg.place(x=130, y=180)
        x_prec = chennai.prec(date_str)
        y_prec = round(x_prec[0])
        y = prec_sent(y_prec)
        prec = Label(root, text=y, font=("Helvetica", 10), fg="white", bg="black")
        prec.place(x=140, y=221)


    else:
        invalid = Label(root, text="enter a supported city", font=("Helvetica", 14), fg="red",bg="#57adff" )
        invalid.place(x=485, y=148)

def getweather():
    city = textfield.get()

    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city)
    obj = TimezoneFinder()

    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

    timezone.config(text=result)
    long_lat.config(text=f"({round(location.latitude, 4)}°N,{round(location.longitude, 4)}°E)")

    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M:%p")
    clock.config(text=current_time)


# def get_date_and_store(textfield1, date_var):
#     date = textfield1.get()
#     date_var.set(date) sloww
date_var = tk.StringVar()
def get_date_and_store(textfield1):
    date = textfield1.get()
    date_var.set(date)  # Store the date in date_var
    print("Entered date:", date)


Round_box = PhotoImage(file="Image/rect2.png")
Label(root, image=Round_box, bg="#57adff").place(x=10, y=10)

label1 = Label(root, text="TempMax", font=('Helvetica', 11), fg="white", bg="#000000")
label1.place(x=50, y=100)

label2 = Label(root, text="TempMin", font=('Helvetica', 11), fg="white", bg="#000000")
label2.place(x=50, y=140)

label3 = Label(root, text="TempAvg", font=('Helvetica', 11), fg="white", bg="#000000")
label3.place(x=50, y=180)

label4 = Label(root, text="Precipitation", font=('Helvetica', 11), fg="white", bg="#000000")
label4.place(x=50, y=220)

# search box1
img = Image.open("Image/rect5.png")
img = img.resize((390, 125))
Search_image = ImageTk.PhotoImage(img)
myimage = Label(image=Search_image, bg="#57adff")
myimage.place(x=380, y=50)

weat_image = PhotoImage(file="Image/cl.png")
weatherimage = Label(root, image=weat_image, bg="#000000")
weatherimage.place(x=410, y=95)
def on_entry_click(event):
    if textfield.get() == 'enter city name':  # Check if the Entry contains the default text
        textfield.delete(0, "end")  # Clear the default text
        textfield.config(fg='white')
        textfield.config(cursor="ibeam")

def on_entry_leave(event):
    if textfield.get() == '':
        textfield.insert(0, 'enter city name')  # Restore the default text
        textfield.config(fg='#bdc5d2')
        textfield.config(cursor="arrow")

textfield = tk.Entry(root, justify='center', width=25, font=('poppins', 15), bg="#000000", border=0, fg="#bdc5d2")
textfield.insert(0, 'enter city name')  # Set the default text
textfield.place(x=446, y=99)
textfield.config(cursor="arrow")
textfield.bind("<Button-1>", on_entry_click)
textfield.bind("<FocusOut>", on_entry_leave)

Search_icon = PhotoImage(file="Image/search.png")
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#000000", command=getweather)
myimage_icon.place(x=705, y=97)

# search box2

im = Image.open("Image/rect5.png")
im = im.resize((390, 125))
Search_ima = ImageTk.PhotoImage(im)
myima = Label(image=Search_image, bg="#57adff")
myima.place(x=380, y=150)

weat_ima = PhotoImage(file="Image/calendar.png")
weatherima = Label(root, image=weat_ima, bg="#000000")
weatherima.place(x=410, y=195)
def on_entry_click2(event):
    if textfield2.get() == 'Date(DD-MM-YYYY)':
        textfield2.delete(0, "end")
        textfield2.config(fg='white')
        textfield2.config(cursor="ibeam")

def on_entry_leave2(event):
    if textfield2.get() == '':
        textfield2.insert(0, 'Date(DD-MM-YYYY)')
        textfield2.config(fg='#bdc5d2')
        textfield2.config(cursor="arrow")

textfield2 = tk.Entry(root, justify='center', width=25, font=('poppins', 15), bg="#000000", border=0, fg="#bdc5d2")
textfield2.insert(0, 'Date(DD-MM-YYYY)')  # Set the default text
textfield2.place(x=440, y=200)
textfield2.config(cursor="arrow")
textfield2.bind("<Button-1>", on_entry_click2)
textfield2.bind("<FocusOut>", on_entry_leave2)

Search_ico = PhotoImage(file="Image/search.png")
myima_ico = Button(image=Search_ico, borderwidth=0, cursor="hand2", bg="#000000",command=cmd )
myima_ico.place(x=705, y=197)

# bottom box
frame = Frame(root, width=900, height=220, bg="#212120")
frame.pack(side=BOTTOM)

firstbox = PhotoImage(file="Image/Rounded Rectangle 2.png")
secondbox = PhotoImage(file="Image/S1.png")


Label(frame, image=firstbox, bg="#212120").place(x=30, y=40)
Label(frame, image=secondbox, bg="#212120").place(x=350, y=40)
Label(frame, image=secondbox, bg="#212120").place(x=525, y=40)
Label(frame, image=secondbox, bg="#212120").place(x=700, y=40)


label2 = Label(frame,text="Suggestion", font=('Helvetica', 11), fg="white", bg="#272829")
label2.place(x=110, y=50)


label1 = Label(frame, text="TempMin", font=('Helvetica', 8), fg="white",bg="#272829")
label1.place(x=361, y=150)

label2 = Label(frame, text="TempMax", font=('Helvetica', 8), fg="white",bg="#272829" )
label2.place(x=358, y=120)

label3 = Label(frame, text="TempMin", font=('Helvetica', 8), fg="white",bg="#272829")
label3.place(x=536, y=150)
label4 = Label(frame, text="TempMax", font=('Helvetica', 8), fg="white",bg="#272829" )
label4.place(x=532, y=120)

label5 = Label(frame, text="TempMin", font=('Helvetica', 8), fg="white",bg="#272829")
label5.place(x=709, y=150)
label6 = Label(frame, text="TempMax", font=('Helvetica', 8), fg="white",bg="#272829" )
label6.place(x=706, y=120)

# clock (here we will place time)
clock = Label(root, font=("Helvetica", 30, 'bold'), fg="white", bg="#57adff")
clock.place(x=50, y=5)

# timezone
timezone = Label(root, font=("Helvetica", 20), fg="white", bg="#57adff")
timezone.place(x=600, y=10)

long_lat = Label(root, font=("Helvetica", 20), fg="white", bg="#57adff")
long_lat.place(x=600, y=40)


root.mainloop()