import pytest

from pyphysics  import *


def test_truediv_same():
    Meter = Unit("m")
    v1 = Meter(2)
    v3 = v1 / v1
    assert v3.value == 1
    assert 0 == len(v3.up)
    assert 0 == len(v3.down)


def test_truediv_partially():
    Meter = Unit("m")
    Second = Unit("sec")
    v1 = Meter(2)
    v2 = Second(3)
    v3 = v1 / (v2 * v2)
    assert v3.value == v1.value / (v2.value * v2.value)
    assert 1 == len(v3.up)
    assert 2 == len(v3.down)


def test_mul_than_div():
    Meter = Unit("m")
    Second = Unit("sec")
    v1 = Meter(2)
    v2 = Second(3)
    v3 = v1 / (v2 * v2)
    assert v3.value == v1.value / (v2.value * v2.value)
    assert Meter in v3.up
    assert Second in v3.down
    assert 1 == len(v3.up)
    assert 2 == len(v3.down)


def test_div_than_mul():
    Meter = Unit("m")
    Second = Unit("sec")
    v1 = Meter(2)
    v2 = Second(3)
    v3 = v1 / v2 * v1
    assert v3.value == v1.value / v2.value * v1.value
    assert Meter in v3.up
    assert Second in v3.down
    assert 2 == len(v3.up)
    assert 1 == len(v3.down)


def test_add_only_same_type():
    Meter = Unit("m")
    Second = Unit("sec")
    v1 = Meter(2)
    v2 = Second(3)
    with pytest.raises(TypeError):
        v1 + v2


def test_sub_only_same_type():
    Meter = Unit("m")
    Second = Unit("sec")
    v1 = Meter(2)
    v2 = Second(3)
    with pytest.raises(TypeError):
        v1 - v2


def test_replace_to_unit_fully():
    Meter = Unit("m")
    Second = Unit("sec")
    Newton = Composite("N", [Meter], [Second, Second])
    v1 = Meter(2)
    v2 = Second(3)
    v3 = v1 / (v2 * v2)
    v4 = v3.replace_to_unit(Newton, 1)
    assert v4.value == v3.value
    assert Newton in v4.up
    assert Second not in v4.down
    assert Meter not in v4.down
    assert 1 == len(v4.up)
    assert 0 == len(v4.down)


def test_replace_to_unit_partial():
    Meter = Unit("m")
    Second = Unit("sec")
    Newton = Composite("N", [Meter], [Second, Second])
    v1 = Meter(2)
    v2 = Second(3)
    v3 = v1 / v2
    v4 = v3.replace_to_unit(Newton, 1)
    assert v4.value == v3.value
    assert Newton in v4.up
    assert Second in v4.up
    assert Second not in v4.down
    assert Meter not in v4.down
    assert 2 == len(v4.up)
    assert 0 == len(v4.down)
