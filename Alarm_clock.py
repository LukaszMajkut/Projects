"""
My first project - Alarm clock (general idea from real python: https://realpython.com/intermediate-python-project-ideas/)
"""
import psycopg2
import pygame
from datetime import datetime


conn = psycopg2.connect(
    host = "localhost",
    user = "postgres",
    password = "?????",
    port = "5432"
)

#CREATING A DATABASE USING PSYCOPG2 LIBRARY - after creating a database we can assign it to conn
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
database_name = "alarm_clock"
cur.execute("create database " + database_name + ";")

conn = psycopg2.connect(
    host = "localhost",
    database = "alarm_clock",
    user = "postgres",
    password = "?????",
    port = "5432"
)

#CREATING TABLE TO STORE DATE/TIME OF ALARM AND LOCATION OF TONE
cur.execute("CREATE TABLE alarm (alarm_date date, alarm_time time, tone_location text)")
conn.commit()

#DEF FUNCTION TO ADD ALARM TO DATABASE
def add_alarm():
    alarm_time = ""
    alarm_date = ""
    while alarm_time == "" and alarm_date == "":
        alarm_time = input("Set the alarm time (format: 23:59)")
        alarm_date = input("Set the alarm date (format: 2020-03-02")
    cur.execute("insert into alarm (alarm_date, alarm_time) values (%s,%s)", (alarm_date, alarm_time))
    conn.commit()
    print (f'Alarm successfully added - date: {alarm_date}, time: {alarm_time}')
    
#DEF FUNCTION TO SET ALARM
def set_alarm():
    cur.execute("select alarm_date, alarm_time from alarm")
    data = cur.fetchall()
    for index, i in enumerate(data):
        if None not in i:
            print(f'''Select date and time to set alarm:
{i} click {index}''')
        else:
            continue
    your_choice = int(input("Your choice: "))
    alarm = data[your_choice]
    date = alarm[0]
    time = alarm[1]
    data_str = date.strftime("%Y-%m-%d")
    time_str = time.strftime("%H:%M")
    data_time_str = data_str + " " + time_str
    return data_time_str
    
#DEF FUNCTION TO DELETE ALARM DATE/TIME OR TONE
def del_alarm_tone():
    action = int(input("""select what you would like to delete:
    0 - alarm
    1 - alarm tone"""))
    if action == 0:
        cur.execute("select alarm_date, alarm_time from alarm")
        data = cur.fetchall()
        for index, i in enumerate(data):
            if None not in i:
                print (f"""Select the date to delete:
                {i} click {index}""")
            else:
                continue
        your_choice = int(input("Your choice: "))
        cur.execute("delete from alarm where alarm_date = %s and alarm_time = %s", data[your_choice])
        conn.commit()
    if action == 1:
        cur.execute("select tone_location from alarm")
        data = cur.fetchall()
        for index, i in enumerate(data):
            if None not in i:
                print (f"""Select tone to delete:
{i} click {index}""")
            else:
                continue
        your_choice = int(input("Your choice: "))
        cur.execute("delete from alarm where tone_location = %s", data[your_choice])
        conn.commit()
        
#DEF FUNCTION TO ADD ALARM TONE
def add_alarm_tone():
    tone = ""
    while tone == "":
        tone = input("Put here tone's path: ")
    cur.execute("insert into alarm (tone_location) values (%s)", (tone,))
    conn.commit()
    tone_name = tone.split("\\")[-1]
    print (f'Alarm tone {tone_name} successfully added.')
    
#DEF FUNCTION TO SET ALARM TONE
def set_alarm_tone():
    cur.execute("select tone_location from alarm")
    data = cur.fetchall()
    for index, i in enumerate(data):
        if None not in i:
            print (f'''Possible tones to choose:
{i} click {index}''')
        else:
            continue
    your_choice = int(input("Your choice: "))
    alarm_tone = data[your_choice]
    return alarm_tone[0]
    
#GENERAL FUNCTIONALITY
def main():
    print("Set alarm time and alarm tone to turn on alarm clock")
    alarm_time = ""
    alarm_tone = ""
    while alarm_time == "" or alarm_tone == "":
        print("""
0 - add alarm,
1 - set alarm,
2 - add alarm tone,
3 - set alarm tone,
4 - delete alarm/alarm tone""")
        action = int(input("Select action: "))
        if action == 0:
            add_alarm()
        elif action == 1:
            alarm_time = set_alarm()
        elif action == 2:
            add_alarm_tone()
        elif action == 3:
            alarm_tone = set_alarm_tone()
        elif action == 4:
            del_alarm_tone()
        else:
            print ("Wrong action")

    time = "not now"
    while time != "now":
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M")
        if alarm_time == dt_string:
            pygame.mixer.init()
            pygame.display.set_mode([500, 500])
            pygame.mixer.music.load(alarm_tone)
            pygame.mixer.music.play()
            running = True
            while running:
                for event in pygame.event.get():
                    answer = input(
                        f"TIME TO GET UP! It's {alarm_time} - TYPE 'OK' TO TURN OFF")
                    if answer == 'OK':
                        pygame.mixer.music.stop()
                        break
                    elif event.type == pygame.QUIT:
                        running = False
                running = False
            time = "now"
        else:
            continue
            
#===========================================================================================================
  
#FULL FUNCIONALITY - Alarm clock Tkinter GUI application
import tkinter as tk
from tkinter import filedialog, Text
import psycopg2
import pygame
from datetime import datetime
import os

conn = psycopg2.connect(
    host = "localhost",
    database = "alarm_clock",
    user = "postgres",
    password = "????",
    port = "5432"
)

cur = conn.cursor()
root = tk.Tk()
should_tic_toc = None

def add_alarm():
    for widget in frame.winfo_children():
        widget.destroy()
    label_time = tk.Label(frame, text="Alarm time:")
    label_date = tk.Label(frame, text="Alarm date:")
    entry_time = tk.Entry(frame, width=50)
    entry_date = tk.Entry(frame, width=50)
    label_time.grid(row=0, column=0)
    entry_time.grid(row=0, column=1)
    label_date.grid(row=1, column=0)
    entry_date.grid(row=1, column=1)
    entry_time.insert(0, "Set the alarm time (format: 23:59)")
    entry_date.insert(0, "Set the alarm date (format: 2020-03-02)")
    def push_alarm_sql():
        cur.execute("insert into alarm (alarm_date, alarm_time) values (%s,%s)", (entry_date.get(), entry_time.get()))
        conn.commit()
        status_label = tk.Label(frame, text=f"Alarm successfully added - date: {entry_date.get()}, time: {entry_time.get()}")
        status_label.grid(row=3, column=1)
        def exit_menu():
            for widget in frame.winfo_children():
                widget.destroy()
        exit_button = tk.Button(frame, text="Back to menu", command=exit_menu)
        exit_button.grid(row=4, column=1)
    push_button = tk.Button(frame, text="CONFIRM", command=push_alarm_sql)
    push_button.grid(row=2, column=1)

def set_alarm():
    for widget in frame.winfo_children():
        widget.destroy()
    set_label = tk.Label(frame, text="Select date and time to set alarm:", font="Verdana 10 bold")
    set_label.grid(row=0, column=0)
    cur.execute("select alarm_date, alarm_time from alarm")
    data = cur.fetchall()
    rows = 1
    for index, i in enumerate(data):
        if None not in i:
            option_label = tk.Label(frame, text=f"""{i[0].strftime("%Y-%m-%d"),i[1].strftime("%H:%M")} - number: {index}""")
            option_label.grid(row=rows, column=0)
            rows += 1
        else:
            continue
    entry_label = tk.Label(frame, text="Choose number:")
    entry_label.grid(row=rows, column=0)
    choice = tk.Entry(frame, width=10)
    choice.grid(row=rows, column=1)
    rows2 = rows+1
    set_label2 = tk.Label(frame, text="Select tone for your alarm:", font="Verdana 10 bold")
    set_label2.grid(row=rows2, column=0)
    rows2 += 1
    cur.execute("select tone_location from alarm")
    data2 = cur.fetchall()
    for index, i in enumerate(data2):
        if None not in i:
            tone_name = i[0].split('\\')[-1]
            option_label = tk.Label(frame, text=f"{tone_name} - number: {index}")
            option_label.grid(row=rows2, column=0)
            rows2 += 1
        else:
            continue
    entry_label2 = tk.Label(frame, text="Choose number:")
    entry_label2.grid(row=rows2, column=0)
    choice2 = tk.Entry(frame, width=10)
    choice2.grid(row=rows2, column=1)
    def push_set_alarm():
        set_frame = tk.Frame(root, bg='white', highlightbackground="black", highlightthickness=1)
        set_frame.pack()
        alarm = data[int(choice.get())]
        print (alarm)
        date = alarm[0]
        time = alarm[1]
        data_str = date.strftime("%Y-%m-%d")
        time_str = time.strftime("%H:%M")
        global data_time_str #defining data_time_str as a global variable
        data_time_str = data_str + " " + time_str
        alarm_tone = data2[int(choice2.get())]
        alarm_tone_name = alarm_tone[0].split('\\')[-1]
        print (alarm_tone)
        info_label = tk.Label(set_frame, text=f"Your alarm clock is set to {data_time_str}\nAlarm tone: {alarm_tone_name}")
        info_label.grid(row=0, column=0)
        def current_time():
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M")
            return dt_string
        def tone_on():
            global should_tic_toc
            global data_time_str
            should_tic_toc = root.after(2000, tone_on)
            if data_time_str == current_time():
                root.after_cancel(should_tic_toc)
                def turn_off():
                    pygame.mixer.music.stop()
                    set_frame.destroy()
                    turn_off.destroy()
                pygame.mixer.init()
                pygame.display.set_mode([10, 10])
                pygame.mixer.music.load(alarm_tone[0])
                pygame.mixer.music.play()
                turn_off = tk.Button(root, text=f"TIME TO GET UP! It's {data_time_str} - CLICK TO TURN OFF", command=turn_off)
                turn_off.pack()
        tone_on()

    def exit_menu():
        for widget in frame.winfo_children():
            widget.destroy()

    push_button = tk.Button(frame, text="CONFIRM", command=push_set_alarm)
    push_button.grid(row=rows2+1, column=1)
    exit_button = tk.Button(frame, text="Back to menu", command=exit_menu)
    exit_button.grid(row=rows2+2, column=0)
def add_alaram_tone():
    for widget in frame.winfo_children():
        widget.destroy()
    tone_name = tk.filedialog.askopenfile(initialdir="/", title="Select '*.wav' File", filetypes=(("executables","*.exe"), ("all files", "*.*")))
    tone_label = tk.Label(frame, text=tone_name)
    tone_label.grid(row=0, column=0)
    def push_add_alarm():
        cur.execute("insert into alarm (tone_location) values (%s)", (str(tone_name).split("'")[1],))
        conn.commit()
        status = tk.Label(frame, text="Alarm tone successfully added.")
        status.grid(row=2, column=0)
        def exit_menu():
            for widget in frame.winfo_children():
                widget.destroy()
        exit_button = tk.Button(frame, text="Back to menu", command=exit_menu)
        exit_button.grid(row=3, column=0)
    push_button = tk.Button(frame, text="ADD", command=push_add_alarm)
    push_button.grid(row=1, column=0)


def del_alarm_tone():
    for widget in frame.winfo_children():
        widget.destroy()
    def opt_del_alarm():
        for widget in frame.winfo_children():
            widget.destroy()
        del_alarm_label = tk.Label(frame, text="Select date to delete:", font="Verdana 10 bold")
        del_alarm_label.grid(row=0, column=0)
        cur.execute("select alarm_date, alarm_time from alarm")
        data = cur.fetchall()
        rows = 1
        for index, i in enumerate(data):
            if None not in i:
                option_label = tk.Label(frame, text=f"""{i[0].strftime("%Y-%m-%d"),i[1].strftime("%H:%M")} - number: {index}""")
                option_label.grid(row=rows, column=0)
                rows += 1
            else:
                continue
        entry_label = tk.Label(frame, text="Choose number:")
        entry_label.grid(row=rows, column=0)
        choice = tk.Entry(frame, width=10)
        choice.grid(row=rows, column=1)
        def push_del():
            cur.execute("delete from alarm where alarm_date = %s and alarm_time = %s", data[int(choice.get())])
            conn.commit()
            succes_label = tk.Label(frame, text="Alarm successfully deleted.")
            succes_label.grid(row=rows+1, column=1)
            def exit_menu():
                for widget in frame.winfo_children():
                    widget.destroy()
            exit_button = tk.Button(frame, text="Back to menu", command=exit_menu)
            exit_button.grid(row=rows+2, column=1)
        push_button = tk.Button(frame, text="CONFIRM", command=push_del)
        push_button.grid(row=rows, column=2)
    def opt_del_tone():
        for widget in frame.winfo_children():
            widget.destroy()
        del_tone_label = tk.Label(frame, text="Select tone to delete:", font="Verdana 10 bold")
        del_tone_label.grid(row=0, column=0)
        cur.execute("select tone_location from alarm")
        data = cur.fetchall()
        rows = 1
        for index, i in enumerate(data):
            if None not in i:
                tone_name = i[0].split('\\')[-1]
                option_label = tk.Label(frame, text=f"{tone_name} - number: {index}")
                option_label.grid(row=rows, column=0)
                rows += 1
            else:
                continue
        entry_label = tk.Label(frame, text="Choose number:")
        entry_label.grid(row=rows, column=0)
        choice = tk.Entry(frame, width=10)
        choice.grid(row=rows, column=1)
        def push_del():
            cur.execute("delete from alarm where tone_location = %s", data[int(choice.get())])
            conn.commit()
            succes_label = tk.Label(frame, text="Alarm tone successfully deleted.")
            succes_label.grid(row=rows+1, column=1)
            def exit_menu():
                for widget in frame.winfo_children():
                    widget.destroy()
            exit_button = tk.Button(frame, text="Back to menu", command=exit_menu)
            exit_button.grid(row=rows+2, column=1)
        push_button = tk.Button(frame, text="CONFIRM", command=push_del)
        push_button.grid(row=rows, column=2)
    del_alarm = tk.Button(frame, text="Delete alarm", command=opt_del_alarm)
    del_tone = tk.Button(frame, text="Delete alarm tone", command=opt_del_tone)
    del_alarm.grid(row=0, column=0)
    del_tone.grid(row=0, column=1)


canvas = tk.Canvas(root, height=400, width=500, bg='#263D42')
canvas.pack()

frame = tk.Frame(root, bg='white')
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

button_frame = tk.LabelFrame(root, bg='#263D42', padx=10, pady=10)
button_frame.pack()

addAlarm = tk.Button(button_frame, text='Add alarm', width=20, command=add_alarm)
setAlarm = tk.Button(button_frame, text='Set alarm/alarm tone', width = 20, command=set_alarm)
addAlarmTone = tk.Button(button_frame, text='Add alarm tone', width = 20, command=add_alaram_tone)
delAlarmTone = tk.Button(button_frame, text='Delete alarm/alarm tone', width=20, command=del_alarm_tone)
addAlarm.grid(row=0, column=0)
setAlarm.grid(row=0, column=1)
addAlarmTone.grid(row=1, column=0)
delAlarmTone.grid(row=1, column=1)

root.mainloop()
