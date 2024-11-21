# Author: Gentry Atkinson (gatkins0@stedwards.edu)
# Organization: St. Edwards Universtiy
# Date: 21 November, 2024

import random
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

NUM_SAMPLES = 1000

if __name__ == '__main__':
    x_values = []
    y_values = []
    labels = []

    for _ in range(NUM_SAMPLES):
        label = random.randint(1, 3)
        labels.append(label)

        if label == 1:
            x_values.append(random.gauss(0.35, 0.1))
            y_values.append(random.gauss(0.5, 0.18))

        elif label == 2:
            x_values.append(random.gauss(0.7, 0.08))
            y_values.append(random.gauss(0.3, 0.1))

        elif label == 3:
            x_values.append(random.gauss(0.75, 0.07))
            y_values.append(random.gauss(0.8, 0.1))
        else:
            print("Unexpected label.")

    

    table = pd.DataFrame.from_dict({
        "Feature 1" : x_values,
        "Feature 2" : y_values,
        "Target" : labels
    })
    print(table.head(3))
    print(f"Total number of rows: {len(table)}")

    # sns.scatterplot(data=table, x='Feature 1', y='Feature 2', hue='Target')
    # plt.show()

    table.to_json("Simple Three Class.json")
    table.to_excel("Simple Three Class.xlsx")
