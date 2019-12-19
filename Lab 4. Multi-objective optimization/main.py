import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from data import alter_matrix, weight_vector, vars, criteria
from utils import matrix_ration, matrix_normalization, manhattan_distance_2p


def replacing_criteria_with_constraints(alter_matrix, main_crit=4, max_main=True, 
                                    levels=[0.7, 0.8, 0.5], sings=[-1, -1, 1]):
    columns_to_norm = list(alter_matrix.columns)
    columns_to_norm.remove(main_crit)
    norm = matrix_ration(alter_matrix[columns_to_norm])
    norm = pd.concat([norm, alter_matrix[[4]]], axis=1)
    for i in range(len(columns_to_norm)):
        if sings[i] == -1:
            norm = norm[norm[columns_to_norm[i]] <= levels[i]]
        else:
            norm = norm[norm[columns_to_norm[i]] >= levels[i]]
    return norm[4].idxmax()


def pareto_optimality(alter_matrix, main_crit=[3, 4]):
    matr = alter_matrix[main_crit]
    matr = matr.sort_values(by=[main_crit[0]])
    xlist = matr[main_crit[0]]
    ylist = matr[main_crit[1]]
    utop = [matr[main_crit[0]].max(), matr[main_crit[1]].max()]
    dists = []
    m_distances = []
    for i in range(len(xlist)):
        dists.append([xlist[i], utop[0]])
        dists.append([ylist[i], utop[1]])
        dists.append("b--")
        d = manhattan_distance_2p([xlist[i], ylist[i]], utop)
        m_distances.append(d)
    plt.plot(xlist, ylist, 'bo', utop[0], utop[1], 'ro', *dists)
    plt.annotate("Т. утопии", xy=utop)
    for index, row in matr.iterrows():
        plt.annotate(index, xy=list(row))
    plt.grid(True)
    plt.show()
    matr["dist"] = pd.Series(m_distances, index=matr.index)
    return list(matr[matr["dist"] == matr["dist"].min()].index)


def weighting_and_combining_criteria(alter_matrix, weight_vector):
    norm = matrix_normalization(alter_matrix)
    gammas = pd.DataFrame(np.zeros((len(weight_vector), len(weight_vector))))
    for col in gammas:
        for i, _ in gammas[col].iteritems():

            if col == i:
                gammas[col][i] = 0
                continue 

            if abs(weight_vector[col] - weight_vector[i]) == 1:
                gammas[col][i] = 0.5
            elif weight_vector[col] > weight_vector[i]:
                gammas[col][i] = 1
            else: 
                gammas[col][i] = 0 
    gammas = gammas.sum()
    vec_norm = np.sqrt((gammas**2).sum())
    norm_gammas = gammas/vec_norm 
    norm_gammas = np.matrix(norm_gammas.to_numpy()).T
    result = norm.to_numpy() * norm_gammas
    return list(norm.index[np.where(result== np.amax(result))[0]])


def hierarchy_analysis(alter_matrix, vars, criteria):
    matr = []
    for key in vars.keys():
        check_consistency_relation(vars[key])
        matr.append(matrix_normalization(vars[key].sum(axis=1)))
    check_consistency_relation(criteria)
    matr = pd.concat(matr, axis=1).to_numpy()
    crit = matrix_normalization(criteria.sum(axis=1))
    crit = np.matrix(crit.to_numpy()).T
    result = matr * crit
    return list(alter_matrix.index[np.where(result== np.amax(result))[0]])


def check_consistency_relation(matr):
    value_alt = matr.product(axis=1)
    weights = (value_alt)**(1/4)
    weights = weights / weights.sum()
    l = weights * matr.sum()
    l = sum(l)
    idx_con = (l - 4) / 3
    print(idx_con / 0.9)


if __name__ == "__main__":
    print(alter_matrix)
    # print("Replacing:", replacing_criteria_with_constraints(alter_matrix))
    # print("Pareto:", pareto_optimality(alter_matrix))
    # print("Weighting: ", weighting_and_combining_criteria(alter_matrix, weight_vector))
    print("Hierarchy: ", hierarchy_analysis(alter_matrix, vars, criteria))
