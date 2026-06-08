"""
Preverjanje pravilnosti kode v modulu tools.py
"""

__author__ = 'Janko Slavic'

import tools
import numpy as np
import sympy as sym

zacetna = np.asarray([[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 9]])
zamenjana_0_1_stolpca = np.asarray([[2, 1, 3],
                                    [5, 4, 6],
                                    [8, 7, 9]])

zamenjana_0_1_vrstica = np.asarray([[4, 5, 6],
                                    [1, 2, 3],
                                    [7, 8, 9]])


def test_swap_columns():
    a = zacetna.copy() # naredimo kopijo podatkov
    b = tools.swap_columns(a, 0, 1) # b (in tudi a) imata zamenjane stolpce
    np.testing.assert_allclose(b, zamenjana_0_1_stolpca)

def test_swap_rows():
    a = zacetna.copy() # naredimo kopijo podatkov
    b = tools.swap_rows(a, 0, 1) # b (in tudi a) imata zamenjani vrstici
    np.testing.assert_allclose(b, zamenjana_0_1_vrstica)

def test_symbolic_expression():
    x = sym.symbols('x', positive=True) # poskusite tukaj positive=False
    a = x**2
    b = sym.sqrt(x**4)
    np.testing.assert_equal(a==b,True)



if __name__ == '__main__':
    test_symbolic_expression()