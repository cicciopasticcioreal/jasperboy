from typing import List, Dict


class TradeHistory:
    """Track executed trades and simple performance metrics."""

    def __init__(self) -> None:
        self.trades: List[Dict[str, float | str]] = []
        self.wins = 0
        self.losses = 0

    def record_trade(
        self, coin: str, side: str, price: float, success: bool
    ) -> None:
        self.trades.append({"coin": coin, "side": side, "price": price})
        if success:
            self.wins += 1
        else:
            self.losses += 1

    def performance(self) -> float:
        total = self.wins + self.losses
        if total == 0:
            return 0.0
        return self.wins / total
