import numpy as np
from sympy import solve, Eq, symbols
from uzytki import new_clients


def test_new_clients():
    Q = [10, 20, 50]
    arg1 = 5
    arg2 = 1
    x = new_clients(Q, arg1, arg2)
    print(x)


if __name__ == '__main__':
    test_new_clients()
