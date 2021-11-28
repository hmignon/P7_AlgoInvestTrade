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

    display_results(knapsack(shares_list))


def read_csv(filename):
    """Import shares data from csv file
    Filter out corrupted data

    @return: shares data (list)
    """
    try:
        with open(filename) as csvfile:
            shares_file = csv.reader(csvfile, delimiter=',')

            if filename != "data/test_shares.csv":
                next(csvfile)       # skip first row in both datasets

            shares_list = []

            for row in shares_file:
                if float(row[1]) <= 0 or float(row[2]) <= 0:
                    pass
                else:
                    share = (
                        row[0],
                        int(float(row[1])*100),
                        float(float(row[1]) * float(row[2]) / 100)
                    )
                    shares_list.append(share)

            return shares_list

    except FileNotFoundError:
        print(f"\nFile '{filename}' does not exist. Please try again.\n")
        time.sleep(1)
        sys.exit()


def knapsack(shares_list):
    """Initialize the matrix (ks) for 0-1 knapsack problem
     Get best shares combination

     @param shares_list: shares data (list)
     @return: best possible combination (list)
    """
    max_inv = int(MAX_INVEST * 100)     # capacity
    shares_total = len(shares_list)
    cost = []       # weights
    profit = []     # values

    for share in shares_list:
        cost.append(share[1])
        profit.append(share[2])

    # Find optimal profit
    ks = [[0 for x in range(max_inv + 1)] for x in range(shares_total + 1)]

    for i in tqdm(range(1, shares_total + 1)):

        for w in range(1, max_inv + 1):
            if cost[i-1] <= w:
                ks[i][w] = max(profit[i-1] + ks[i-1][w-cost[i-1]], ks[i-1][w])
            else:
                ks[i][w] = ks[i-1][w]

    # Retrieve combination of shares from optimal profit
    best_combo = []

    while max_inv >= 0 and shares_total >= 0:

        if ks[shares_total][max_inv] == \
                ks[shares_total-1][max_inv - cost[shares_total-1]] + profit[shares_total-1]:

            best_combo.append(shares_list[shares_total-1])
            max_inv -= cost[shares_total-1]

        shares_total -= 1

    return best_combo


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
