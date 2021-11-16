from tqdm import tqdm

import csv
import time
import sys

start_time = time.time()

# Check for custom cash investment (default = 500)
try:
    MAX_INVEST = float(sys.argv[2])
except IndexError:
    MAX_INVEST = 500


def main():
    """Check for filename input"""
    try:
        filename = "data/" + sys.argv[1] + ".csv"
    except IndexError:
        print("\nNo filename found. Please try again.\n")
        time.sleep(1)
        sys.exit()

    shares_list = read_csv(filename)

    print(f"\nProcessing '{sys.argv[1]}' ({len(shares_list)} valid shares) for {MAX_INVEST}€ :")

    best_combo = get_combo(shares_list)
    display_results(best_combo)


def read_csv(filename):
    """Import shares data from .csv
    Filter out corrupted data

    @return: shares data (list)
    """
    try:
        with open(filename) as csvfile:
            shares_file = csv.reader(csvfile, delimiter=',')

            if filename != "data/test_shares.csv":
                next(csvfile)

            shares_list = []
            for row in shares_file:
                if float(row[1]) <= 0 or float(row[2]) <= 0:
                    pass
                else:
                    share = [
                        row[0],
                        int(float(row[1])*100),
                        float(float(row[1]) * float(row[2]) / 100)
                    ]
                    shares_list.append(share)

            return shares_list

    except FileNotFoundError:
        print(f"\nFile '{filename}' does not exist. Please try again.\n")
        time.sleep(1)
        sys.exit()


def get_combo(shares_list):
    """Get best shares combination.

    @param shares_list: list of all imported shares data
    @return: most profitable combination (list)
    """
    max_inv = int(MAX_INVEST * 100)
    shares = len(shares_list)
    profit = []
    cost = []

    for share in shares_list:
        profit.append(share[2])
        cost.append(share[1])

    ks = knapsack(max_inv, profit, cost, shares)

    best_combo = []

    while max_inv >= 0 and shares >= 0:

        if ks[shares][max_inv] == ks[shares - 1][max_inv - cost[shares - 1]] + profit[shares - 1]:
            best_combo.append(shares_list[shares - 1])
            max_inv -= cost[shares - 1]

        shares -= 1

    return best_combo


def knapsack(max_inv, profit, cost, shares):
    """Initialize the matrix (ks) for 0-1 knapsack problem

     @param max_inv: maximum cash investment * 100 (int)
     @param profit: list of all shares profits (float)
     @param cost: list of all shares costs (float)
     @param shares: total number of shares (int)
     
     @return: knapsack matrix (ks)
    """
    ks = [[0 for x in range(max_inv + 1)] for x in range(shares + 1)]

    for i in tqdm(range(shares + 1)):

        for inv in range(max_inv + 1):
            if i == 0 or inv == 0:
                ks[i][inv] = 0
            elif cost[i-1] <= inv:
                ks[i][inv] = max(
                    profit[i-1] + ks[i-1][inv - cost[i-1]],
                    ks[i-1][inv]
                )
            else:
                ks[i][inv] = ks[i - 1][inv]

    return ks


def display_results(best_combo):
    """Display best combination results
    @param best_combo: most profitable shares combination (list)
    """
    print(f"\nMost profitable investment ({len(best_combo)} shares) :\n")

    cost = []
    profit = []

    for item in best_combo:
        print(f"{item[0]} | {item[1] / 100} € | +{item[2]} €")
        cost.append(item[1] / 100)
        profit.append(item[2])

    print("\nTotal cost : ", sum(cost), "€")
    print("Profit after 2 years : +", sum(profit), "€")
    print("\nTime elapsed : ", time.time() - start_time, "seconds\n")


if __name__ == "__main__":
    main()
