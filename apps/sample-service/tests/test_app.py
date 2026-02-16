import pytest
from apps.sample_service.src.app import add, safe_divide

def test_add_basic():
    assert add(2, 3) == 5

def test_safe_divide_basic():
    assert safe_divide(10, 2) == 5

def test_safe_divide_zero():
    with pytest.raises(ValueError):
        safe_divide(10, 0)
