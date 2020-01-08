from math import sin, pi, modf, log, fabs
from matplotlib import pyplot as plt
from random import uniform
from prettytable import PrettyTable
import numpy as np


def source_signal(x):
    return sin(x) + 0.5


def gen_source_signal(xmin, xmax, f):
    K = 100
    xk = [xmin + k * (xmax - xmin) / K for k in range(0, K + 1)]
    return xk, list(map(f, xk))


def gen_noisy_signal(xmin, xmax, f):
    K = 100
    a = 0.25
    xk = [xmin + k * (xmax - xmin) / K for k in range(0, K + 1)]
    fk = list(map(f, xk))
    return xk, [f + uniform(-a, a) for f in fk]


def gen_weights(win_size):
    weights = np.zeros(win_size)
    M = (win_size - 1) // 2

    weights[M] = np.random.uniform(0, 1)
    middle_indexes = np.array([i for i in range(1, M)])

    for i in middle_indexes:
        weights[i] = np.random.uniform(0, 1 - sum([weights[j]
                                for j in range(i + 1, win_size - 1 - i) ])) * 0.5
        weights[win_size - 1 - i] = weights[i]

    weights[0] = (1 - sum([weights[j] for j in range(1, win_size - 1)])) * 0.5
    weights[win_size - 1] = weights[0] 
    
    return weights


def get_values_by_rolling_average(noisy_values, weights):
    win_size = len(weights)
    M = (win_size - 1) // 2

    result = noisy_values.copy()

    for i in range(M, len(noisy_values) - M):
        result[i] = sum([noisy_values[j] * weights[j - i + M]
                                            for j in range(i - M, i + M + 1)])
    return result


def get_noisiness(filtered_values):
    return sum([fabs(filtered_values[i] - filtered_values[i-1])
                                    for i in range(1, len(filtered_values))])


def get_difference(filtered_values, noisy_values):
    return sum([fabs(filtered_values[i] - noisy_values[i])
                    for i in range(len(filtered_values))]) / len(noisy_values)


def get_distance(noisiness, difference):
    return fabs(noisiness) + fabs(difference)


def stochastic_filtering(xmin, xmax, noisy_values, win_size):
    L = 10
    P = 0.95
    eps = 0.01
    lambdas = [l / L for l in range(0, L + 1)] 
    N = int(log(1 - P) / log(1 - eps / (xmax - xmin)))

    results = dict()
    opt_crit_nois = []
    opt_crit_diff = []
    table = PrettyTable()
    table.field_names = ['λ', '‎α ', '‎ω ', 'ẟ ', 'J', 'dist']
    
    for la in lambdas:
        experiment_results = dict()
        for n in range(N):
                alpha_weights = gen_weights(win_size)
                ffk = get_values_by_rolling_average(noisy_values, alpha_weights)
                noisiness = get_noisiness(ffk)
                difference = get_difference(ffk, noisy_values)

                integr_crit = la * noisiness - (1 - la) * difference
                experiment_results[integr_crit] = dict(
                                            weights=alpha_weights, 
                                            noisiness=noisiness,
                                            difference=difference
                                        )

        min_integr_crit = min(experiment_results.keys())
        min_exp_res = experiment_results[min_integr_crit]
        distance = get_distance(min_exp_res['noisiness'], min_exp_res['difference'])
        results[distance] = dict(
                        la=la, 
                        integr=min_integr_crit, 
                        noisiness=min_exp_res['noisiness'],
                        difference=min_exp_res['difference'],
                        alphas=min_exp_res['weights']
                    )
        table.add_row([la, min_exp_res['weights'], round(min_exp_res['noisiness'], 5), 
                        round(min_exp_res['difference'], 5), 
                        round(min_integr_crit, 5), round(distance, 5)])
        opt_crit_nois.append(min_exp_res['noisiness'])
        opt_crit_diff.append(min_exp_res['difference'])

    min_distance = min(results.keys())
    min_res = results[min_distance]

    print(table)
    print(f"Оптимальное значение: \nλ={min_res['la']} ω={min_res['noisiness']}")
    print(f"ẟ={min_res['difference']} J={min_res['integr']}")

    return get_values_by_rolling_average(noisy_values, min_res['alphas']), \
                [lambdas, opt_crit_nois, opt_crit_diff]


if __name__ == "__main__":
    xk, fk = gen_source_signal(0, pi, source_signal)

    nxk, nfk = gen_noisy_signal(0, pi, source_signal)

    ffk3, to_graph3 = stochastic_filtering(0, pi, nfk, 3)

    ffk5, to_graph5  = stochastic_filtering(0, pi, nfk, 5)

    plt.figure()
    plt.plot(xk, fk, label='f(x) = sin(x) + 0.5')
    plt.plot(nxk, nfk, label='noisy f(x)', linewidth=1.5, alpha=0.7)
    plt.plot(nxk, ffk3, label='filtered noisy f(x) by r=3', linewidth=1, alpha=0.7)
    plt.plot(nxk, ffk5, label='filtered noisy f(x) by r=5', linewidth=1, alpha=0.7)
    plt.legend(loc='lower center')
    plt.grid(True)

    plt.figure()
    for i in range(len(to_graph3[0])):
        plt.plot(to_graph3[1][i], to_graph3[2][i], 'o', 
                                        label=str(to_graph3[0][i]), alpha=0.7)
    plt.grid(True)
    plt.legend()

    plt.figure()
    for i in range(len(to_graph5[0])):
        plt.plot(to_graph5[1][i], to_graph5[2][i], 'o', 
                                        label=str(to_graph5[0][i]), alpha=0.7)
    plt.grid(True)
    plt.legend()
    plt.show()