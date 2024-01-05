""" utility routines """

import logging
import warnings

import numpy as np
import pandas as pd

from .freqs import pandas_freq

logger = logging.getLogger(__name__)


def extract_dates(prices):
    """ series of dates from column or index data """

    if 'date' in prices:
        dates = prices.get('date')

    elif 'date' in prices.index.names:
        dates = prices.index.get_level_values('date').to_series(index=prices.index)

    else:
        raise ValueError("Dataframe has no date column or index!")

    return dates


def date_offset(prices, *, delta=None, warn=True):
    """
    relative date offset from a prices dataframe

    Returns:
        a series of integers
    """

    dates = extract_dates(prices)

    if delta is None:
        delta = dates.drop_duplicates().sort_values().diff().min()

    minutes = delta / pd.Timedelta(minutes=1)

    if warn and minutes not in (1, 2, 5, 10, 15, 30, 60, 120, 1440):
        warnings.warn(
            f"Implied timedelta {delta} not standard. Use delta parameter!",
            stacklevel=2
        )

    lastd = dates.max()

    offset = (lastd - dates) / delta

    return offset


def get_sampling(prices, basis=365):
    """ average yearly sampling rate """

    dates = extract_dates(prices)

    period = dates.diff().mean()

    return pd.Timedelta(days=basis) / period


def resample_prices(prices, freq):
    """ resample prices """

    freq = pandas_freq(freq)

    aggspec = dict(open='first', high='max', low='min', close='last', volume='sum')
    prices = prices.resample(freq).agg(aggspec).dropna(subset=['close'])

    return prices


def concat_prices(frames, convert_utc=True, remove_duplicates=True):
    """ concatanate prices and remove duplicates """

    if convert_utc:
        frames = [f.tz_convert('UTC') for f in frames]

    prices = pd.concat(frames)

    if remove_duplicates:
        prices = prices[~prices.index.duplicated(keep='last')]

    return prices


def adjust_prices(prices, splits=None, include_divs=False, inplace=False):
    """ adjust prices using split_factor and div_pct """

    if splits is None:
        splits = prices

    split_factor = splits.split_factor.fillna(1.0)

    if include_divs and hasattr(splits, 'div_pct'):
        div_pct = splits.div_pct.fillna(0.0)
        split_factor = split_factor * (div_pct + 1.0)

    cumprod = split_factor[::-1].cumprod()[::-1]

    bak_adjust, adj_factor = cumprod.iloc[0], cumprod.shift(-1).fillna(1.0)

    if splits is not None:
        adj_factor = adj_factor.asof(prices.index).fillna(bak_adjust)

    if not inplace:
        prices = prices.copy()

    for column in ['open', 'high', 'low', 'close', 'vwap', 'price', 'mid']:
        if column in prices:
            prices[column] /= adj_factor

    for column in ['volume']:
        if column in prices:
            prices[column] *= adj_factor

    return prices


def extract_splits(prices):
    """ extracts split & dividend data from daily prices """

    split_factor = prices.split_factor.fillna(1.0)
    columns = [split_factor]
    mask = (split_factor != 1.0)

    if hasattr(prices, 'div_pct'):
        div_pct = prices.div_pct
    elif hasattr(prices, 'div_cash'):
        div_pct = prices.div_cash / prices.close
    else:
        div_pct = None

    if div_pct is not None:
        div_pct = div_pct.fillna(0.0)
        columns.append(div_pct)
        mask = mask | (div_pct != 0.0)

    if np.any(mask):
        splits = pd.concat(columns, axis=1)[mask]
        return splits

    return None


def price_gaps(prices, resample_freq=None):
    """ price gaps in series """

    if resample_freq is not None:
        prices = resample_prices(prices, freq=resample_freq)

    if not prices.index.is_monotonic_increasing:
        raise ValueError("Data is not ordered!")

    if 'adj_close' in prices:
        close = prices.adj_close
        trange = prices.adj_high / prices.adj_low - 1.0
    else:
        close = prices.close
        trange = prices.high / prices.low - 1.0

    change = close.pct_change()

    std = change.rolling(30).std()

    max_change = 0.25

    mask = (change.abs() > max_change) & \
           (change.abs() > std * 5.0) & \
           (change.abs() > trange * 2.0)

    result = change[mask].rename("price gap")

    return result


def time_gaps(prices, max_days=7):
    """ time gaps in series """

    dates = prices.index.to_series()
    dspan = dates.diff()

    result = dspan[dspan > pd.Timedelta(days=max_days)].rename("time gap")

    return result


def check_prices(prices, ticker='series', warn=True, verbose=False):
    """ check prices for possible gaps in price or time """

    if prices is None:
        return False

    result = True

    pgaps = price_gaps(prices)
    tgaps = time_gaps(prices)

    if len(pgaps):
        result = False
        if warn:
            warnings.warn(
                f"{ticker} has {len(pgaps)} price gaps!",
                stacklevel=2
            )
        if verbose:
            print(pgaps)

    if len(tgaps):
        result = False
        if warn:
            warnings.warn(
                f"{ticker} has {len(tgaps)} time gaps!",
                stacklevel=2
            )
        if verbose:
            print(tgaps)

    return result


def fix_price_gaps(prices, gaps=None, verbose=None):
    """ fixes price gaps """

    if gaps is None:
        gaps = price_gaps(prices)

    if gaps.empty:
        logger.debug("No gaps found!")
        return prices

    gaps = gaps.reindex_like(prices).fillna(0.0)

    if verbose:
        for ts, gap in gaps[gaps != 0].iteritems():
            print("Correcting gap of {gap} on {date}...".format(date=ts.date(), gap=gap))

    factor = 1.0 / (1.0 + gaps)
    factor = factor.shift(-1, fill_value=1.0)
    factor = factor[::-1].cumprod()[::-1]

    for col in ['open', 'high', 'low', 'close']:
        if col in prices:
            prices[col] /= factor

    for col in ['volume']:
        if col in prices:
            prices[col] *= factor

    return prices


def append_quote(prices, quote):
    """ append quote (dict with timestamp) to prices (df) """

    ts = quote.get('timestamp')

    if not ts:
        raise ValueError("timestamp is missing!")

    date = pd.to_datetime(ts[:10])

    if date <= prices.index[-1]:
        return

    record = dict(quote, close=quote['last'], split_factor=1.0, div_pct=0.0)
    record = {k: record.get(k) for k in prices.columns if k in record}

    prices.loc[date] = record


def slice_prices(prices, start_date=None, end_date=None, max_bars=None):
    """ slice prices dataframe """

    if start_date is not None:
        prices = prices.loc[start_date:]

    if end_date is not None:
        prices = prices.loc[:end_date]

    if max_bars:
        prices = prices.tail(max_bars)

    return prices
