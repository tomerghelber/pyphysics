from typing import *
from functools import total_ordering


def is_number(a: Any):
    return isinstance(a, (int, float))


@total_ordering
class UnitValue(SupportsFloat, SupportsInt, SupportsAbs, SupportsRound):
    """Wrapper of float to has physics units as part of its type.
    """

    def __init__(self, value: float, up: Sequence[str], down: Sequence[str]=None):
        self.value = float(value)
        up = list(sorted(up))
        down = list(sorted(down)) if down else []
        i = 0
        while i < len(down):
            current = down[i]
            if current in up:
                up.remove(current)
                down.remove(current)
            else:
                i += 1
        self.up = tuple(up)
        self.down = tuple(down)

    def replace_unit(self, unit: 'Composite', power: Optional[int]=None):
        """
        Args:
            power: If exists, replace unit with the power.
        """
        new_up = list(self.up)
        new_down = list(self.down)
        for _ in range(power or new_up.count(unit)):
            new_up.remove(unit)
            new_up += unit.up
            new_down += unit.down
        for _ in range(power or new_down.count(unit)):
            new_down.remove(unit)
            new_down += unit.up
            new_up += unit.down
        return UnitValue(self.value, new_up, new_down)

    def replace_to_unit(self, unit: 'Composite', power: Optional[int]=None):
        """
        Args:
            power: If exists, replace unit with the power.
        """
        new_up = list(self.up)
        new_down = list(self.down)

        if power is None:
            max_replace = max([new_up.count(elem) / count for elem, count in Counter(unit.up).items()] + [new_down.count(elem) / count for elem, count in Counter(unit.down).items()])
        else:
            max_replace = power
        new_up += unit.down * max_replace
        new_down += unit.up * max_replace

        return UnitValue(self.value, new_up, new_down)

    def __truediv__(self, other: 'UnitValue' or float or int):
        """
        Examples:
            >>> Meter = Unit("m")
            >>> Second = Unit("sec")
            >>> v1 = Meter(2)
            >>> v2 = Second(3)
            >>> v3 = v1 / v2
            >>> v3.value == v1.value / v2.value
            True
            >>> Meter in v3.up
            True
            >>> Second in v3.down
            True
            >>> len(v3.up)
            1
            >>> len(v3.down)
            1
            >>> v3 = v1 / v1
            >>> v3.value
            1.0
            >>> len(v3.up)
            0
            >>> len(v3.down)
            0
            >>> scalar = 4
            >>> v4 = v3 / scalar
            >>> v4.value == v3.value / scalar
            True
            >>> v4.up == v3.up
            True
            >>> v4.down == v3.down
            True
        """
        if is_number(other):
            return UnitValue(self.value / other, self.up, self.down)
        return UnitValue(self.value / other.value, self.up + other.down, self.down + other.up)

    def __mul__(self, other: 'UnitValue' or float or int):
        """
        Examples:
            >>> Meter = Unit("m")
            >>> Second = Unit("sec")
            >>> v1 = Meter(2)
            >>> v2 = Second(3)
            >>> v3 = v1 * v2
            >>> v3.value == v1.value * v2.value
            True
            >>> Meter in v3.up
            True
            >>> Second in v3.up
            True
            >>> len(v3.up)
            2
            >>> len(v3.down)
            0
            >>> scalar = 4
            >>> v4 = v3 * scalar
            >>> v4.value == v3.value * scalar
            True
            >>> v4.up == v3.up
            True
            >>> v4.down == v3.down
            True
        """
        if is_number(other):
            return UnitValue(self.value * other, self.up, self.down)
        return UnitValue(self.value * other.value, self.up + other.up, self.down + other.down)

    def __add__(self, other: 'UnitValue'):
        """
        Examples:
            >>> Meter = Unit("m")
            >>> v1 = Meter(2)
            >>> v2 = v1 + v1
            >>> v2.value == v1.value + v1.value
            True
            >>> v2.up == v1.up
            True
            >>> v2.down == v1.down
            True
        """
        if not self.__same_type(other):
            raise TypeError("Not the same type")
        return UnitValue(self.value + other.value, self.up, self.down)

    def __sub__(self, other: 'UnitValue'):
        """
        Examples:
            >>> Meter = Unit("m")
            >>> v1 = Meter(2)
            >>> v2 = v1 - v1
            >>> v2.value
            0.0
            >>> v2.up == v1.up
            True
            >>> v2.down == v1.down
            True
        """
        if not self.__same_type(other):
            raise TypeError("Not the same type")
        return UnitValue(self.value - other.value, self.up, self.down)

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __round__(self) -> 'UnitValue':
        return UnitValue(round(self.value), self.up, self.down)

    def __abs__(self) -> 'UnitValue':
        return UnitValue(abs(self.value), self.up, self.down)

    def __same_type(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.up == other.up and self.down == other.down

    def __lt__(self, other: Any) -> bool:
        return self.__same_type(other) and self.value < other.value

    def __eq__(self, other: Any) -> bool:
        return self.__same_type(other) and self.value == other.value

    def __hash__(self) -> int:
        return hash((self.value, self.up, self.down))

    def __repr__(self) -> str:
        up = "*".join(map(lambda a: a.signature, self.up))
        down = "*".join(map(lambda a: a.signature, self.down))
        if down:
            if len(self.up) > 1:
                up = "({})".format(up)
            if len(self.down) > 1:
                down = "({})".format(down)
            unit_type = "{}/{}".format(up, down)
        else:
            unit_type = up
        return "{} {}".format(self.value, unit_type)


@total_ordering
class Unit(Callable[[float], UnitValue], Hashable):
    """A physics unit to create unit value.
    """
    def __init__(self, signature: str):
        self.signature = signature

    def __call__(self, value: float) -> UnitValue:
        return UnitValue(value, [self])

    def __lt__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.signature < other.signature

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.signature == other.signature
    
    def __hash__(self) -> int:
        return hash(self.signature)

    def __repr__(self) -> str:
        return "Unit<{}>".format(self.signature)


class Composite(Unit):
    """A physics unit that is bult from several basic units.
    """
    def __init__(self, signature: str, up: Sequence[Unit], down: Sequence[Unit]):
        Unit.__init__(self, signature)
        self.up = up
        self.down = down
