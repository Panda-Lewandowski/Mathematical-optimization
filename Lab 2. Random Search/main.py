from math import exp, sin, log, ceil
from random import uniform
from numpy import arange
from prettytable import PrettyTable
from matplotlib import pyplot as plt
from matplotlib import mlab


def rnds(f, a, b, eps=1e-5):
    table = PrettyTable()
    table.add_column("q\\P", list(map(lambda x: round(x, 3), 
                            arange(0.005, 0.105, 0.005))))

    for p in arange(0.9, 1, 0.01):
        column = []
        for q in arange(0.005, 0.105, 0.005):
            N = ceil(log(1 - p) / log(1 - q))
            xs = [uniform(a, b) for i in range(N)]
            ys = list(map(f, xs))
            cur_min = round(min(ys), 5)
            column.append(cur_min)
        table.add_column(str(round(p, 2)), column)

    print(table)


if __name__ == "__main__":
    f1 = lambda x: x ** 2 * exp(sin(x))
    f2 = lambda x: f1(x) * sin(5*x)

    xmin = 16.0
    xmax = 20.0

    dx = 0.01

    xlist = arange(xmin, xmax, dx)
    ylist1 = [f1(x) for x in xlist]
    ylist2 = [f2(x) for x in xlist]

    fig, axs = plt.subplots(2)
    axs[0].plot(xlist, ylist1)
    axs[0].grid(True)
    axs[1].plot(xlist, ylist2)
    axs[1].grid(True)
    plt.show()

    rnds(f1, 16, 20)
    rnds(f2, 16, 20)