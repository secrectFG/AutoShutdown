
from logging.config import stopListening
import time
import os
import PySimpleGUI as sg
from psgtray import SystemTray
import stopwatch

def getdatetime():
    return time.gmtime().tm_hour+8,time.gmtime().tm_min

menu = ['', ['显示窗口', '隐藏窗口',  '---',  '退出']]
title = '定时关机程序'

hour = 22
min = 40

layout = [
    [sg.T('到'),sg.Input(str(hour),key="in_hour",size=(5,10)),sg.T('时'),sg.Input(str(min),key="in_min",size=(5,10)),sg.T('分关机'),],
    [sg.T('剩余时间',key='_LB_')],
    [sg.B("隐藏"),sg.B("退出")]
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
    # print(event,'===',values)
    
    if event =='-WINDOW CLOSE ATTEMPTED-':
        window.hide()
    if event == '-TRAY-':
        event = values[event]
        if event in ('显示窗口', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()
        elif event in ('隐藏窗口', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            window.hide()
            tray.show_icon()        # if hiding window, better make sure the icon is visible
    if event =='退出':
        break
    if event =='隐藏':
        window.hide()
        tray.show_icon()
        
    try:
        hour = int(values['in_hour'])
        min = int(values['in_min'])
    except:
        window['in_hour'].update('23')
        window['in_min'].update('59')
    h,m = getdatetime()
    lefthour = hour-h
    leftmin = min-m
    if leftmin<0:
        leftmin = min-m+lefthour*60
        lefthour-=1

    window['_LB_'].update(f'剩余{lefthour}小时 {leftmin}分钟')
    if lefthour<=0 and leftmin<=0 and sw.duration>120:
        os.system("shutdown /s /t 120")
        break
tray.close()            # optional but without a close, the icon may "linger" until moused over
window.close()
# def shutdown(hour,min):
#     while True:
#         h,m = getdatetime()
#         lefthour = hour-h
#         leftmin = min-m
#         if leftmin<0:
#             leftmin = min-m+lefthour*60
#             lefthour-=1

#         print(f'剩余{lefthour}小时 {leftmin}分钟')
#         if lefthour<=0 and leftmin<=0:
#             break
#         time.sleep(10)
    # os.system("shutdown /s /t 30")

# shutdown(20,29)
