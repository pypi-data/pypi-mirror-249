""" ticker data """

import sys

from functools import lru_cache

from .model import TickerHandler

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

DEFAULT_SOURCE = "rawdata"
ENTRY_POINTS = "bardata_tickers"


@lru_cache
def default_source() -> str:
    return DEFAULT_SOURCE


@lru_cache
def ticker_handler(source: str = None) -> TickerHandler:
    if source is None:
        source = default_source()

    entries = entry_points(group=ENTRY_POINTS, name=source)

    if not entries:
        raise ValueError(f"No ticker engine for {source=}")

    entry = list(entries)[0]

    engine: TickerHandler = entry.load()(source)

    return engine


def get_tickers(moniker: str = None, *, source: str = None):
    """ tickers for index/portfolio symbol """

    handler = ticker_handler(source=source)

    return handler.get_tickers(moniker)
