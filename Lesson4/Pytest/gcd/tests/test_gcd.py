import pytest
from gcd import gcd

@pytest.mark.parametrize("test_args,expected", [
    ((0,1), 1), ((1,0), 1), ((6,6), 6),
    ((1,50), 1), ((25,1), 1), ((2,4), 2),
    ((2,5), 1), ((5,2), 1), ((7,9), 1)
])
def test_some(test_args, expected):
    assert gcd(*test_args) == expected

def test_some1(test_args, expected):
    assert gcd(*test_args) != expected

def test_input_type_exeption():
    with pytest.raises(TypeError):
        gcd('23', 7)