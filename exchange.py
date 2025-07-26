class ExchangeConnector:
    """Basic interface for exchange interactions."""

    def place_order(self, coin: str, side: str, amount: float) -> None:
        print(f"Placing {side} order for {amount} {coin}")


class BybitConnector(ExchangeConnector):
    """Stub connector for Bybit exchange."""

    pass
