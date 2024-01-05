""" model classes """

from abc import ABC, abstractmethod


class PriceEngine(ABC):
    """ Price Engine """

    priority: int = 0

    def __init__(self, source=None):
        self.source = source

    @abstractmethod
    def get_prices(self,
                   ticker: str, freq: str = 'daily', *,
                   start_date=None, end_date=None,
                   max_bars=None, adjusted=True):
        """ fetch prices data """
        ...


class TickerHandler(ABC):
    """ Ticker Handler """

    priority: int = 0

    def __init__(self, source=None):
        self.source = source

    @abstractmethod
    def get_tickers(self, moniker: str):
        ...
