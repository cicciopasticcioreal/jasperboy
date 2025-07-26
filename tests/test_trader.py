import threading
import unittest
from trader import Trader
from simulation import SimulationEnvironment, Backtester

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

if __name__ == '__main__':
    unittest.main()
