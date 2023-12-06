import pytest
def add(a,b):
    return(a + b)
def sub(a, b):
    return(a - b)



 
def test_add():
    assert add(4, 5) == 9
def test_sub():
    assert sub(4, 5) == -1