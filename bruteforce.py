from tqdm import tqdm

from itertools import combinations
import csv
import time

start_time = time.time()

MAX_INVEST = 500


def main():
    shares_list = read_csv()
    best_combo = set_combos(shares_list)
    display_results(best_combo)


def read_csv():
    """Import shares data from .csv
    @return: shares list
    """
    with open("data/shares.csv") as csvfile:
        shares_file = csv.reader(csvfile, delimiter=',')

        shares_list = []
        for row in shares_file:
            shares_list.append([row[0], float(row[1]), float(row[2])])

        return shares_list


def set_combos(shares_list):
    """Set all possible combinations of shares
    Check if under max possible investment
    Check profit
    @return: most profitable combination (list)
    """
    profit = 0
    best_combo = []

    for i in tqdm(range(len(shares_list))):
        combos = combinations(shares_list, i+1)

        for combo in combos:
            total_cost = calc_cost(combo)

            if total_cost <= MAX_INVEST:
                total_profit = calc_profit(combo)

                if total_profit > profit:
                    profit = total_profit
                    best_combo = combo

    return best_combo


def calc_cost(combo):
    """Sum of current share combo prices
    @return: total cost (float)
    """
    prices = []
    for el in combo:
        prices.append(el[1])

    return sum(prices)


def calc_profit(combo):
    """Sum of current share combo profit
    @return: total profit (float)
    """
    profits = []
    for el in combo:
        profits.append(el[1] * el[2] / 100)

    return sum(profits)


def display_results(best_combo):
    """Display best combination results"""
    print("\nMost profitable investment :\n")

    for item in best_combo:
        print(f"{item[0]} | {item[1]} € | +{item[2]} %")

    print("\nTotal cost : ", calc_cost(best_combo), "€")
    print("Profit : +", calc_profit(best_combo), "€")
    print("\nTime elapsed : ", time.time() - start_time, "seconds")


if __name__ == "__main__":
    main()
