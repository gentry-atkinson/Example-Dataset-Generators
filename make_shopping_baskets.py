# Author: Gentry Atkinson (gatkins0@stedwards.edu)
# Organization: St. Edwards Universtiy
# Date: 26 September, 2024

import random
import pandas as pd

NUM_STRONG_PAIRS = 5
NUM_WEAK_PAIRS = 5
NUM_ROWS = 50_000

WITH_NOISE = False

all_products = [
    "apples", "bananas", "strawberries", "carrots", "garlic", "lemons", "parsley",
    "potatoes", "tomatoes", "pasta", "rice", "bread", "tortillas", "chicken",
    "eggs", "beef", "ham", "butter", "milk", "yogurt", "sugar", "flour", "honey",
    "yeast", "cocoa", "corn", "bacon", "shrimp", "salsa", "jelly", "beans",
    "tuna", "vinegar", "soap", "sponges", "batteries", "detergent", "mayo", 
    "toothpaste", "coffee", "mustard", "paprika", "cinamon", "limes", "peaches",
    "celery", "onions", "feta", "cookies", "buns", "pita", "salmon", "bleach",
    "foil", "lotion", "mouthwash", "sunscreen", "diapers"
]

all_shoppers = random.sample(range(100_000, 999_999), 500)
all_stores = list(range(1, 51))

strong_pairs = [(a, b) for a, b in [random.sample(all_products, 2) for _ in range(NUM_STRONG_PAIRS)]]
weak_pairs = [(a, b) for a, b in [random.sample(all_products, 2) for _ in range(NUM_STRONG_PAIRS)]]
favorite_product = random.choice(all_products)

if __name__ == '__main__':
    shoppers = []
    stores = []
    baskets = []

    print("Strong Pairs: ", strong_pairs)
    print("Weak Pairs: ", weak_pairs)
    print(f"Number of possible products: {len(all_products)}")
    print(f"Favorite product: {favorite_product}")

    for _ in range(NUM_ROWS):
        shoppers.append(random.choice(all_shoppers))
        stores.append(random.choice(all_stores))
        basket_size = random.randint(5, 15)
        basket = set(random.sample(all_products, basket_size))
        # TREND- strong pairs appear together frequently
        for a, b in strong_pairs:
            if a in basket and random.randint(0,1)==1:
                basket.add(b)
            elif b in basket and random.randint(0,1)==1:
                basket.add(a) 

        # TREND- weak pairs appear less frequently but more than random
        for a, b in weak_pairs:
            if a in basket and random.randint(0,3)==3:
                basket.add(b)
            elif b in basket and random.randint(0,3)==3:
                basket.add(a)

        # TREND- favorite product
        if random.randint(0,2)==2:
            basket.add(favorite_product)

        # Stringify baskets
        basket = list(basket)
        random.shuffle(basket)
        basket = ', '.join(basket)
        
        baskets.append(basket)

    if WITH_NOISE:
        pass


    # Convert to DF and write to JSON
    table = pd.DataFrame.from_dict({
        "Store" : stores,
        "Shopper" : shoppers,
        "Basket" : baskets
    })

    print(table.head(10))
    table.to_json("Shopping Basket Database.json")
    table.to_excel("Shopping Basket Database.xlsx")