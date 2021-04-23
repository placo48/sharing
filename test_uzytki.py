from uzytki import define_starting_df
import pandas as pd
from uzytki import new_clients


def test_define_starting_df():
    assert define_starting_df(3, [10, 20, 50, 100]).equals(
        pd.DataFrame({'Q0': [10], 'Q1': [20], 'Q2': [50], 'Q3': [100]},
                     columns=['Q0', 'Q1', 'Q2', 'Q3']))
    assert define_starting_df(2, [10, 20, 50]).equals(pd.DataFrame({'Q0': [10], 'Q1': [20], 'Q2': [50]},
                                                                   columns=['Q0', 'Q1', 'Q2']))


def test_new_clients():
    Q = [10, 20, 50]
    arg1 = 10
    arg2 = 2
    x = new_clients(Q, arg1, arg2)
    print(x)

if __name__=='__main__':
    test_new_clients()