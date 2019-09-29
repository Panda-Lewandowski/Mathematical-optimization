from math import exp, sin, sqrt, ceil, log
from prettytable import PrettyTable


inv_phi = (sqrt(5) - 1) / 2 # 1/phi                                                                                                                     
inv_phi2 = (3 - sqrt(5)) / 2 # 1/phi^2 


def gss(f, a, b, eps=1e-5):
    a, b = min(a, b), max(a, b)
    h = b - a
    if h <= eps: return (a,b)
                                                                                                                  
    n = int(ceil(log(eps / h) / log(inv_phi))) + 1

    c = a + inv_phi2 * h
    d = a + inv_phi * h
    yc = f(c)
    yd = f(d)
    
    table = PrettyTable()
    column_names = ["Начало интервала", "Конец интервала", 
                    "Точность поиска", "f(ak)", "f(bk)"]
    c_lst = [round(c, 5)]
    d_lst = [round(d, 5)]
    len_lst = [round(h, 5)]
    yc_lst = [round(yc, 5)]
    yd_lst = [round(yd, 5)]
    
    for _ in range(n - 1):
        if yc < yd:
            b, d, yd = d, c, yc
            h = inv_phi * h
            c = a + inv_phi2 * h
            yc = f(c)
        else:
            a, c, yc = c, d, yd
            h = inv_phi * h
            d = a + inv_phi * h
            yd = f(d)

        c_lst.append(round(c, 5))
        d_lst.append(round(d, 5))
        len_lst.append(round(h, 5))
        yc_lst.append(round(yc, 5))
        yd_lst.append(round(yd, 5))

    table.add_column(column_names[0], c_lst)
    table.add_column(column_names[1], d_lst)
    table.add_column(column_names[2], len_lst)
    table.add_column(column_names[3], yc_lst)
    table.add_column(column_names[4], yd_lst) 

    print(table)

    if yc < yd:
        return (a, d), yc
    else:
        return (c, b), yd


def ops(f, a, b, eps=1e-5):
    a, b = min(a, b), max(a, b)

    N = 1
    x = (b - a) / (N + 1) + a
    y = f(x)
    delta = (b - a) / (N + 1)
    record_y = y

    N_lst = [N]
    x_lst = [x]
    y_lst = [y]


    table = PrettyTable()
    column_names = ["Количество точек (N)", "Значение x в минимуме", "Минимум"]

    while delta > eps:
        N += 1
        x = [k * (b - a) / (N + 1) + a for k in range(1, N + 1)]
        y = list(map(f, x))

        N_lst.append(N)
        y_lst.append(round(min(y), 5))
        x_lst.append(round(x[y.index(min(y))], 5))

        record_y = min(record_y, min(y))
        delta = (b - a) / (N + 1)
        # print(N, record_y, delta)

    table.add_column(column_names[0], N_lst)
    table.add_column(column_names[1], x_lst)
    table.add_column(column_names[2], y_lst)
    print(table)
    print("Рекордный минимум: ", record_y)

    return record_y


if __name__ == "__main__":
    f = lambda x: x ** 2 * exp(sin(x)) 
    gss(f, 16, 20, eps=0.1)
    ops(f, 16, 20, eps=0.1)