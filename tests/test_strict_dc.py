import pytest

from dataclasses import dataclass, is_dataclass
from typing import Dict, List, Union, Tuple

from strict_dc import StrictDcError, StrictDC


@dataclass
class TestDC(StrictDC):
    a: int
    b: str
    c: Dict[str, int]
    d: List[float]
    e: Tuple[int, str, float]
    f: Union[str, int, None]


@pytest.mark.parametrize("a, b, c, d, e, f", [
    ('a', 'b', dict(c=5), [6.8, 2.3], (5, 'e', 6.7), None),
    (3, 1, dict(c=5), [6.8, 2.3], (5, 'e', 6.7), None),
    (3, 'b', dict(c='5'), [6.8, 2.3], (5, 'e', 6.7), None),
    (3, 'b', dict(c=5), ['6.2', 2.3], (5, 'e', 6.7), None),
    (3, 'b', dict(c=5), [6.2, 2.3], (5, 6, 6.7), None),
    (3, 'b', dict(c=5), [6.2, 2.3], (5, 'e', 6.7), 5.5),
])
def test_invalid_dataclass(a, b, c, d, e, f):
    with pytest.raises(StrictDcError):
        TestDC(a=a, b=b, c=c, d=d, e=e, f=f)


@pytest.mark.parametrize("a, b, c, d, e, f", [
    (3, 'b', dict(c=5), [6.8, 2.3], (5, 'e', 6.7), None),
    (3, 'b', dict(c=5), [6.8, 2.3], (5, 'e', 6.7), 'a'),
    (3, 'b', dict(c=5, v=2), [6.8, 2.3], (5, 'e', 6.7), None),
    (3, 'b', dict(c=5), [6.8, 2.3, 8.3], (5, 'e', 6.7), None),
])
def test_valid_dataclass(a, b, c, d, e, f):
    assert is_dataclass(TestDC(a=a, b=b, c=c, d=d, e=e, f=f))
