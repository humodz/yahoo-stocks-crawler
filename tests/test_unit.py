import pytest

from app.utils import parse_amount


@pytest.mark.unit
@pytest.mark.parametrize(['argument', 'expected'], [
    # Preserve exact input
    ('123.45', 123.45),
    ('+123.45', 123.45),
    ('-333.33', -333.33),
    # Modifiers
    ('45%', 0.45),
    ('-67%', -0.67),
    ('1M', 1000000),
    ('+1.23M', 1230 * 1000),
    ('-4.56M', -4560 * 1000),
    ('3456B', 3456 * (1000 ** 3)),
    ('99T', 99 * (1000 ** 4)),
    # Commas
    ('1,000.00', 1000),
    ('1,000,000.00', 1000 ** 2),
    # Spaces
    ('   1234   ', 1234),
    ('   34B   ', 34 * (1000 ** 3)),
    # Empty
    ('', None),
    ('N/A', None),
    ('n/a', None),
])
def test_parse_amount_valid(argument, expected):
    assert parse_amount(argument) == expected


@pytest.mark.unit
@pytest.mark.parametrize('argument', [
    'ff', 'dkwqke', '1.000.000', '12asd314%', '3456MT', 'M123', '12-', '12-34', '123 B'
])
def test_parse_amount_error(argument):
    with pytest.raises(ValueError):
        parse_amount(argument)


