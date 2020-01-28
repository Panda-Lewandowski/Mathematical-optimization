from math import log
from random import choice, uniform
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import matplotlib.pyplot as plt


def fitness(x, y):
    return -log(1 + x ** 2 + y ** 2)

def np_fitness(x, y):
    return -np.log(1 + x ** 2 + y ** 2)

def calculate_fitness_for_generation(gen, f):
    fits = dict()
    for ind in gen:
        fits[f(*ind)] = ind
    return fits

def crossover(a, b):
    return (a[0], b[1]), (b[0], a[1])

def mutation(ind):
    eps = 0.15
    return (ind[0] + eps * uniform(-1, 1), ind[1] + eps * uniform(-1, 1))

def selection(gen_with_fits, n):
    val = sum(gen_with_fits.keys())
    probs = dict()
    for ind in gen_with_fits.keys():
        prob = ind / val
        probs[prob] = gen_with_fits[ind]
    new_gen_prob = list(probs.keys())
    new_gen_prob.sort()
    new_gen_prob = new_gen_prob[:n]
    new_gen = []
    for ind in new_gen_prob:
        new_gen.append(probs[ind])
    return new_gen


if __name__ == "__main__":
    N = 10
    X = np.arange(-2, 2, 0.25)
    Y = np.arange(-2, 2, 0.25)
    X, Y = np.meshgrid(X, Y)
    Z = np_fitness(X, Y)

    fig = plt.figure()
    ax = Axes3D(fig)

    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    generation = [(uniform(-2, 2), uniform(-2, 2)) for i in range(4)]
    population = []

    for i in range(N+1):
        population.append(generation)
        fits = calculate_fitness_for_generation(generation, fitness)
        print(f"{i}   Gen: {generation}  \nFits: {fits} \nMax: {max(fits.keys())} \nSum: {sum(fits.keys())/4} \n")
        sorted_fits = list(fits.keys())
        sorted_fits.sort(reverse=True)
        children1 = crossover(fits[sorted_fits[0]], fits[sorted_fits[1]])
        children2 = crossover(fits[sorted_fits[0]], fits[sorted_fits[2]])
        children = children1 + children2
        mutant = choice(children)
        children = [child for child in children if child != mutant]
        children.append(mutation(mutant))
        generation += children
        fits = calculate_fitness_for_generation(generation, fitness)
        generation = selection(fits, 4)
        # print(f"{i}   Gen: {generation}  \nFits: {fits} \nMax: {max(fits.keys())} \nSum: {sum(fits.keys())/4} \n")
        # print(generation)

    plt.figure()
    i = 0
    for gen in population:
        xs = [p[0] for p in gen]
        ys = [p[1] for p in gen]
        plt.plot(xs, ys, 'o', color=f"C{i}", label=f"{i}", alpha=0.5)
        i+=1

    plt.grid(True)
    plt.legend(loc='center left', title="N", bbox_to_anchor=(1, 0.5))
    plt.show()
