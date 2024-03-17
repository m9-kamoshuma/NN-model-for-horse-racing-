from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Input, concatenate, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.python.keras.utils.vis_utils import plot_model
import numpy as np
import pickle


### データ処理 ###

# データインポート
f = open("C:/Users/shuma/python_practice/horse_ai/data/racehorse_data.txt","rb")
racehorse_data = pickle.load(f)

for i in range(len(racehorse_data)):
    race=racehorse_data[i]
    while len(race)!=18:
        race.append('')

racehorse_data = np.array(racehorse_data)
course_condition_data = np.array(np.load('C:/Users/shuma/python_practice/horse_ai/data/course_condition_data.npy'))
placetype_data = np.array(np.load('C:/Users/shuma/python_practice/horse_ai/data/placetype_data.npy'))
weather_data = np.array(np.load('C:/Users/shuma/python_practice/horse_ai/data/weather_data.npy'))
length_data = np.array(np.load('C:/Users/shuma/python_practice/horse_ai/data/length_data.npy'))
rank_data = np.array(np.load('C:/Users/shuma/python_practice/horse_ai/data/rank_data.npy'))

# データ中の全ての馬のリスト作成
list_horse=[]
for i in range(len(racehorse_data)):
    horses=racehorse_data[i]
    for j in range(len(horses)):
        horse=horses[j]
        if (horse in list_horse)==False:
            list_horse.append(horse)

# データの変形
weather=[]
for i in range(len(weather_data)):
    if weather_data[i]=="晴":
        weather.append(np.array([1,0,0]))
    elif weather_data[i]=="雨":
        weather.append(np.array([0,1,0]))
    else:
        weather.append(np.array([0,0,1]))
weather=np.array(weather)
weather_data=weather

course_condition=[]
for i in range(len(course_condition_data)):
    if course_condition_data[i]=="良":
        course_condition.append(np.array([1,0,0]))
    elif course_condition_data[i]=="不":
        course_condition.append(np.array([0,1,0]))
    else:
        course_condition.append(np.array([0,0,1]))
course_condition=np.array(course_condition)
course_condition_data=course_condition

placetype=[]
for i in range(len(placetype_data)):
    if placetype_data[i]=="芝":
        placetype.append(np.array([1,0,0]))
    elif placetype_data[i]=="ダートダート":
        placetype.append(np.array([0,1,0]))
    else:
        placetype.append(np.array([0,0,1]))
placetype=np.array(placetype)
placetype_data=placetype

racehorses=[]
for i in range(len(racehorse_data)):
    racehorse=[]
    horses=racehorse_data[i]
    for j in range(len(horses)):
        horse=horses[j]
        race=[0]*18
        if (horse in list_horse)==True:
            num10=list_horse.index(horse)
            num2=bin(num10)
            num2_list=list(num2)
            for i in range(2, len(num2_list)):
                race[i]=int(num2_list[i])
        racehorse.append(race)
    racehorses.append(racehorse)
racehorse_data2=np.array(racehorses)

x1_train,x1_test, x2_train,x2_test, x3_train,x3_test, x4_train,x4_test, x5_train,x5_test, y_train,y_test = train_test_split(racehorse_data2, course_condition_data, weather_data, placetype_data, length_data, rank_data, test_size=0.2, random_state=4)


### モデル構築 ###

# 入力の次元
num_racehorse = 18
num_course_condition = 4
num_weather = 4
num_placetype = 4
num_length = 4

# 入力を定義
racehorse_input = Input(shape=(18,18))
course_condition_input = Input(shape=(3,))
weather_input = Input(shape=(3,))
placetype_input = Input(shape=(3,))
length_input = Input(shape=(1,))

# racehorse_inputから結合前まで
x1=Flatten(input_shape=(18, 18))(racehorse_input)
x1 = Dense(100, activation="relu")(x1)
x1 = Model(inputs=racehorse_input, outputs=x1)

# course_condition_inputから結合前まで
x2 = Dense(32, activation="relu")(course_condition_input)
x2 = Model(inputs=course_condition_input, outputs=x2)

# weather_inputから結合前まで
x3 = Dense(32, activation="relu")(weather_input)
x3 = Model(inputs=weather_input, outputs=x3)

# placetype_inputから結合前まで
x4 = Dense(32, activation="relu")(placetype_input)
x4 = Model(inputs=placetype_input, outputs=x4)

# length_inputから結合前まで
x5 = Dense(1, activation="relu")(length_input)
x5 = Model(inputs=length_input, outputs=x5)


# 結合
combined = concatenate([x1.output, x2.output, x3.output, x4.output, x5.output])

# 密結合
z = Dense(2048, activation="tanh")(combined)
z = Dense(18, activation="sigmoid")(z)

# モデル定義とコンパイル
model = Model(inputs=[x1.input, x2.input, x3.input, x4.input, x5.input], outputs=z)

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
model.summary()

# 学習
history = model.fit([x1_train, x2_train, x3_train, x4_train, x5_train], y_train, epochs=100)
