import random
from typing import Dict, List, Type

from strategies import Strategy, BuyAndHoldStrategy, MovingAverageStrategy


class StrategySelector:
    """Automatically chooses a strategy for each coin."""

    def __init__(self, strategies: List[Type[Strategy]] | None = None) -> None:
        self.strategies = strategies or [
            BuyAndHoldStrategy,
            MovingAverageStrategy,
        ]

    def select_strategies(self, coins: List[str]) -> Dict[str, Strategy]:
        mapping: Dict[str, Strategy] = {}
        for coin in coins:
            strat_cls = random.choice(self.strategies)
            mapping[coin] = strat_cls()
        return mapping
