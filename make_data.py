import NN
import numpy as np

num_place=5
num_held=5
num_day=5
num_race=5
s_year=10
e_year=15

num_data=num_place*num_held*num_day*num_race

course_condition_data = []
weather_data = []
placetype_data = []
length_data = []
racehorse_data = []
rank_data = []

horse_list = np.load('C://data/horse_list.npy')

for year in range(s_year,e_year):
    for place in range(1,num_place):
        for held in range(1,num_held):
            for day in range(1,num_day):
                for race in range(1,num_race):

                    url="https://race.netkeiba.com/race/result.html?race_id=20"+str(year)+NN.Num(place)+NN.Num(held)+NN.Num(day)+NN.Num(race)+"&rf=race_list"
                    info=NN.get_info(url)
                    if info == 0:
                        continue

                    [info_racehorses,info_rank]=NN.get_info_racehorse(url,horse_list)

                    if info_racehorses==0:
                        continue #リストに馬が居なかったらそのれーすの情報は訓練データにしないで次のレースにスキップ
                        
                    info_course_condition=NN.get_info_course_condition(info)
                    info_weather=NN.get_info_weather(info)
                    info_placetype=NN.get_info_placetype(info)
                    info_length=NN.get_info_length(info)

                    racehorse_data.append(info_racehorses)     
                    course_condition_data.append(info_course_condition)
                    weather_data.append(info_weather)
                    placetype_data.append(info_placetype)
                    length_data.append(info_length)
                    rank_data.append(info_rank)


# データ保存
np.save('C://data/racehorse_data.npy', racehorse_data)
np.save('C://data/course_condition_data.npy', course_condition_data)
np.save('C://data/weather_data.npy', weather_data)
np.save('C://data/placetype_data.npy', placetype_data)
np.save('C://data/length_data.npy', length_data)
np.save('C://data/racehorse_data.npy', racehorse_data)

for i in range(len(rank_data)):
    while len(rank_data[i])<18:
        rank_data[i].append(0)
np.save('C://data/rank_data.npy', rank_data)

