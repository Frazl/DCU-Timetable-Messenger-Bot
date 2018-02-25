import datetime
import configfraz

def getday():
    now = datetime.datetime.now()
    today = now.strftime("%A")[:3]
    today = today
    return today

def gettomorrow():
    today = int(datetime.datetime.now().weekday())
    if today != 6:
        today = today + 1
    else:
        today = 0 
    return configfraz.days[today]


def nexttime():
    now = datetime.datetime.now()
    hour = int(now.strftime("%H"))
    minute = int(now.strftime("%M"))
    if hour > 16:
        s = gettomorrow()
        return s
    elif hour < 8:
        hour = "8:00"
        return hour
    else:
        if minute >= 30:
            minute = 30
        else:
            minute = 0
        hour += 1
        s = str(hour)+":"+str(minute)
        if len(s) < 5:
            s = s + "0"
        return s