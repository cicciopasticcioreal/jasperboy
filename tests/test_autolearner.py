import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from autolearner import AutoLearner  # noqa: E402
from strategy_selector import StrategySelector  # noqa: E402
from strategies import BuyAndHoldStrategy  # noqa: E402


def test_autolearner_switches_strategy():
    selector = StrategySelector(strategies=[BuyAndHoldStrategy])
    history = type('H', (), {'trades': []})()
    learner = AutoLearner(selector, history, min_trades=2)
    strategies = {'BTC': BuyAndHoldStrategy()}

    learner.record_trade('BTC', success=False)
    learner.record_trade('BTC', success=False)
    learner.review(strategies)

    assert isinstance(strategies['BTC'], BuyAndHoldStrategy)
    assert learner.trades_by_coin['BTC'] == {'wins': 0, 'losses': 0}
