import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sympy import solve, Eq, symbols


# starting parameters
def define_parameters(n_=3, s0=0.1, s1=0.4, s2=0.65, q0=0.2, q1=0.2, q2=0, q3=0,
                      p0=0.5, p1=0.3, p2=0.3, p3=0.9, r0=0.2, r1=0.1, r2=0.05, r3=0.1,
                      Q00=10, Q01=20, Q02=50, Q03=100, t_=0):
    n = n_  # number of starting generations
    s = [s0, s1, s2]
    q = [q0, q1, q2, q3]
    p = [p0, p1, p2, p3]
    r = [r0, r1, r2, r3]
    Q = [Q00, Q01, Q02, Q03]
    t = t_
    return n, s, q, p, r, Q, t


def new_clients(Q, *args):
    srednia = sum(Q) / len(Q)
    srednia = srednia / args[0]
    variance = args[1]
    x, y = symbols('x y')
    eq1 = Eq(srednia - x * y, 0)
    eq2 = Eq(variance - x * y * y, 0)
    sol = solve((eq1, eq2), (x, y))[0]
    return np.random.gamma(sol[0], sol[1])


def define_starting_df(n, Q):
    names = ['Q' + str(i) for i in range(n + 1)]
    df = pd.DataFrame(0, index=np.arange(1), columns=names)
    for j in range(n + 1):
        df.iloc[0, j] = Q[j]
    return df


def next_year(df, df2, n, t, s, p, k, k_):
    row = [0] * (n + 1)
    t = t + 1
    for j in range(n + 1):
        if j != n and j != n - 1:
            row[j] = round(s[j] * df.iloc[t - 1][-(n - j + 1)])
        elif j == n - 1:
            row[j] = round(s[j] * df.iloc[t - 1][-(n - j + 1)])
            for i in range(n + 1):
                row[j] += round(q[i] * df.iloc[t - 1][-n + i - 1])
            row[j] += round(k_)
        elif j == n:
            for i in range(n + 1):
                row[j] += round(p[i] * df.iloc[t - 1][-n + i - 1])
            row[j] += round(k)
    size = len(df.columns)
    no_zeros = size - (n + 1)
    list_zeros = [0] * no_zeros
    row = list_zeros + row
    df.loc[t] = row

    new_users_1 = 0
    for l in range(n):
        new_users_1 += round(p[l] * df.iloc[t - 1][-n + l - 1])
    new_users_1 += round(k)
    new_users_2 = 0
    for l in range(n):
        new_users_2 += round(q[l] * df.iloc[t - 1][-n + l - 1])
    new_users_2 += round(k_)
    last_row = df2.loc[t - 1]
    last_row[-1] += new_users_1
    if len(last_row) > 1:
        last_row[-2] += new_users_2
    df2.loc[t] = last_row
    return df, df2, t


def new_generation(df, df2):
    last_name = df.columns[-1]
    number_of_new_gen = str(int(last_name[1:]) + 1)
    new_name = 'Q' + number_of_new_gen
    df[new_name] = 0
    df2[new_name] = 0
    return df, df2


def create_number_of_users_df(n, Q):
    names = ['Q' + str(n)]
    df = pd.DataFrame(0, index=np.arange(1), columns=names)
    df.iloc[0, 0] = Q[n]
    return df


def plot_df(df):
    df.plot.line(title='Liczba posiadaczy generacji Qi w czasie')


if __name__ == '__main__':
    n, s, q, p, r, Q, t = define_parameters()
    df1 = define_starting_df(n, Q)
    df2 = create_number_of_users_df(n, Q)
    k = new_clients(Q, 5, 5)
    k_ = new_clients(Q, 15, 5)
    df1, df2, t = next_year(df1, df2, n, t, s, p, k, k_)
    for i in range(4):
        df1, df2 = new_generation(df1, df2)
        k = new_clients(Q, 5, 5)
        df1, df2, t = next_year(df1, df2, n, t, s, p, k, k_)
        k = new_clients(Q, 5, 5)
        df1, df2, t = next_year(df1, df2, n, t, s, p, k, k_)
    print(df1)
    print(df2)
    plot_df(df2)
