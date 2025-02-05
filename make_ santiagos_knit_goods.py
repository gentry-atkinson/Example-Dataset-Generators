import random
import pandas as pd

NOISE = True

MONTHS = {1:31, 2:28, 3:31, 
          4:30, 5:31, 6:30, 
          7:31, 8:31, 9:30,
          10:31, 11:30, 12:31}

product_prices = {
    "Fuzzy Hat" : 16.00,
    "Striped Scarf" : 22.00,
    "Fringed Scarf" : 23.00,
    "Sweater Vest" : 40.00,
    "Sweater with Pockets" : 65.00
}

product_weights_by_year = {
    2020 : [0.7, 0.1, 0.1, 0.05, 0.05],
    2021 : [0.6, 0.2, 0.1, 0.05, 0.05],
    2022 : [0.5, 0.2, 0.2, 0.05, 0.05],
    2023 : [0.4, 0.2, 0.2, 0.15, 0.05],
    2024 : [0.2, 0.2, 0.2, 0.25, 0.15]
}

product_base_costs = {
    "Fuzzy Hat" : 4.08,
    "Striped Scarf" : 5.51,
    "Fringed Scarf" : 5.53,
    "Sweater Vest" : 12.19,
    "Sweater with Pockets" : 18.09
}

all_colors = ["Red", "Blue", "Green", "Purple"]
color_weights = {
    "Fuzzy Hat" : [0.4, 0.3, 0.2, 0.1],
    "Striped Scarf" : [0.6, 0.1, 0.1, 0.2],
    "Fringed Scarf" : [0.55, 0.1, 0.15, 0.2],
    "Sweater Vest" : [0.1, 0.4, 0.4, 0.1],
    "Sweater with Pockets" : [0.1, 0.3, 0.1, 0.5]
}

def inc_day(day, month, year) -> tuple:
    day += 1
    if day > MONTHS[month]:
        day = 1
        month += 1
    if month > 12:
        month = 1
        year += 1
    return day, month, year

if __name__ == '__main__':
    transac_ids = []
    days = []
    months = []
    years = []
    products = []
    colors = []
    sold_for = []
    costs = []

    day = 1
    month = 1
    year = 2020

    while year < 2025:
        for _ in range(random.randint(0, 1+(year-2020))):
            # Select Product
            product = random.choices(
                list(product_prices.keys()),
                weights=product_weights_by_year[year],
                k=1
            )[0]

            # Select Color
            color = random.choices(
                all_colors,
                weights = color_weights[product],
                k=1
            )[0]

            # Compute cost of product
            cost = product_base_costs[product] * (1.05**(year-2020))

            days.append(day)
            months.append(month)
            years.append(str(year))
            transac_ids.append(str(random.randint(100000000, 999999999)))
            products.append(product)
            colors.append(color)

            # NOISE- 1% of sale prices recorded as 0
            if NOISE and random.randint(1,100) == 1:
                sold_for.append("$ 0.00")
            else:
                sold_for.append(f"${product_prices[product] : .2f}")
            costs.append(f"${cost : .2f}")

        day, month, year = inc_day(day, month, year)

    # Build DataFrame
    table = pd.DataFrame.from_dict({
        "Transaction ID": transac_ids,
        "Day": days,
        "Month": months,
        "Year": years,
        "Product Name": products,
        "Product Color": colors,
        "Sold For": sold_for,
        "Cost to Make": costs,
    })

    # NOISE- Add a duplicate row
    if NOISE:
        row_to_dup = random.randint(500, len(table)-500)
        table.loc[row_to_dup+1] = table.loc[row_to_dup]
        print(f"Duped row: {row_to_dup}")

    print(table.head())
    table.to_json("Santiagos Knit Goods.json", index=False)
    table.to_excel("Santiagos Knit Goods.xlsx", index=False)

