import sys
sys.path.append('src')
import pandas as pd
from cmpd.main import cmpd_set, cmpd_get_diff

def test_cmpd_set_1():
    uoa = 'cc'
    a = 'tests/data/test3/inputA.csv'
    b = 'tests/data/test3/inputB.csv'
    assert cmpd_set(uoa, a, b) == True

def test_cmpd_set_2():
    uoa = 'cc'
    a = 'tests/data/test4/inputA.csv'
    b = 'tests/data/test4/inputB.csv'
    assert cmpd_set(uoa, a, b) == False

def test_cmpd_get_diff_1():
    uoa = 'cc'
    a = 'tests/data/test4/inputA.csv'
    b = 'tests/data/test4/inputB.csv'
    assert cmpd_get_diff(uoa, b, a) == {'E'}
 