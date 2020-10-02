from typing import *
from functools import total_ordering


def is_number(a):
    return isinstance(a, (int, float))


@total_ordering
class UnitValue(SupportsFloat, SupportsInt, SupportsAbs, SupportsRound, Hashable):
    def __init__(self, value: float, up: Sequence[str], down: Sequence[str]=None):
        self.value = float(value)
        self.up = list(sorted(up))
        self.down = list(sorted(down)) if down else []
        i = 0
        while i < len(self.down):
            if self.down[i] in self.up:
                self.up.remove(self.down[i])
                self.down.remove(self.down[i])
            else:
                i += 1

    def replace_unit(self, unit):
        new_up = list(self.up)
        new_down = list(self.down)
        for up in unit.up:
            if up in new_up:
                new_up.remove(up)
            else:
                new_down += [up]
        for down in unit.down:
            if down in new_down:
                new_down.remove(down)
            else:
                new_up += [down]
        new_up += [unit]
        return UnitValue(self.value, new_up, new_down)

    def __truediv__(self, other):
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

    def __mul__(self, other):
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

    def __add__(self, other):
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

    def __sub__(self, other):
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

    def __round__(self):
        return UnitValue(round(self.value), self.up, self.down)

    def __abs__(self):
        return UnitValue(abs(self.value), self.up, self.down)

    def __same_type(self, other):
        return isinstance(other, type(self)) and self.up == other.up and self.down == other.down

    def __lt__(self, other):
        return self.__same_type(other) and self.value < other.value

    def __eq__(self, other):
        return self.__same_type(other) and self.value == other.value

    def __hash__(self):
        return hash((self.value, self.up, self.down))

    def __repr__(self):
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
    def __init__(self, signature: str):
        self.signature = signature

    def __call__(self, value: float) -> UnitValue:
        return UnitValue(value, [self])

    def __lt__(self, other):
        return isinstance(other, type(self)) and self.signature < other.signature

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.signature == other.signature
    
    def __hash__(self):
        return hash(self.signature)

    def __repr__(self) -> str:
        return "Unit<{}>".format(self.signature)


class Composite(Unit):
    def __init__(self, signature, up, down):
        Unit.__init__(self, signature)
        self.up = up
        self.down = down
