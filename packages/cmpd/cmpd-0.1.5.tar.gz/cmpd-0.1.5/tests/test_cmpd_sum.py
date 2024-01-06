import sys
sys.path.append('src')
import pandas as pd
from cmpd.main import cmpd_sum

def test_cmpd_sum_1():
    uoa = 'cc'
    agg = 'amount'
    a = 'tests/data/test1/input.csv'
    b = 'tests/data/test1/control.csv'
    assert cmpd_sum(uoa, a, b, agg) == True
    
def test_cmpd_sum_2():
    uoa = ['cc','mon']
    agg = 'amount'
    a = 'tests/data/test2/input.csv'
    b = 'tests/data/test2/control.csv'
    assert cmpd_sum(uoa, a, b, agg) == True
