from dataclasses import dataclass
import pandas as pd

@dataclass
class TradeSignal:
    symbol: str
    action: str  # 'buy' or 'sell'
    confidence: float

class SimpleMovingAverageStrategy:
    def __init__(self, short_window: int = 20, long_window: int = 50):
        self.short_window = short_window
        self.long_window = long_window

    def generate(self, df: pd.DataFrame, symbol: str) -> TradeSignal:
        """Generate trade signal based on SMA crossover."""
        if len(df) < self.long_window:
            return TradeSignal(symbol, 'hold', 0.0)
        sma_short = df['close'].rolling(window=self.short_window).mean()
        sma_long = df['close'].rolling(window=self.long_window).mean()
        if sma_short.iloc[-2] < sma_long.iloc[-2] and sma_short.iloc[-1] > sma_long.iloc[-1]:
            return TradeSignal(symbol, 'buy', 1.0)
        elif sma_short.iloc[-2] > sma_long.iloc[-2] and sma_short.iloc[-1] < sma_long.iloc[-1]:
            return TradeSignal(symbol, 'sell', 1.0)
        return TradeSignal(symbol, 'hold', 0.0)
