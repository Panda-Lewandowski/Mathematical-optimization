import random
import math
import matplotlib.pyplot as plt
from prettytable import PrettyTable

def f(x):
    # return x ** 2 * math.exp(math.sin(x))
    return x ** 2 * math.exp(math.sin(x)) * math.sin(5*x)

def P (d, T):
    return math.exp((-d)/T)

if __name__ == '__main__':

    curr_state = 16
    T1, T2 = 10000, 0.1
    coolingRate = 0.95
    curr_eval = f(curr_state)
    min_eval = curr_eval

    table = PrettyTable()
    table.field_names = ["#", "T", "x", "f(x)", "P", "+/-"]
    i = 0

    while T1 > T2:
        new_state = random.uniform(16, 20)
        Dif = f(new_state) - f(curr_state)
        dis = "-"
        if Dif < 0:
            curr_state = new_state
            curr_eval = f(curr_state)
            min_eval = min(min_eval, curr_eval)
            table.add_row([i, round(T1, 5), round(curr_state, 5), round(curr_eval, 5), "-", "+"])
        else:
            R = random.random()
            if P(Dif, T1) >= R:
                curr_state = new_state
                curr_eval = f(curr_state)
                min_eval = min(min_eval, curr_eval)
                dis = "+"
            table.add_row([i, round(T1, 5), round(curr_state, 5), round(curr_eval, 5), round(P(Dif, T1), 5), dis])
        i += 1
        T1 = T1 * coolingRate

    print(table)
    print("Minimum: ", min_eval)


