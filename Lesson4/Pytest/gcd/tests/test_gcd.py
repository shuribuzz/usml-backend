import pytest
from gcd import gcd

@pytest.mark.parametrize("test_input,expected", [
    ("gcd(0, 1)", 1),
    ("gcd(1, 0)", 1),
    ("gcd(6, 6)", 6),
    ("gcd(2, 1)" or "gcd(1 , 5)", 1),
    ("gcd(2, 4)", 2),
    ("gcd(2, 5)", 1),
    ("gcd(5, 2)", 2),
    ("gcd(7, 9)", 1),
])

def test_eval(test_input, expected):
    assert eval(test_input) == expected

def test_exeption():
    with pytest.raises(TypeError):
        gcd('23', 7)


