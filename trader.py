import threading
import time
import random
from typing import Callable, Any, Optional

from coin_selector import CoinSelector
from exchange import ExchangeConnector
from market_cache import MarketCache
from simulation import SimulationEnvironment
from strategy_selector import StrategySelector
from autolearner import AutoLearner
from trade_history import TradeHistory


class Trader:
    """Basic trader that operates on a simulation environment."""

    def __init__(
        self,
        stop_event: threading.Event,
        environment: Optional[SimulationEnvironment] = None,
        market_fetcher: Optional[Callable[[], Any]] = None,
        coin_selector: Optional[CoinSelector] = None,
        strategy_selector: Optional[StrategySelector] = None,
        exchange: Optional[ExchangeConnector] = None,
        history: Optional[TradeHistory] = None,
    ) -> None:
        self.stop_event = stop_event
        self.env = environment or SimulationEnvironment()
        self.market_cache = MarketCache(market_fetcher or (lambda: []))
        self.coin_selector = coin_selector or CoinSelector()
        self.strategy_selector = strategy_selector or StrategySelector()
        self.exchange = exchange or ExchangeConnector()
        self.history = history or TradeHistory()
        self.learner = AutoLearner(self.strategy_selector, self.history)
        self.coins = self.coin_selector.select_coins()
        self.strategies = self.strategy_selector.select_strategies(self.coins)

    def run(self):
        """Run until stop_event is set."""
        while not self.stop_event.is_set():
            self.market_cache.update_cache()
            try:
                price = self.env.step()
            except StopIteration:
                print("Simulation finished")
                break
            except Exception as exc:
                print(f"Error: {exc}")
                break

            for coin, strategy in self.strategies.items():
                signal = strategy.generate_signal(price)
                if signal != "hold":
                    self.exchange.place_order(coin, signal, 1)
                    # Determine trade success using next price if available
                    next_price = price
                    if hasattr(self.env, "prices") and self.env._index < len(self.env.prices):
                        next_price = self.env.prices[self.env._index]
                    if signal == "buy":
                        success = next_price > price
                    else:
                        success = next_price < price
                    self.history.record_trade(
                        coin, signal, price, success=success
                    )
                    self.learner.record_trade(coin, success)

            self.learner.review(self.strategies)

            print(f"Processed price {price:.2f} for coins {self.coins}")
            time.sleep(1)
        print("Trader stopped")
