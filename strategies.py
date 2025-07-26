from __future__ import annotations

from collections import deque


class Strategy:
    """Base class for trading strategies."""

    def generate_signal(self, price: float) -> str:
        """Return 'buy', 'sell', or 'hold'."""
        return "hold"


class BuyAndHoldStrategy(Strategy):
    """Always hold."""

    def generate_signal(self, price: float) -> str:  # noqa: D401
        return "hold"


class MovingAverageStrategy(Strategy):
    """Simple moving average crossover strategy."""

    def __init__(self, window: int = 5) -> None:
        self.window = window
        self.prices: deque[float] = deque(maxlen=window)

    def generate_signal(self, price: float) -> str:
        self.prices.append(price)
        if len(self.prices) < self.window:
            return "hold"
        avg = sum(self.prices) / len(self.prices)
        if price > avg:
            return "buy"
        return "sell"
