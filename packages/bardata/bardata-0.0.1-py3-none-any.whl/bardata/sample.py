""" sample routines """

import string
import itertools

import numpy as np
import pandas as pd
import datetime as dt

from . import model
from .freqs import pandas_freq, split_frequency

DEFAULT_MAX_DATES = 500

MAXIMUM_PERIODS = dict(
    day=5000,
    week=1000,
    month=200,
    hour=20000,
    minute=20000
)


def maximum_periods(freq: str):
    count, freq = split_frequency(freq)
    return MAXIMUM_PERIODS.get(freq, 200) / count


def sample_dates(max_dates=None, freq=None, *,
                 start_date=None, end_date=None):
    """ sample dates (wrapper around pandas date_range) """

    if freq is None:
        freq = 'daily'

    if not start_date and not end_date:
        end_date = dt.date.today()

    if start_date and end_date:
        periods = None
    elif max_dates:
        periods = max_dates
    else:
        periods = DEFAULT_MAX_DATES

    max_periods = maximum_periods(freq)
    if periods > max_periods:
        periods = max_periods

    freq = pandas_freq(freq)

    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)

    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)

    dates = pd.date_range(periods=periods, start=start_date, end=end_date, freq=freq)

    if max_dates and len(dates) > max_dates:
        dates = dates[-max_dates:]

    return dates


def random_walk(max_bars=None, freq='daily', *,
                start_date=None, end_date=None,
                start_value=100.0, volatility=0.20, fwd_rate=0.10,
                name=None, seed=None):
    """ series of random walk prices """

    generator = np.random.default_rng(seed)

    dates = sample_dates(freq=freq, max_dates=max_bars, start_date=start_date, end_date=end_date)
    count = len(dates)

    avgdelta = dates.diff().mean()
    sampling = pd.Timedelta(days=365) / avgdelta

    fwd = np.log(1 + fwd_rate) / sampling
    std = volatility / np.sqrt(sampling)

    change = generator.standard_normal(count - 1) * std + np.log(1 + fwd)
    price = start_value * np.exp(np.r_[0.0, change.cumsum(0)])

    series = pd.Series(price, index=dates.values, name=name).rename_axis(index='date')

    return series


def sample_prices(max_bars=None, freq='daily', *,
                  start_date=None, end_date=None,
                  start_value=100.0, volatility=0.20, fwd_rate=0.10,
                  skip=0, volume_as_int=True, seed=None):
    """ dataframe of random prices """

    generator = np.random.default_rng(seed)

    dates = sample_dates(freq=freq, max_dates=max_bars, start_date=start_date, end_date=end_date)
    count = len(dates)

    avgdelta = dates.diff().mean()
    sampling = pd.Timedelta(days=365) / avgdelta

    fwd = np.log(1 + fwd_rate) / sampling
    std = volatility / np.sqrt(sampling)

    rnd = generator.standard_normal((count, 4)).cumsum(1) * std + fwd
    cum = np.r_[0.0, rnd[:, -1].cumsum(0)[:-1]]

    op = start_value * np.exp(rnd[:, 0] + cum)
    hi = start_value * np.exp(rnd.max(1) + cum)
    lo = start_value * np.exp(rnd.min(1) + cum)
    cl = start_value * np.exp(rnd[:, -1] + cum)

    vol = np.exp(generator.standard_normal(count) * 0.2 + 1.0) * 50000.0

    data = dict()

    data['date'] = dates.values
    data['open'] = op.round(2)
    data['high'] = hi.round(2)
    data['low'] = lo.round(2)
    data['close'] = cl.round(2)
    data['volume'] = vol.astype(int) if volume_as_int else vol.round(2)

    prices = pd.DataFrame(data).set_index('date')

    if skip > 0:
        prices.iloc[:skip] = np.nan

    if skip < 0:
        prices.iloc[skip:] = np.nan

    return prices


def sample_tickers(count=10, *, ticker_length=3):
    """ sample tickers """

    def ticker_generator(chars=string.ascii_uppercase):
        for length in itertools.count(ticker_length):
            for item in itertools.product(chars, repeat=length):
                yield "".join(item)

    tickers = ticker_generator()

    return list(itertools.islice(tickers, count))


class Prices(model.PriceEngine):
    """ Price Engine """

    def get_prices(self,
                   ticker: str, freq: str = 'daily', *,
                   start_date=None, end_date=None,
                   max_bars=None, adjusted=True):
        prices = sample_prices(freq=freq, max_bars=max_bars,
                               start_date=start_date, end_date=end_date)
        return prices


class Tickers(model.TickerHandler):
    """ Ticker Handler """

    def get_tickers(self, moniker: str = None):
        if moniker is not None:
            raise ValueError(f"Moniker {moniker!r} unexppected")
        tickers = sample_tickers()
        return tickers
