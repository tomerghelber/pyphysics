from pyphysics  import *

class Time(Unit):
    pass

class Length(Unit):
    pass

class Composite(Unit):
    def __init__(self, signature, up, down):
        Unit.__init__(self, signature)
        self.up = up
        self.down = down


def test_truediv_different():
    Meter = Length("m")
    Second = Time("sec")
    v1 = Meter(2)
    v2 = Second(3)
    v3 = v1 / v2
    assert v3.value == v1.value / v2.value
    assert Meter in v3.up
    assert Second in v3.down
    assert 1 == len(v3.up)
    assert 1 == len(v3.down)

def test_truediv_same():
    Meter = Length("m")
    v1 = Meter(2)
    v3 = v1 / v1
    assert v3.value == 1
    assert 0 == len(v3.up)
    assert 0 == len(v3.down)

def test_truediv_partially():
    Meter = Length("m")
    Second = Time("sec")
    v1 = Meter(2)
    v2 = Second(3)
    v3 = v1 / (v2 * v2)
    assert v3.value == v1.value / (v2.value * v2.value)
    assert 1 == len(v3.up)
    assert 2 == len(v3.down)

def test_mul():
    Meter = Length("m")
    Second = Time("sec")
    v1 = Meter(2)
    v2 = Second(3)
    v3 = v1 * v2
    assert v3.value == v1.value * v2.value
    assert Meter in v3.up
    assert Second in v3.up
    assert 2 == len(v3.up)
    assert not v3.down

def test_mul_than_div():
    Meter = Length("m")
    Second = Time("sec")
    v1 = Meter(2)
    v2 = Second(3)
    v3 = v1 / (v2 * v2)
    assert v3.value == v1.value / (v2.value * v2.value)
    assert Meter in v3.up
    assert Second in v3.down
    assert 1 == len(v3.up)
    assert 2 == len(v3.down)

def test_div_than_mul():
    Meter = Length("m")
    Second = Time("sec")
    v1 = Meter(2)
    v2 = Second(3)
    v3 = v1 / v2 * v1
    assert v3.value == v1.value / v2.value * v1.value
    assert Meter in v3.up
    assert Second in v3.down
    assert 2 == len(v3.up)
    assert 1 == len(v3.down)

def test_add_only_same_type():
    Meter = Length("m")
    Second = Time("sec")
    v1 = Meter(2)
    v2 = Second(3)
    try:
        v1 + v2
    except TypeError:
        pass

def test_sub_only_same_type():
    Meter = Length("m")
    Second = Time("sec")
    v1 = Meter(2)
    v2 = Second(3)
    try:
        v1 - v2
    except TypeError:
        pass

def test_add():
    Meter = Length("m")
    v1 = Meter(2)
    v2 = v1 + v1
    assert v2.value == v1.value + v1.value
    assert v2.up == v1.up
    assert v2.down == v1.down

def test_sub():
    Meter = Length("m")
    v1 = Meter(2)
    v2 = v1 - v1
    assert v2.value == 0
    assert v2.up == v1.up
    assert v2.down == v1.down

def test_replace_unit_fully():
    Meter = Length("m")
    Second = Time("sec")
    Newton = Composite("N", [Meter], [Second, Second])
    v1 = Meter(2)
    v2 = Second(3)
    v3 = v1 / (v2 * v2)
    v4 = v3.replace_unit(Newton)
    assert v4.value == v3.value
    assert Newton in v4.up
    assert Second not in v4.down
    assert Meter not in v4.down
    assert 1 == len(v4.up)
    assert 0 == len(v4.down)

def test_replace_unit_partial():
    Meter = Length("m")
    Second = Time("sec")
    Newton = Composite("N", [Meter], [Second, Second])
    v1 = Meter(2)
    v2 = Second(3)
    v3 = v1 / v2
    v4 = v3.replace_unit(Newton)
    assert v4.value == v3.value
    assert Newton in v4.up
    assert Second in v4.up
    assert Second not in v4.down
    assert Meter not in v4.down
    assert 2 == len(v4.up)
    assert 0 == len(v4.down)
