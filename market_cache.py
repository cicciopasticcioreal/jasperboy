import datetime
from typing import Callable, Any


class MarketCache:
    """Simple cache for market data with periodic refresh."""

    def __init__(self, fetcher: Callable[[], Any]):
        """Initialize cache and load markets once.

        Parameters
        ----------
        fetcher: Callable[[], Any]
            Function used to fetch fresh market data.
        """
        self._fetcher = fetcher
        self.markets = self._fetcher()
        self._last_updated = datetime.datetime.now(datetime.timezone.utc)

    @property
    def last_updated(self) -> datetime.datetime:
        """Return timestamp of last cache update."""
        return self._last_updated

    def update_cache(self, force: bool = False) -> None:
        """Refresh markets if one hour has passed or if forced."""
        now = datetime.datetime.now(datetime.timezone.utc)
        if force or (now - self._last_updated >= datetime.timedelta(hours=1)):
            self.markets = self._fetcher()
            self._last_updated = now
