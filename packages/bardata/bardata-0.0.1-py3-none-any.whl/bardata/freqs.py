""" frequency utils """

# see https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases

import re

PANDAS_FREQ = dict(day='B', week='W', month='M', year='Y', hour='H', minute='T')


def split_frequency(freq: str) -> str:
    """ split freq string into count and frequency (long name) """

    if match := re.fullmatch(r"(\d+)(\w+)", freq):
        count, freq = int(match.group(1)), match.group(2)
    elif match := re.fullmatch(r"(\w+)", freq):
        count, freq = 1, match.group(1)
    else:
        raise ValueError(f"Invalid freq {freq!r}")

    if freq in ('D', 'day', 'daily'):
        freq = 'day'
    elif freq in ('W', 'week', 'weekly'):
        freq = 'week'
    elif freq in ('M', 'month', 'monthly'):
        freq = 'month'
    elif freq in ('Y', 'year', 'yearly'):
        freq = 'year'
    elif freq in ('H', 'hour', 'hourly'):
        freq = 'hour'
    elif freq in ('T', 'min', 'minute'):
        freq = 'minute'
    else:
        raise ValueError(f"Invalid freq {freq!r}")

    return count, freq


def pandas_freq(freq: str) -> str:
    """ map a frequency string to a pandas frequency string """

    count, freq = split_frequency(freq)
    freq = PANDAS_FREQ.get(freq)

    if count != 1:
        freq = f"{count}{freq}"

    return freq

