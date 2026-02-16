def add(a: int, b: int) -> int:
    """Simple function used for test generation demos."""
    return a + 

def safe_divide(a: float, b: float) -> float:
    """Division with a clear error on divide-by-zero."""
    if b == 0:
        raise ValueError("b must not be 0")
    return a / b
