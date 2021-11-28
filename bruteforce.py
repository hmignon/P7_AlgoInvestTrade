from tqdm import tqdm

from itertools import combinations
import csv
import time
import sys


start_time = time.time()

# Check for custom cash investment (default = 500)
try:
    MAX_INVEST = float(sys.argv[1])
except IndexError:
    MAX_INVEST = 500


def main():
    shares_list = read_csv()

    print(f"\nProcessing {len(shares_list)} shares for {MAX_INVEST}€ :")

    best_combo = set_combos(shares_list)
    display_results(best_combo)


def read_csv():
    """Import shares data from test_shares.csv

    @return: shares data (list)
    """
    with open("data/test_shares.csv") as csvfile:
        shares_file = csv.reader(csvfile, delimiter=',')

        shares_list = []
        for row in shares_file:
            shares_list.append(
                (row[0], float(row[1]), float(row[2]))
            )

        return shares_list


def set_combos(shares_list):
    """Set all possible combinations of shares
    Check if under max possible investment
    Check and get highest profit

    @param shares_list: list of all imported shares data
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

    @param combo: list of current shares combo
    @return: total cost (float)
    """
    prices = []
    for el in combo:
        prices.append(el[1])

    return sum(prices)


def calc_profit(combo):
    """Sum of current share combo profit

    @param combo: list of current shares combo
    @return: total profit (float)
    """
    profits = []
    for el in combo:
        profits.append(el[1] * el[2] / 100)

    return sum(profits)


def display_results(best_combo):
    """Display best combination results

    @param best_combo: most profitable shares combination (list)
    """
    print(f"\nMost profitable investment ({len(best_combo)} shares) :\n")

    for item in best_combo:
        print(f"{item[0]} | {item[1]} € | +{item[2]} %")

    print("\nTotal cost : ", calc_cost(best_combo), "€")
    print("Profit after 2 years : +", calc_profit(best_combo), "€")
    print("\nTime elapsed : ", time.time() - start_time, "seconds")


if __name__ == "__main__":
    main()
