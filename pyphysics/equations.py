from .units import Unit, Composite, UnitValue


meter = Unit('m')
gram = Unit('g')
second = Unit('sec')

newton = Composite('N', up=[gram, meter], down=[second, second])

def centerfugal_force(m: UnitValue[gram], v, r: UnitValue[meter]):
    return m * v * v / r
