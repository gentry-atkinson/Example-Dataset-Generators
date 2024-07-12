# Author: Gentry Atkinson (gatkins0@stedwards.edu)
# Organization: St. Edwards Universtiy
# Date: 11 July, 2024

import random
import pandas as pd

START_YEAR = 2015
FINAL_YEAR = 2023
WITH_NOISE = True
NUM_SELLERS = 1000
NUM_BUYERS = 10000
LOSS_PER_YEAR = 0.05

MANFS_W_SCALE = {'CompuCraft' : 1.0, 'R&L' : 0.8, 'ValuServe' : 0.6, 
                'TSN' : 1.2, 'Soft Systems' : 1.4, 'Cherry' : 2.0}

PROD_CATS_W_MEAN_MSRP = {
    'Laptop': 1200, 'Monitor' : 400, 'Desktop' : 1000,
    'Mouse' : 20, 'Projector' : 150, 'VR Headset' : 300
}

PROD_NAME_1 = ['Full', 'Easy', 'Octo', 'Micro', 'Red', 'Soft', 'Wild', 
               'Busy', 'Clever', 'Dark', 'Clear', 'Team']

PROD_NAME_2 = ['Slide', 'Sail', 'Pro', 'Way', 'State', 'Life', 'Case', 'Prod',
               'System', 'Work', 'Day', 'Area', 'Cash', 'Book', 'Word', 'Job',
               'Eye', 'House', 'Power', 'Line', 'City', 'Back', 'Level', 'Art']

MONTHS = {'Jan':31, 'Feb':28, 'Mar':31, 
          'Apr':30, 'May':31, 'Jun':30, 
          'Jul':31, 'Aug':31, 'Sep':30,
          'Oct':31, 'Nov':30, 'Dec':31}

# TREND- some resalers have lower avg sale prices
RESALERS_W_SCALE = {
    'Ebay' : 1.0, 'FB Marketplace' : 0.95, 'Classified Ad' : 1.1, 'Pawn/Consignment Shop' : 0.7,
    'Craigslist' : 0.9, 'OfferUp' : 1.05, 'NextDoor' : 1.08, 'Swappa' : 1.02
}

CONDS_W_SCALE = {
    'Poor' : 0.6, 'Fair' : 0.8, 'Normal' : 0.9, 'Good' : 1.0, 'Great' : 1.05
}

class Product:
    def __init__(self, cat: str, msrp : int, name : str) -> None:
        self.category = cat
        self.msrp = msrp
        self.name = name
        self.product_code = str(random.randint(1000, 9999)) + '-' + str(random.randint(100000, 999999))

    def __str__(self):
        return self.name + ' $' + str(self.msrp)

def make_product_list(man: str, n: int) -> list[Product]:
    l = []
    for _ in range(n):
        cat = random.choice(list(PROD_CATS_W_MEAN_MSRP.keys()))
        msrp = int(PROD_CATS_W_MEAN_MSRP[cat] * MANFS_W_SCALE[man]) + random.randint(0, PROD_CATS_W_MEAN_MSRP[cat]//10)
        name = random.choice(PROD_NAME_1) + ' ' + random.choice(PROD_NAME_2)
        if random.randint(0, 1) == 0:
            name += random.choice([' ', '-', ': '])
            name += random.choice(['M', 'N', 'X', 'Alpha', 'Q-', 'P'])
            name += str(random.randint(10, 999))
        l.append(Product(cat, msrp, name))
    return l

SELLER_IDS_W_SCALE = {i : random.gauss(1.1, 0.1) for i in range(NUM_SELLERS)}
BUYER_IDS_W_SCALE = {i : random.gauss(0.9, 0.1) for i in range(NUM_BUYERS)}

if __name__ == '__main__':
    year = START_YEAR
    mon_idx = 0
    day = 1

    prod_names = []
    prod_codes = []
    cats = []
    year_prod = []
    msrps = []
    mans = []
    sale_prices = []
    s_ids = []
    b_ids = []
    conds = []
    dates = []
    resalers = []

    # Make a list of products for every manufacturer
    prod_lists = {
        man : make_product_list(man, random.randint(10, 30)) for man in list(MANFS_W_SCALE.keys())
    }
    print(f"Number of manufacturers: {len(prod_lists)}")
    print(f"Total number of products: {sum([len(l) for l in prod_lists.values()])}")

    # TREND- some years have higher prices than others
    year_scale = random.gauss(1, 0.05)

    # TREND- prices increase over time
    inflation = 1.0

    while year <= FINAL_YEAR:
        month = list(MONTHS.keys())[mon_idx]
        for _ in range(random.randint(5, 20)):
            # Choose all factors
            man = random.choice(list(MANFS_W_SCALE.keys()))
            prod = random.choice(prod_lists[man])
            s_id = random.choice(list(SELLER_IDS_W_SCALE.keys()))
            b_id = random.choice(list(BUYER_IDS_W_SCALE.keys()))
            cond = random.choice(list(CONDS_W_SCALE.keys()))
            resaler = random.choice(list(RESALERS_W_SCALE.keys()))
            age = random.randint(0, 10)

            #Calculate sale price
            price = random.gauss(prod.msrp, prod.msrp/20)
            price *= SELLER_IDS_W_SCALE[s_id]
            price *= BUYER_IDS_W_SCALE[b_id]
            price *= CONDS_W_SCALE[cond]
            price *= RESALERS_W_SCALE[resaler]
            price *= year_scale
            price *= inflation
            price *= (1-LOSS_PER_YEAR)**age

            #Add values to column lists
            prod_names.append(prod.name)
            prod_codes.append(prod.product_code)
            cats.append(prod.category)
            year_prod.append(year - age)
            msrps.append(f"${prod.msrp * inflation:.0f}")
            mans.append(man)
            sale_prices.append(round(price, 2))
            s_ids.append(s_id)
            b_ids.append(b_id)
            conds.append(cond)
            dates.append(str(day) + ' ' + month + ', ' + str(year))
            resalers.append(resaler)

        #Increment day
        day += 1
        if day > MONTHS[month]:
            day = 1
            mon_idx += 1
        if mon_idx == 12:
            mon_idx = 0
            year += 1
            year_scale = random.gauss(1, 0.05)
            inflation = (1.0 + (LOSS_PER_YEAR/2)) ** (year - START_YEAR)

    tids = [i for i in range(1, len(prod_names)+1)]
    print(f"{len(prod_names)} transactions generated")

    #Make DataFrame with columns and write to file
    table = pd.DataFrame.from_dict({
        'Seller ID' : s_ids,
        'Buyer ID' : b_ids,
        'Product Name' : prod_names,
        'Product Category' : cats,
        'Manufacturer' : mans,
        'Product MSRP' : msrps,
        'Product Date of Manufacture' : year_prod,
        'Condition of Product' : conds,
        'Transaction Date' : dates,
        'Transaction Platform' : resalers,
        'Product Code' : prod_codes,
        'Sale Price' : sale_prices
    })
    print(table.head(10))
    print(f"Total number of rows: {len(table)}")

    table.to_json("Electronics_sales.json")
    table.to_excel("Electronics_sales.xlsx")