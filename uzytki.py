import pandas as pd
import numpy as np


# starting parameters
def define_parameters(n_=2, s0_=0.2, s1_=0.4, p0_=0.7,
                      p1_=0.5, p2_=0.9, r0_=0.1, r1_=0.1, r2_=0.1, Q00_=10, Q01_=20, Q02_=50, k_=10):
    n = n_  # number of starting generations
    s0 = s0_
    s1 = s1_
    p0 = p0_
    p1 = p1_
    p2 = p2_
    r0 = r0_
    r1 = r1_
    r2 = r2_
    Q00 = Q00_
    Q01 = Q01_
    Q02 = Q02_
    k = k_
    return n, s0, s1, p0, p1, p2, r0, r1, r2, Q00, Q01, Q02, k


def define_starting_df(n, Q00, Q01, Q02):
    names = ['Q' + str(i) for i in range(n + 1)]
    df = pd.DataFrame(0, index=np.arange(2 * (n + 1) - 5), columns=names)
    df.iloc[0, 0] = Q00
    df.iloc[0, 1] = Q01
    df.iloc[0, 2] = Q02
    t = 0
    return df, t


def next_year(df, t, s0, s1, p0, p1, p2, k):
    row = [0, 0, 0]
    t = t + 1
    print(df.iloc[t - 1][-2])
    row[0] = round(s0 * df.iloc[t - 1][-3])
    row[1] = round(s1 * df.iloc[t - 1][-2])
    row[2] = round(p2 * df.iloc[t - 1][-1] + p1 * df.iloc[t - 1][-2] + p0 * df.iloc[t - 1][-3]) + k
    size = len(df.columns)
    no_zeros = size - 3
    list_zeros = [0] * no_zeros
    print(row)
    row = list_zeros + row
    df.loc[t] = row
    return df, t


def new_generation(df):
    last_name = df.columns[-1]
    number_of_new_gen = str(int(last_name[-1]) + 1)
    new_name = 'Q' + number_of_new_gen
    df[new_name] = 0


if __name__ == '__main__':
    n, s0, s1, p0, p1, p2, r0, r1, r2, Q00, Q01, Q02, k = define_parameters()
    df, t = define_starting_df(n, Q00, Q01, Q02)
    df, t = next_year(df, t, s0, s1, p0, p1, p2, k)
    new_generation(df)
    df, t = next_year(df, t, s0, s1, p0, p1, p2, k)
    df, t = next_year(df, t, s0, s1, p0, p1, p2, k)
    new_generation(df)
    df, t = next_year(df, t, s0, s1, p0, p1, p2, k)
    df, t = next_year(df, t, s0, s1, p0, p1, p2, k)
    print(df)
