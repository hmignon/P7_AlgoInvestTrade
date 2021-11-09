from tqdm import tqdm

import csv
import time

start_time = time.time()

MAX_INVEST = 500


def main():
    shares_list = read_csv()
    best_combo = get_combo(shares_list)
    display_results(best_combo)


def read_csv():
    """Import shares data from .csv
    Filter out corrupted data
    @return: shares list
    """
    with open("data/dataset1_Python+P7.csv") as csvfile:
        shares_file = csv.reader(csvfile, delimiter=',')
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


def knapsack(shares_list):
    W = MAX_INVEST * 100
    n = len(shares_list)
    val = []
    wt = []

    for share in shares_list:
        val.append(share[2])
        wt.append(share[1])

    ks = [[0 for x in range(W + 1)] for x in range(n + 1)]

    for i in tqdm(range(n)):

        for w in range(W + 1):
            if i == 0 or w == 0:
                ks[i][w] = 0
            elif wt[i-1] <= w:
                ks[i][w] = max(
                    val[i-1] + ks[i-1][w-wt[i-1]],
                    ks[i-1][w]
                )
            else:
                ks[i][w] = ks[i-1][w]

    return W, n, ks


def get_combo(shares_list):
    W, n, ks = knapsack(shares_list)

    best_combo = []

    while W >= 0 and n >= 0:
        share = shares_list[n - 1]

        if ks[n][W] == ks[n-1][W - share[1]] + share[2]:
            best_combo.append(share)
            W -= share[1]

        n -= 1

    return best_combo


def display_results(best_combo):
    """Display best combination results"""
    print("\nMost profitable investment :\n")

    cost = []
    profit = []

    for item in best_combo:
        print(f"{item[0]} | {item[1] / 100} € | +{item[2]} €")
        cost.append(item[1] / 100)
        profit.append(item[2])

    print("\nTotal cost : ", sum(cost), "€")
    print("Profit: +", sum(profit), "€")
    print("\nTime elapsed : ", time.time() - start_time, "seconds")


if __name__ == "__main__":
    main()
