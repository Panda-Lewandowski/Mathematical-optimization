def matrix_ration(matrix):
    return (matrix - matrix.min()) / (matrix.max() - matrix.min())


def matrix_normalization(matrix):
    return matrix / matrix.sum()


def manhattan_distance_2p(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])