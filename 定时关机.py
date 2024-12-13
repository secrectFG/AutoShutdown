import time
import os
import PySimpleGUI as sg
from psgtray import SystemTray
import stopwatch

# Function to get the current time adjusted to your timezone
def getdatetime():
    return time.gmtime().tm_hour + 8, time.gmtime().tm_min

# Function to load saved hour and minute
def load_saved_time():
    try:
        with open("time_config.txt", "r") as f:
            hour, min = map(int, f.read().split(','))
    except FileNotFoundError:
        # Default time if file doesn't exist
        hour, min = 22, 40
    return hour, min

# Function to save the current hour and minute
def save_time(hour, min):
    try:
        with open("time_config.txt", "w") as f:
            f.write(f"{hour},{min}")
    except:
        pass

# Load saved time
hour, min = load_saved_time()

menu = ['', ['显示窗口', '隐藏窗口', '---', '退出']]
title = '定时关机程序'

layout = [
    [sg.T('到'), sg.Input(str(hour), key="in_hour", size=(5, 10)), sg.T('时'),
     sg.Input(str(min), key="in_min", size=(5, 10)), sg.T('分关机')],
    [sg.T('剩余时间', key='_LB_')],
    [sg.B("隐藏"), sg.B("退出")]
]

window = sg.Window(title, layout, finalize=True, enable_close_attempted_event=True)
tray = SystemTray(menu, single_click_events=False, window=window, tooltip=title)
leftmin = 0

window.hide()
tray.show_icon()

sw = stopwatch.Stopwatch()
sw.start()

while True:
    event, values = window.read(timeout=500)
    
    if event == '-WINDOW CLOSE ATTEMPTED-':
        window.hide()
    
    if event == '-TRAY-':
        event = values[event]
        if event in ('显示窗口', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()
        elif event in ('隐藏窗口', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            window.hide()
            tray.show_icon()
    
    if event == '退出':
        break

    if event == '隐藏':
        window.hide()
        tray.show_icon()

    try:
        hour1 = int(values['in_hour'])
        min1 = int(values['in_min'])
        #判断是否改变
        if hour1 != hour or min1 != min:
            hour = hour1
            min = min1
            save_time(hour, min)  # Save the new time
    except:
        window['in_hour'].update('23')
        window['in_min'].update('59')

    h, m = getdatetime()
    lefthour = hour - h
    leftmin = min - m
    if leftmin < 0:
        leftmin = min - m + lefthour * 60
        lefthour -= 1
    window['_LB_'].update(f'剩余{lefthour}小时 {leftmin}分钟')

    if lefthour <= 0 and leftmin <= 0 and sw.duration > 120:
        os.system("shutdown /s /t 120")
        break

tray.close()  # optional but without a close, the icon may "linger" until moused over
window.close()
