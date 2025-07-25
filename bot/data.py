import ccxt
import pandas as pd
from typing import List

class DataFetcher:
    def __init__(self, exchange_id: str = "binance"):
        self.exchange = getattr(ccxt, exchange_id)()

    def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> pd.DataFrame:
        """Fetch OHLCV data for a symbol and return as DataFrame."""
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def list_markets(self) -> List[str]:
        markets = self.exchange.load_markets()
        return list(markets.keys())
