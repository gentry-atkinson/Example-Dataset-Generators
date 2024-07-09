# Author: Gentry Atkinson (gatkins0@stedwards.edu)
# Organization: St. Edwards Universtiy
# Date: 9 July, 2024

import pandas as pd
import random

if __name__ == '__main__':
    name_list = []
    with open('Example-Dataset-Generators/raw_last_names.txt', 'r') as f:
        contents = f.readlines()
        for line in contents:
            name_list.append(line.split('\t')[0].strip())
    random.shuffle(name_list)
    new_name_list = []
    for i, name in enumerate(name_list):
            new_name_list.append(name[0] + name[1:].lower())
    print(f'Len of names is {len(name_list)}')
    with open('Example-Dataset-Generators/last_names.txt', 'w+') as f:
        f.write('\n'.join(new_name_list))

    print("Generating a dataset of 10,000 random students")
    table = pd.DataFrame()



        
