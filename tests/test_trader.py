import os
import sys
import threading
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from trader import Trader  # noqa: E402
from simulation import SimulationEnvironment, Backtester  # noqa: E402


class TraderTestCase(unittest.TestCase):
    def test_trader_stops_on_event(self):
        stop_event = threading.Event()
        env = SimulationEnvironment(prices=[1, 2, 3])
        trader = Trader(stop_event, env)
        thread = threading.Thread(target=trader.run)
        thread.start()
        stop_event.set()
        thread.join(timeout=5)
        self.assertFalse(thread.is_alive())

    def test_backtester_runs(self):
        stop_event = threading.Event()
        env = SimulationEnvironment(prices=[1, 2, 3])
        trader = Trader(stop_event, env)
        backtester = Backtester(env)
        results = backtester.run(trader)
        self.assertEqual(results, [1, 2, 3])

    def test_trader_uses_market_cache_once(self):
        calls = []

        def fetch():
            calls.append(1)
            return ["m"]

        stop_event = threading.Event()
        env = SimulationEnvironment(prices=[1])
        trader = Trader(stop_event, env, market_fetcher=fetch)
        thread = threading.Thread(target=trader.run)
        thread.start()
        thread.join(timeout=5)
        self.assertEqual(len(calls), 1)

    def test_trade_success_calculation(self):
        class BuyStrategy:
            def generate_signal(self, price):
                return "buy"

        stop_event = threading.Event()
        env = SimulationEnvironment(prices=[1, 2])
        trader = Trader(
            stop_event,
            env,
            coin_selector=type("C", (), {"select_coins": lambda self: ["BTC"]})(),
            strategy_selector=type(
                "S", (), {"select_strategies": lambda self, coins: {c: BuyStrategy() for c in coins}}
            )(),
        )
        thread = threading.Thread(target=trader.run)
        thread.start()
        thread.join(timeout=5)
        self.assertEqual(trader.history.wins, 1)


if __name__ == '__main__':
    unittest.main()
