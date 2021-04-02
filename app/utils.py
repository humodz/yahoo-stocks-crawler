import re


# +10000.00M
_parse_amount_regexp = re.compile(r'([-+])?(\d+(\.\d+)?)(\D)?')

# percent, million, billion, etc
_modifiers = {
    '%': 1 / 100,
    'M': 1000 ** 2,
    'B': 1000 ** 3,
    'T': 1000 ** 4,
}


def parse_amount(raw_value: str):
    raw_value = raw_value.strip().replace(',', '')

    if raw_value == '' or raw_value.upper() == 'N/A':
        return None

    sign, str_value, _, modifier = _parse_amount_regexp.match(raw_value).groups()

    result = float(str_value)

    if sign == '-':
        result = -result

    if modifier is not None:
        if modifier not in _modifiers:
            raise RuntimeError(f'Unknown modifier: {modifier}')
        result = result * _modifiers[modifier]

    return result

