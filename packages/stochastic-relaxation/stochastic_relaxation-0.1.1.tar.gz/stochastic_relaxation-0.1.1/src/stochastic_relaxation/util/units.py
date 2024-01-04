'''
Handle units using pint
'''

from pint import UnitRegistry, Quantity

#=======#
# Units #
#=======#
ureg = UnitRegistry()
Q_ = ureg.Quantity

def assert_pint_type(item, units: str):
    '''
    Assert that item is a pint Quantity with given units, and return item.
    If item is a string, converts to pint Quantity and asserts units.
    '''
    assert type(item) == str or type(item) == Quantity, f'{item} must be a string or pint Quantity'
    if type(item) == str:
        val, unit = item.split(' ', 1)
        item = Q_(float(val), unit)
    assert item.check(units), f'{item} must have units {units}'
    return item

def assert_pint_si_type(item, units: str):
    '''
    Assert that item is a pint Quantity with given units, and returns item in SI units.
    If item is a string, converts and returns pint Quantity in SI units.
    '''
    item = assert_pint_type(item, units)
    item = item.to_base_units()
    return item

def assert_pint_si_magnitude(item, units: str):
    '''
    Assert that item is a pint Quantity with given units, and returns item magnitude in SI units.
    If item is a string, converts and returns pint Quantity magnitude in SI units.
    '''
    item = assert_pint_si_type(item, units)
    return item.magnitude
