```python
import pytest
from apps.sample-service.src.app import add, safe_divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, -1) == -2
    assert add(0, 0) == 0

def test_safe_divide():
    assert safe_divide(10, 2) == 5.0
    assert safe_divide(-10, 2) == -5.0
    assert safe_divide(10, -2) == -5.0
    with pytest.raises(ValueError, match="b must not be 0"):
        safe_divide(10, 0)
```
