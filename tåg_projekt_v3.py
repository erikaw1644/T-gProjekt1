import datetime
import time
import requests

#gör om textfilen till en dicttionary

def avgångar(filename):
    with open(filename, "r", encoding = "utf-8") as file:
        for line in file:
            line = line.strip().split(",")
            line = [x.split('":"') for x in line]
            line = {a.replace('"', "" ) : b.replace('"', "" ) for a, b in line}
    return line

api_key = '57ba6c3a29fcb1bef4d8e0213406d71b' #Nyckel till OpenWeather API
tid = datetime.datetime.now()
formatted_time = tid.strftime("%H:%M")
print("KLockan är: " + formatted_time)


#Formaterar tiden till formatet vi vill ha
morning_time = datetime.datetime(tid.year, tid.month, tid.day, 5, 0)
day_time = datetime.datetime(tid.year, tid.month, tid.day, 11, 0)
evening_time = datetime.datetime(tid.year, tid.month, tid.day, 17, 0)
night_time = datetime.datetime(tid.year, tid.month, tid.day, 23, 59)

#Avgör vilken fil med tågtider som ska användas, beroende på tiden
if morning_time <= tid < day_time:
    avgångar_dict = avgångar("avgångar_morgon.txt")

elif day_time <= tid < evening_time:
    avgångar_dict = avgångar("avgångar_dag.txt")

elif evening_time <= tid <= night_time:
    avgångar_dict = avgångar("avgångar_kväll.txt")

elif tid < morning_time:
    avgångar_dict = avgångar("avgångar_natt.txt")


else:
    print("Kan inte jämföra tiderna")

avgångar_dict["tid_Nu"] = formatted_time


def Sorterade_Avgångar():
    avgångar_sorterade_tid = sorted(avgångar_dict.items(), key=lambda avgångar_dict:avgångar_dict[1])
    avgångar_sorterade = dict(avgångar_sorterade_tid)
    print("Sorterade avgångar efter tid tidigast-senast:")
    print()
    for i in avgångar_sorterade:
        print(f"{i}  {avgångar_sorterade[i]}")
    print()
    
#Nästa 5:
    key = 'tid_Nu'
    temp = list(avgångar_sorterade)

    n = 1
    print("Nästa 5 avgångar är: ")
    print()
    for i in range(5):
        try: 
            nästa5 = temp[temp.index(key) + n]
        except (ValueError, IndexError): 
            nästa5 = None
        n+=1 
        print(str(nästa5))
    print()

Sorterade_Avgångar()

Avgångar_Morgon = avgångar("avgångar_morgon.txt")
Avgångar_Dag = avgångar("avgångar_dag.txt")
Avgångar_Kväll = avgångar("avgångar_kväll.txt")
Avgångar_Natt =  avgångar("avgångar_natt.txt")

def resa():
    destination = input("Vart vill du resa? ")
    
    for i in avgångar_dict:
        if destination == f"{i}":
            print("Dagens avgångar till "+destination+ " går dessa tider: ")
            print(Avgångar_Morgon[destination])
            print(Avgångar_Dag[destination])
            print(Avgångar_Kväll[destination])
            print(Avgångar_Natt[destination])
            print()
            print("Vädret i "+destination+": ")
            weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={destination}&units=metric&lang=sv&APPID={api_key}")
            weather_data = weather_data.json()
            
            find_description = weather_data["weather"]
            description = find_description[0]["description"]
            
            find_temperature = weather_data["main"]
            temperature = find_temperature["temp"]
            
            print(f"{description}, temperatur: {temperature}{chr(176)}C")
            
            
resa()     
