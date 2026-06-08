""" Tools for working with matrices
"""
__author__ = 'Janko Slavic'

import numpy as np


def swap_columns(matrix, i, j):
    """ Swap two columns

    :param matrix:
    :param i:
    :param j:
    :return: matrix with swapped values
    """
    matrix[:, [i, j]] = matrix[:, [j, i]]  # here we use advanced slicing!
    return matrix


def swap_rows(matrix, i, j):
    """ Swap two rows

    :param matrix:
    :param i:
    :param j:
    :return: matrix with swapped values
    """
    # TODO check whether this really works correctly
    matrix[[j, i], :] = matrix[[i, j], :]
    return matrix


def gaussian_elimination(A, b, show_steps=False):
    """ Returns the Gaussian elimination of the augmented coefficient matrix

    :param A: coefficient matrix
    :param b: vector of constants
    :param show_steps: whether to print the individual steps
    :return Ab: augmented coefficient matrix
    """
    Ab = np.column_stack((A, b))
    for p, pivot_row in enumerate(Ab[:-1]):
        for row in Ab[p + 1:]:
            if pivot_row[p]:
                row[p:] = row[p:] - pivot_row[p:] * row[p] / pivot_row[p]
            else:
                raise Exception('Division by 0.')
        if show_steps:
            print('Step: {:g}'.format(p))
            print(Ab)
    return Ab


def gaussian_elimination_pivoting(A, b, show_steps=False):
    """ Returns the Gaussian elimination of the augmented coefficient matrix, uses partial pivoting

    :param A: coefficient matrix
    :param b: vector of constants
    :param show_steps: whether to print the individual steps
    :return Ab: augmented coefficient matrix
    """
    Ab = np.column_stack((A, b))
    for p in range(len(Ab) - 1):
        p_max = np.argmax(np.abs(Ab[p:, p])) + p
        if p != p_max:
            Ab[[p], :], Ab[[p_max], :] = Ab[[p_max], :], Ab[[p], :]
        pivot_row = Ab[p, :]
        for row in Ab[p + 1:]:
            if pivot_row[p]:
                row[p:] = row[p:] - pivot_row[p:] * row[p] / pivot_row[p]
            else:
                raise Exception('Division by 0.')
        if show_steps:
            print('Step: {:g}'.format(p))
            print('Pivot row:', pivot_row)
            print(Ab)
    return Ab


def gauss_solve(Ab):
    """ Given the Gaussian elimination of the augmented matrix Ab, returns the solution vector x.

    :param Ab: augmented coefficient matrix
    :return x: solution vector
    """
    n = len(Ab)
    x = np.zeros(n)
    for p, pivot_row in enumerate(Ab[::-1]):
        x[n - p - 1] = (pivot_row[-1] - pivot_row[n - p:-1] @ x[n - p:]) / (pivot_row[n - p - 1])
    return x


def LU_decomposition(A):
    """ Returns the decomposition of A as ``[L\\U]`` """
    # elimination
    for p, pivot_row in enumerate(A[:-1]):
        for i, row in enumerate(A[p + 1:]):
            if pivot_row[p]:
                m = row[p] / pivot_row[p]
                row[p:] = row[p:] - pivot_row[p:] * m
                row[p] = m
    return A


def LU_solve(LU, b):
    """ Returns the value x given ``[L\\U]x=b`` """
    y = np.zeros_like(b)
    x = np.zeros_like(b)
    for i, b_ in enumerate(b):
        y[i] = (b_ - np.dot(LU[i, :i], y[:i]))
    n = len(b)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - LU[i, i + 1:] @ x[i + 1:]) / LU[i, i]
    return x


def LU_decomposition_pivoting(A, show_steps=False):
    """ Returns the LU decomposition matrix and the vector of swapped rows, uses partial pivoting

    :param A:           coefficient matrix
    :param show_steps:  print the individual steps
    :return LU:         LU matrix
    :return pivoting:   vector of row swaps (important when finding the solution)
    """
    LU = A.copy()
    pivoting = np.arange(len(A))
    for p in range(len(LU) - 1):
        p_max = np.argmax(np.abs(LU[p:, p])) + p
        if p != p_max:
            LU[[p], :], LU[[p_max], :] = LU[[p_max], :], LU[[p], :]
            pivoting[p], pivoting[p_max] = pivoting[p_max], pivoting[p]
        pivot_row = LU[p, :]
        for row in LU[p + 1:]:
            if pivot_row[p]:
                m = row[p] / pivot_row[p]
                row[p:] = row[p:] - pivot_row[p:] * m
                row[p] = m
            else:
                raise Exception('Division by 0.')
        if show_steps:
            print('Step: {:g}'.format(p))
            print('Pivot row:', pivot_row)
            print(LU)
    return LU, pivoting


def LU_solve_pivoting(LU, b, pivoting):
    """ Returns the value x given ``[L\\U]x=b``.

        Use this in the case of partial pivoting
    """
    y = np.zeros_like(b)
    x = np.zeros_like(b)
    for i, b_ in enumerate(b[pivoting]):
        y[i] = (b_ - LU[i, :i] @ y[:i])
    n = len(b)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - LU[i, i + 1:] @ x[i + 1:]) / LU[i, i]
    return x


if __name__ == '__main__':
    import numpy as np

    a = np.arange(9).reshape((3, 3))
    b = swap_columns(a, 0, 1)
    print(b)
    c = swap_rows(a, 0, 1)  # we must not forget: a only points to a memory location
    print(c)
