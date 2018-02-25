from bs4 import BeautifulSoup
import requests
import configfraz
import dcudates
import warnings
warnings.filterwarnings("ignore")

times = configfraz.times

days = configfraz.days

def dataset():
    data = {
    "Mon": {
        '8:00' : [],
        '8:30' : [],
        '9:00' : [],
        '9:30' : [],
        '10:00' : [],
        '10:30' : [],
        '11:00' : [],
        '11:30' : [],
        '12:00' : [],
        '12:30' : [],
        '13:00' : [],
        '13:30' : [],
        '14:00' : [],
        '14:30' : [],
        '15:00' : [],
        '15:30' : [],
        '16:00' : [],
        '16:30' : [],
        '17:00' : [],
        '17:30' : [],
    },
    "Tue": {
        '8:00' : [],
        '8:30' : [],
        '9:00' : [],
        '9:30' : [],
        '10:00' : [],
        '10:30' : [],
        '11:00' : [],
        '11:30' : [],
        '12:00' : [],
        '12:30' : [],
        '13:00' : [],
        '13:30' : [],
        '14:00' : [],
        '14:30' : [],
        '15:00' : [],
        '15:30' : [],
        '16:00' : [],
        '16:30' : [],
        '17:00' : [],
        '17:30' : [],
        
    },
    "Wed": {
        '8:00' : [],
        '8:30' : [],
        '9:00' : [],
        '9:30' : [],
        '10:00' : [],
        '10:30' : [],
        '11:00' : [],
        '11:30' : [],
        '12:00' : [],
        '12:30' : [],
        '13:00' : [],
        '13:30' : [],
        '14:00' : [],
        '14:30' : [],
        '15:00' : [],
        '15:30' : [],
        '16:00' : [],
        '16:30' : [],
        '17:00' : [],
        '17:30' : [],
        
    },
    "Thu": {
        '8:00' : [],
        '8:30' : [],
        '9:00' : [],
        '9:30' : [],
        '10:00' : [],
        '10:30' : [],
        '11:00' : [],
        '11:30' : [],
        '12:00' : [],
        '12:30' : [],
        '13:00' : [],
        '13:30' : [],
        '14:00' : [],
        '14:30' : [],
        '15:00' : [],
        '15:30' : [],
        '16:00' : [],
        '16:30' : [],
        '17:00' : [],
        '17:30' : [],
        
    },
    "Fri": {
        '8:00' : [],
        '8:30' : [],
        '9:00' : [],
        '9:30' : [],
        '10:00' : [],
        '10:30' : [],
        '11:00' : [],
        '11:30' : [],
        '12:00' : [],
        '12:30' : [],
        '13:00' : [],
        '13:30' : [],
        '14:00' : [],
        '14:30' : [],
        '15:00' : [],
        '15:30' : [],
        '16:00' : [],
        '16:30' : [],
        '17:00' : [],
        '17:30' : [],
        
    },
    "Sat": {
        '8:00' : [],
        '8:30' : [],
        '9:00' : [],
        '9:30' : [],
        '10:00' : [],
        '10:30' : [],
        '11:00' : [],
        '11:30' : [],
        '12:00' : [],
        '12:30' : [],
        '13:00' : [],
        '13:30' : [],
        '14:00' : [],
        '14:30' : [],
        '15:00' : [],
        '15:30' : [],
        '16:00' : [],
        '16:30' : [],
        '17:00' : [],
        '17:30' : [],
       
    },
    "Sun": {
        '8:00' : [],
        '8:30' : [],
        '9:00' : [],
        '9:30' : [],
        '10:00' : [],
        '10:30' : [],
        '11:00' : [],
        '11:30' : [],
        '12:00' : [],
        '12:30' : [],
        '13:00' : [],
        '13:30' : [],
        '14:00' : [],
        '14:30' : [],
        '15:00' : [],
        '15:30' : [],
        '16:00' : [],
        '16:30' : [],
        '17:00' : [],
        '17:30' : [],
        
        },
    }
    return data

#Handles list results
def responsehandler(l):
    s = ""
    for x in l:
        s = s + x + "\n"
    if len(l) == 0:
        s = "Nothing On"
    return s

#Handles Dictionary Results
def dictionaryhandler(d):
    s = ""
    check = True
    for key in d.keys():
        s = s + key + " " + "\n".join(d[key]) + "\n"
        if d[key] != [] and check:
            check = False
    if check:
        s = "Nothing On Today"
    return s

#Locates the TR IDs from the DCU website
#This must be done to account for multiple rows
def getdays(x):
    days_id = []
    for i in range(0, len(x)):
        c = x[i].get_text().split("\n")
        if c[1] in days:
            xstring = str(x[i])
            rowspan = xstring.split("rowspan")[1][2]
            rowspan = int(rowspan)
            days_id.append([i])
            prevadditional = 0
            for iii in range(rowspan-1):
                toincrease = xstring.count("<tr")
                if prevadditional == 0:
                    additional = i + toincrease
                else:
                    additional = toincrease + prevadditional

                xstring = str(x[additional])
                prevadditional = additional
                days_id[len(days_id) - 1].append(additional)
    return days_id

#Builds and returns a string, s
def timetableparser(x, i, day, data):
    i = i
    t = 2 
    le_flag = False
    s = ""
    while i < len(x) and t < 21:
        if le_flag:
            data[day][times[t]].append(s)
            le_flag = False
            t = t + 1
            continue
        if x[i] != "":
            s = "\n", x[i+9], "\nIn ", x[i+1], "\nWith ", x[i+8] + "\n"
            s = "".join(str(i) for i in s)
            s = "\n" + s
            data[day][times[t]].append(s)
            i = i + 22
            t += 1
            le_flag = True
        else:
            i = i + 1
            t = t + 1
    return s

def normal(days_id, x, data):
    for dayidmini in days_id:
        for i in range(0, len(dayidmini)):
            dayid = dayidmini[i]
            y = x[dayid].get_text().split("\n")
            if y[1] != "":
                day = y[1]
            if i == 0:
                #print("Today is:", day)
                timetableparser(y, 2, day, data)
            else:
                timetableparser(y, 1, day, data)
    return data

def run(day, time=False, code="CA", year="1"):
    data = dataset()
    page = requests.get("https://www101.dcu.ie/timetables/feed.php?prog="+code+"&per="+year+"&week1=20&week2=31&hour=1-20&template=student", verify=False)
    soup = BeautifulSoup(page.content, 'html.parser')
    x = soup.find_all("tr")
    days_id = getdays(x)
    all_data = data
    all_data = normal(days_id, x, data)
    if time:
        return all_data[day][time]
    else:
        return all_data[day]

def beautify(datacontent):
    s = ""
    if type(datacontent) == dict:
        for key in datacontent.keys():
            for x in datacontent[key]:
                s = s + "---" + x
            if s == "":
                s = "Nothing"
            print("At", key, "There is", s)
            s = ""
    elif type(datacontent) == list:
        if len(datacontent) < 1:
            print("Nothing")
        for x in datacontent:
            print(x)

def next(code="CA", year="1"):
    day = dcudates.getday()
    time = dcudates.nexttime()
    if time in days:
        return dictionaryhandler(run(time, None, code, year))
    else:
        return responsehandler(run(day, time, code, year))

def gettoday(code="CA", year="1"):
    day = dcudates.getday()
    return run(day, None, code, year)

def main():
    while True:
        print("Enter a Day")
        day = input()
        if day == "next":
            code = input()
            print(beautify(next(code)))
            continue
        if day not in days:
            print("Warning: Day not valid if entered")
        print("Enter a time")
        time = input()
        if time not in configfraz.timechecks:
            print("Warning: Time not valid if entered")
        print("Enter a module code")
        code = input()
        print("Fetching results:")

        if time == "":
            time = None
        if day == "":
            day = None
        if code == "":
            code = None

        beautify(run(day, time, code))    

if __name__ == '__main__':
    main()