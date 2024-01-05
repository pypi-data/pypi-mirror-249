""" price data """

import sys

import numpy as np
import pandas as pd

from functools import lru_cache

from concurrent.futures import ThreadPoolExecutor, as_completed

from .freqs import pandas_freq, split_frequency
from .dates import quick_timedelta
from .model import PriceEngine

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

# MAYBE add caching (boolean) parameter ... where ?
# MAYBE add source, start_date and end_date to combine_prices ?
# MAYBE can we remove resample param from combine prices ???


DEFAULT_PRICES = 'rawdata'
DEFAULT_INTRADAY = 'polygon'

ENTRY_POINTS = "bardata_prices"


@lru_cache
def default_source(freq: str = None) -> str:
    """ best source for given freq """

    count, freq = split_frequency(freq or 'daily')

    if freq in ('hour', 'minute'):
        return DEFAULT_INTRADAY

    return DEFAULT_PRICES


@lru_cache
def price_engine(source: str = None) -> PriceEngine:
    """ engine for source """

    if source is None:
        source = default_source()

    entries = entry_points(group=ENTRY_POINTS, name=source)

    if not entries:
        raise ValueError(f"No price engine for {source=}")

    entry = tuple(entries)[0]

    engine: PriceEngine = entry.load()(source=source)

    return engine


def get_prices(ticker: str, freq: str = 'daily', *,
               source=None, start_date=None, end_date=None,
               max_bars=None, adjusted=True):
    """ get prices from default engine """

    if freq is None:
        freq = 'daily'

    if source is None:
        source = default_source(freq=freq)

    engine = price_engine(source)

    return engine.get_prices(
        ticker, freq=freq,
        start_date=start_date,
        end_date=end_date,
        max_bars=max_bars,
        adjusted=adjusted
    )


def collect_prices(tickers, *, freq='daily', source=None,
                   start_date=None, end_date=None,
                   max_bars=None, use_threads=True):
    """ yields ticker, prices pais overs list of tickers  """

    if source is None:
        source = default_source(freq=freq)

    kwds = dict(
        freq=freq,
        source=source,
        start_date=start_date,
        end_date=end_date,
        max_bars=max_bars
    )

    if use_threads:
        executor = ThreadPoolExecutor()

        fvmap = {
            executor.submit(get_prices, ticker, **kwds): ticker
            for ticker in tickers
        }

        for fv in as_completed(fvmap):
            ticker = fvmap[fv]
            prices = fv.result()
            if prices is not None:
                yield ticker, prices
    else:
        for ticker in tickers:
            prices = get_prices(ticker, **kwds)
            if prices is not None:
                yield ticker, prices


def combine_prices(tickers, *, freq='daily', source=None, item='close',
                   max_bars=None, period=None, resample=None,
                   pct_change=False, log_returns=False,
                   use_threads=True):
    """
    matrix of closing prices aligned by date
    to insure better aliognement use resample instead of freq
    """

    data = {
        k: v[item]
        for k, v in collect_prices(
            tickers,
            freq=freq,
            source=source,
            max_bars=max_bars,
            use_threads=use_threads
        )
    }

    result = pd.DataFrame(data).dropna()

    if resample is not None:
        rule = pandas_freq(resample)
        result = result.resample(rule).agg('last')

    if period:
        delta = quick_timedelta(period)
        enddate = result.index[-1]
        begdate = enddate - delta
        result = result.loc[begdate:]

    if log_returns:
        result = result.apply(np.log).diff().dropna()

    if pct_change:
        result = result.apply(np.log).diff().dropna().apply(np.exp) - 1

    return result
