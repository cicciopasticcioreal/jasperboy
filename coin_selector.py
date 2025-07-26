import random
from typing import List


class CoinSelector:
    """Selects cryptocurrencies to trade."""

    def __init__(
        self, available_coins: List[str] | None = None, max_coins: int = 3
    ) -> None:
        self.available_coins = available_coins or [
            "BTC",
            "ETH",
            "SOL",
            "XRP",
            "ADA",
        ]
        self.max_coins = max_coins

    def select_coins(self) -> List[str]:
        """Return a random subset of coins to trade."""
        num = min(self.max_coins, len(self.available_coins))
        return random.sample(self.available_coins, num)
