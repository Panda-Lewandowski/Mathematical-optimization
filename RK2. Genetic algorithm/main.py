from math import log
from random import uniform, choice

def fitness(x, y):
    return -log(1 + x ** 2 + y ** 2)

def calculate_fitness_for_generation(gen, f):
    fits = dict()
    for ind in gen:
        fits[f(*ind)] = ind
    return fits

def crossover(a, b):
    return (a[0], b[1]), (b[0], a[1])

def mutation(ind):
    eps = 0.1
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
    N = 20
    generation = [(uniform(-2, 2), uniform(-2, 2)) for i in range(4)]

    for i in range(N):
        fits = calculate_fitness_for_generation(generation, fitness)
        
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
        print(i, sum(fits.keys())/4, max(fits.keys()))
        generation = selection(fits, 4)
        # print(generation)
        