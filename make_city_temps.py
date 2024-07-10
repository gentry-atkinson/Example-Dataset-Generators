# Author: Gentry Atkinson (gatkins0@stedwards.edu)
# Organization: St. Edwards Universtiy
# Date: 10 July, 2024

import random
import pandas as pd
import numpy as np

START_YEAR = 2010
FINAL_YEAR = 2023
START_MEAN_TEMP = 21

CITY_MEAN_TEMP_OFFSET = {
    "Sydney" : 0.5,
    "Hong Kong" : 7.0,
    "Seattle" : 0.0,
    "Frankfurt" : -10.0,
    "Ottawa" : -3.0,
    "Buenos Aires" : -2.5,
    "Nairobi" : -0.6
}

CITY_TEMP_SWING = {
    "Sydney" : 1.2,
    "Hong Kong" : 1.3,
    "Seattle" : 0.5,
    "Frankfurt" : 0.2,
    "Ottawa" : 1.1,
    "Buenos Aires" : 1.8,
    "Nairobi" : 1.4
}

CITY_LAT_LONG = {
    "Sydney" : ('33.9S', '151.2E'),
    "Hong Kong" : ('22.3N', '114.2E'),
    "Seattle" : ('47.6N', '112.3W'),
    "Frankfurt" : ('50.1N', '8.9E'),
    "Ottawa" : ('45.4N', '75.7W'),
    "Buenos Aires" : ('34.6S', '53.4W'),
    "Nairobi" : ('1.3S', '36.8E')
}

HEMI = {
    "North" : ["Hong Kong", "Seattle", "Frankfurt", "Ottawa"],
    "South" : ["Sydney", "Buenos Aires", "Nairobi"]
}

AVG_DAY = {
    "00:00" : 3.0, "01:00" : 2.0, "02:00" : 1.5, "03:00" : 1.0,
    "04:00" : 0.5, "05:00" : 0.5, "06:00" : 0.0, "07:00" : 0.0,
    "08:00" : 0.5, "09:00" : 1.0, "10:00" : 2.0, "11:00" : 3.0,
    "12:00" : 4.0, "13:00" : 5.5, "14:00" : 7.0, "15:00" : 8.5,
    "16:00" : 9.0, "17:00" : 9.0, "18:00" : 8.5, "19:00" : 8.0,
    "20:00" : 7.0, "21:00" : 6.0, "22:00" : 5.0, "23:00" : 4.0,
}

SEASON_OFFSET = {
    "Spring" : 0.0,
    "Summer" : 2.0,
    "Fall" : -0.5,
    "Winter" : -2.0 
}

SEASON_MONTHS = {
    "Spring" : ['Mar', 'Apr', 'May'],
    "Summer" : ['Jun', 'Jul', 'Aug'],
    "Fall" : ['Sep', 'Oct', 'Nov'],
    "Winter" : ['Dec', 'Jan', 'Feb'] 
}

MONTHS = {'Jan':31, 'Feb':28, 'Mar':31, 
          'Apr':30, 'May':31, 'Jun':30, 
          'Jul':31, 'Aug':31, 'Sep':30,
          'Oct':31, 'Nov':30, 'Dec':31}

if __name__ == '__main__':
    cities = []
    dates = []
    temps = []
    lats = []
    longs = []
    mean_temp = START_MEAN_TEMP
    for year in range(START_YEAR, FINAL_YEAR+1):
        for month in random.sample(list(MONTHS.keys()), random.randint(4, 12)):
            for day in random.sample(list(range(1, 29)), random.randint(2, 21)):
                city = random.choice(list(CITY_MEAN_TEMP_OFFSET.keys()))
                date = str(year) + '-' + month + '-' + str(day)
                temp = AVG_DAY.copy()
                day_offset = random.gauss(0,1)
                hem = 'North' if 'N' in CITY_LAT_LONG[city][0] else 'South'
                for s, m in SEASON_MONTHS.items():
                    if month in m:
                        season = s
                        break
                s_o = SEASON_OFFSET[season]
                s_o *= CITY_TEMP_SWING[city]
                if hem == 'South':
                    s_o *= -1.0
                for hour in temp:
                    temp[hour] *= CITY_TEMP_SWING[city]
                    temp[hour] += mean_temp
                    temp[hour] += s_o
                    temp[hour] += random.gauss(0,1)
                cities.append(city)
                dates.append(date)
                temps.append(temps)
                lats.append(CITY_LAT_LONG[city][0])
                longs.append(CITY_LAT_LONG[city][1])
        mean_temp += random.gauss(0.5, 0.2)
        print(f'Completed {year}')
    print('All temps generated')
    
    table = pd.DataFrame.from_dict({
        'Date' : dates,
        'City': cities,
        'Latitude' : lats,
        'Longitude' : longs,
        #'Recorded Hourly Temperatures' : temps
    })
    print(table.head(10))
                    
