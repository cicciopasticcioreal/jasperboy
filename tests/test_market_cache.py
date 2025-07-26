import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from market_cache import MarketCache  # noqa: E402


def test_cache_updates_once_per_hour():
    calls = []

    def fetcher():
        calls.append(1)
        return ["market"]

    cache = MarketCache(fetcher)
    assert len(calls) == 1

    # Should not update because less than an hour passed
    cache.update_cache()
    assert len(calls) == 1

    # Simulate time passing
    cache._last_updated -= datetime.timedelta(hours=2)
    cache.update_cache()
    assert len(calls) == 2
