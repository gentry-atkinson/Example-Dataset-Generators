# Author: Gentry Atkinson (gatkins0@stedwards.edu)
# Organization: St. Edwards Universtiy
# Date: 17 July, 2024

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import random

STEPS_PER_DAY = 50
NUM_SYMBOLS = 15
START_YEAR = 2014
FINAL_YEAR = 2023
UPPER_BOUND = 10000
LOWER_BOUND = 2

TRENDS = ['up', 'down', 'flat']

INDUSTRIES_W_MEAN_START = {
    "Technology" : random.randint(50, 250),
    "Defense" : random.randint(50, 250),
    "Consumer Electronics" : random.randint(50, 250),
    "Automotive" : random.randint(50, 250)
}

SYMBOLS_W_IND= {
    ''.join(random.choices(population='A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split(), k=3)) : 
    random.choice(list(INDUSTRIES_W_MEAN_START.keys()))
    for _ in range(NUM_SYMBOLS)
}

MONTHS = {1:31, 2:28, 3:31, 
          4:30, 5:31, 6:30, 
          7:31, 8:31, 9:30,
          10:31, 11:30, 12:31}

def rand_walk(start: float, trend: str) -> np.ndarray:
    walk = np.zeros(STEPS_PER_DAY)
    walk[0] = start
    for i in range(1, len(walk)):
        if trend == 'up':
            walk[i] = walk[i-1] + random.gauss(start/1000, start/1000)
        elif trend == 'down':
            walk[i] = walk[i-1] + random.gauss(-1 * start/1000, start/1000)
        elif trend == 'flat':
            walk[i] = walk[i-1] + random.gauss(0, start/1000)
        else:
            assert False, "Bad trend in rand_walk"
    return walk


if __name__ == '__main__':
    prices_and_trends = {
        sym : (
            random.gauss(INDUSTRIES_W_MEAN_START[ind], 10),
            random.choice(TRENDS)
        )
        for (sym, ind) in SYMBOLS_W_IND.items()
    }
    year = START_YEAR
    month_idx = 1
    day = 1
    years = []
    months = []
    days = []
    symbs = []
    is_tech = []
    is_def = []
    is_ce = []
    is_auto = []
    opens = []
    closes = []
    highs = []
    lows = []
    means = []
    for year in range(START_YEAR, FINAL_YEAR+1):
        print(f"Year: {year}")
        for month in range(1, 13):
            for day in range(1, MONTHS[month]+1):
                for sym in prices_and_trends:
                    start_price, trend = prices_and_trends[sym]
                    if start_price > UPPER_BOUND:
                        trend = 'down'
                    elif start_price < LOWER_BOUND:
                        trend = 'up'
                    elif random.randint(1, 10) == 1:
                        trend = random.choice(TRENDS) 
                    walk = rand_walk(start_price, trend)
                    years.append(year)
                    months.append(month)
                    days.append(day)
                    symbs.append(sym)
                    is_tech.append(1 if SYMBOLS_W_IND[sym]=='Technology' else 0)
                    is_def.append(1 if SYMBOLS_W_IND[sym]=='Defense' else 0)
                    is_ce.append(1 if SYMBOLS_W_IND[sym]=='Consumer Electronics' else 0)
                    is_auto.append(1 if SYMBOLS_W_IND[sym]=='Automotive' else 0)
                    opens.append(round(walk[0], 2))
                    closes.append(round(walk[-1], 2))
                    highs.append(round(np.max(walk), 2))
                    lows.append(round(np.min(walk), 2))
                    means.append(round(np.mean(walk), 2))
                    prices_and_trends[sym] = (walk[-1], trend)
    print(f"{len(symbs)} rows generated")
    table = pd.DataFrame.from_dict({
        'Year' : years,
        'Month' : months,
        'Day' : days,
        'Stock Symbol' : symbs,
        'Is Technology' : is_tech,
        'Is Defense' : is_def,
        'Is Consumer Electronics' : is_ce,
        'Is Automotive' : is_auto,
        'Stock Open Price' : opens,
        'Stock Close Price' : closes,
        'Daily Mean Price' : means,
        'Daily High Price' : highs,
        'Daily Low Price' : lows
    })
    print(table.tail(10))
    print(f"Total number of rows: {len(table)}")

    table.to_json("Financial_market.json")
    table.to_excel("Financial_market.xlsx")

    
    fig, axes = plt.subplots(nrows=NUM_SYMBOLS, ncols=1)
    for i, ax in enumerate(axes):
        sym = list(prices_and_trends.keys())[i]
        print(f"Checking symbol {sym}")
        #titanic[titanic["Pclass"].isin([2, 3])]
        rows = table[table['Stock Symbol'].isin([sym])]
        ax.plot(range(rows.shape[0]), rows['Daily Mean Price'])
    plt.show()
