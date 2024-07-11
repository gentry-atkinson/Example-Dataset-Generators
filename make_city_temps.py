# Author: Gentry Atkinson (gatkins0@stedwards.edu)
# Organization: St. Edwards Universtiy
# Date: 10 July, 2024

import random
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

START_YEAR = 2000
FINAL_YEAR = 2023
WITH_NOISE = True
START_MEAN_TEMP = 19

CITY_MEAN_TEMP_OFFSET = {
    "Sydney" : 0.5,
    "Hong Kong" : 7.0,
    "Seattle" : -2.0,
    "Frankfurt" : -10.0,
    "Ottawa" : -3.0,
    "Buenos Aires" : -2.5,
    "Nairobi" : 3.0
}

CITY_TEMP_SWING = {
    "Sydney" : 1.2,
    "Hong Kong" : 1.3,
    "Seattle" : 0.5,
    "Frankfurt" : 0.4,
    "Ottawa" : 1.4,
    "Buenos Aires" : 1.5,
    "Nairobi" : 0.8
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

CITY_COLORS = {
    "Sydney" : 'red',
    "Hong Kong" : 'orange',
    "Seattle" : 'blue',
    "Frankfurt" : 'green',
    "Ottawa" : 'black',
    "Buenos Aires" : 'purple',
    "Nairobi" : 'yellow'
}

# Annual rainy days
CITY_PRECIP = {
    "Sydney" : 60,
    "Hong Kong" : 136,
    "Seattle" : 165,
    "Frankfurt" : 108,
    "Ottawa" : 67,
    "Buenos Aires" : 102,
    "Nairobi" : 50
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
    "Summer" : 10.0,
    "Fall" : -2.5,
    "Winter" : -12.0 
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

def get_ordered_sample(l: list, n=1) -> list:
    idxs = random.sample(list(range(len(l))), n)
    idxs.sort()
    return [l[i] for i in idxs]

if __name__ == '__main__':
    cities = []
    dates = []
    temps = []
    lats = []
    longs = []
    precips = []
    mean_temp = START_MEAN_TEMP
    for year in range(START_YEAR, FINAL_YEAR+1):
        for month in get_ordered_sample(list(MONTHS.keys()), random.randint(6, 12)):
            for day in get_ordered_sample(list(range(1, MONTHS[month]+1)), random.randint(10, 21)):
                city = random.choice(list(CITY_MEAN_TEMP_OFFSET.keys()))
                date = str(year) + '-' + month + '-' + str(day)
                temp = AVG_DAY.copy()

                # Small constant shift for the day
                day_offset = random.gauss(0,1)

                # Determine if the day is raining
                if random.randint(1, 365) >= CITY_PRECIP[city]:
                    precip = "None"
                else:
                    precip = round(random.gauss(4*CITY_PRECIP[city]/365, 0.1), 2)

                # Determine the season of the month
                for s, m in SEASON_MONTHS.items():
                    if month in m:
                        season = s
                        break

                # Get a slightly randomized shift to reflect the season
                s_o = random.gauss(SEASON_OFFSET[season], 2)
                s_o *= CITY_TEMP_SWING[city]
                if 'N' in CITY_LAT_LONG[city][0]:
                    s_o *= -1.0

                # Iterate over hours in day, adding shifts to the AVG_DAY
                for hour in temp:
                    temp[hour] *= CITY_TEMP_SWING[city]
                    temp[hour] += mean_temp
                    temp[hour] += CITY_MEAN_TEMP_OFFSET[city]
                    temp[hour] += s_o
                    temp[hour] += day_offset
                    temp[hour] += random.gauss(0,1) # hour offset
                    # TREND- rainy days are slighty cooler
                    if precip != 'None':
                        temp[hour] -= random.gauss(2, 0.5)
                    temp[hour] = round(temp[hour], 3)

                # Add all values to columns lists
                cities.append(city)
                dates.append(date)
                temps.append(temp)
                lats.append(CITY_LAT_LONG[city][0])
                longs.append(CITY_LAT_LONG[city][1])
                precips.append(precip)

        # TREND - mean temp increases slightly every year
        mean_temp += random.gauss(0.1, 0.1)
        print(f'Completed {year}')
    print('All temps generated')

    if WITH_NOISE:
        # NUISANCE- some lats and longs have time values
        for i in random.sample(range(0, len(cities)), len(cities)//100):
            lats[i] = '00:00'
            longs[i] = '00:00'

        # NUISANCE- some cities in all caps with truncated names
        for i in random.sample(range(0, len(cities)), len(cities)//100):
            cities[i] = cities[i].upper()[:-1*random.randint(1, 3)]

        # NUISANCE- some dates are in a different format
        for i in random.sample(range(0, len(cities)), len(cities)//100):
            year, month, day = dates[i].split('-')
            dates[i] = str(day) + '/' + month + '/' + str(year)

        # NOISE- some days have been entered in farenheit
        for i in random.sample(range(0, len(cities)), len(cities)//100):
            for time in AVG_DAY:
                temps[i][time] = temps[i][time]*1.8 + 32
        
        # NOISE- some NaN values have been entered as temps
        for i in random.sample(range(0, len(cities)), len(cities)//100):
            time = random.choice(list(AVG_DAY.keys()))
            temps[i][time] = float('nan')

        # NOISE- some days are missing temperature values after noon
        for i in random.sample(range(0, len(cities)), len(cities)//100):
            temps[i] = {time:temps[i][time] for time in list(AVG_DAY.keys())[0:12]}

    
    table = pd.DataFrame.from_dict({
        'Date' : dates,
        'City': cities,
        'Latitude' : lats,
        'Longitude' : longs,
        'Measured Temperatures (Celsius)' : temps,
        'Rainfall (cm)' : precips
    })
    print(table.head(10))
    print(f"Total number of rows: {len(table)}")

    table.to_json("City_Temperatures.json")
    table.to_excel("City_Temperatures.xlsx")

    if not WITH_NOISE:
        plt.figure()
        for idx in table.index:
            plt.scatter(
                max(temps[idx].values()), 
                min(temps[idx].values()),
                c=CITY_COLORS[cities[idx]],
            )
        plt.title("All measured max and min temps")
        plt.savefig('max_and_min_temps.png')

        plt.figure()
        idx = random.randint(0, len(cities)-1)
        plt.plot(temps[idx].keys(), temps[idx].values())
        plt.title(f"{dates[idx]} in {cities[idx]}")
        plt.savefig('one day of weather.png')

        