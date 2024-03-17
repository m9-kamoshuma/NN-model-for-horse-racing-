import requests
from bs4 import BeautifulSoup
import re


# URL用の数字出力関数
def Num(num):
    if num<10:
        num='0'+str(num)
    else:
        num=str(num)
    return num

def get_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    info = soup.find('div', class_="RaceData01")
    if info != None:
        info=info.get_text(strip=True)
        return info
    else:
        return 0


def get_info_course_condition(info):
    info_place=[]
    if ('良' in info)==True:
        info_place='良'
    elif ('稍' in info)==True:
        info_place='稍'
    elif ('重' in info)==True:
        info_place='重'
    else:#不
        info_place='不'
    return info_place


def get_info_weather(info):
    info_weather=[]
    if ('晴' in info)==True:
        info_weather='晴'
    elif ('曇' in info)==True:
        info_weather='曇'
    else:#雨
        info_weather='雨'
    
    return info_weather

def get_info_placetype(info):
    info_placetype=[]
    if ('芝' in info)==True:
        info_placetype='芝'
    elif ('障' in info)==True:
        info_placetype='障'
    else:#ダート
        info_placetype='ダートダート'
        
    return info_placetype


def get_info_length(info):
    info_length=[]
    info_length = re.findall(r"\d+", info)
    info_length = int(info_length[2])
    return info_length


def get_info_racehorse(url,list):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    info_race_horses =soup.find_all(class_="Horse_Name")
    info_waku =soup.find_all(class_="Num Txt_C")

    info_racehorses=[]
    tmp1=[]
    tmp2=[]
    rank=[]
    if info_race_horses!=[]:
        for race_horse in info_race_horses:
                horses=race_horse.find_all("a")
                for horse in horses:
                    horse=horse.get_text()
                    if (horse in list) == False:
                        info_racehorses=0
                        rank=0
                        return info_racehorses,rank
                    else:
                        info_racehorses.append(horse)
        for waku in info_waku:
                waku=int(waku.find('div').get_text())
                tmp1.append(waku)
        info_waku=tmp1
        for i in range(1,len(info_waku)+1):
            num=info_waku.index(i) 
            horse=info_racehorses[num]
            tmp2.append(horse) 
            rank.append(num+1)
            
    return info_racehorses,rank





