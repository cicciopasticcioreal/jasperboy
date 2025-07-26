import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from coin_selector import CoinSelector  # noqa: E402
from strategy_selector import StrategySelector  # noqa: E402


def test_coin_selector_limit():
    selector = CoinSelector(max_coins=2)
    coins = selector.select_coins()
    assert len(coins) == 2


def test_strategy_selector_maps_to_coins():
    coins = ["BTC", "ETH"]
    sel = StrategySelector()
    strategies = sel.select_strategies(coins)
    assert set(strategies.keys()) == set(coins)
