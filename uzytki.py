import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# starting parameters
def define_parameters(n_=3, s0=0.1, s1=0.6, s2=0.65, p0=0.5,
                      p1=0.3, p2=0.3, p3=0.9, r0=0.4, r1=0.1, r2=0.05, r3=0.1,
                      Q00=10, Q01=20, Q02=50, Q03=100, k_=30, t_=0):
    n = n_  # number of starting generations
    s = [s0, s1, s2]
    p = [p0, p1, p2, p3]
    r = [r0, r1, r2, r3]
    Q = [Q00, Q01, Q02, Q03]
    k = k_
    t = t_
    return n, s, p, r, Q, k, t


def define_starting_df(n, Q):
    names = ['Q' + str(i) for i in range(n + 1)]
    df = pd.DataFrame(0, index=np.arange(1), columns=names)
    for j in range(n + 1):
        df.iloc[0, j] = Q[j]
    return df


def next_year(df, df2, n, t, s, p, k):
    row = [0] * (n + 1)
    t = t + 1
    for j in range(n + 1):
        if j != n:
            row[j] = round(s[j] * df.iloc[t - 1][-(n - j + 1)])
        elif j == n:
            for i in range(n + 1):
                row[j] += round(p[i] * df.iloc[t - 1][-n + i - 1])
            row[j] += k
    size = len(df.columns)
    no_zeros = size - (n + 1)
    list_zeros = [0] * no_zeros
    row = list_zeros + row
    df.loc[t] = row

    new_users = 0
    for l in range(n):
        new_users += round(p[l] * df.iloc[t - 1][-n + l - 1])
    new_users += k
    last_row = df2.loc[t - 1]
    last_row[-1] += new_users
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
    n, s, p, r, Q, k, t = define_parameters()
    df = define_starting_df(n, Q)
    df2 = create_number_of_users_df(n, Q)
    df, df2, t = next_year(df, df2, n, t, s, p, k)
    for i in range(6):
        df, df2 = new_generation(df, df2)
        df, df2, t = next_year(df, df2, n, t, s, p, k)
        df, df2, t = next_year(df, df2, n, t, s, p, k)
    print(df)
    print(df2)
    plot_df(df2)
