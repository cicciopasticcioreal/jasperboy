import itertools
import random

class SimulationEnvironment:
    """Simple simulated market environment."""

    def __init__(self, prices=None):
        self.prices = prices or [100 + random.uniform(-1, 1) for _ in range(100)]
        self._index = 0

    def reset(self):
        self._index = 0

    def step(self):
        if self._index >= len(self.prices):
            raise StopIteration("No more data")
        price = self.prices[self._index]
        self._index += 1
        return price

class Backtester:
    def __init__(self, environment: SimulationEnvironment):
        self.env = environment

    def run(self, trader, max_steps=100):
        self.env.reset()
        results = []
        for _ in range(max_steps):
            try:
                price = self.env.step()
                results.append(price)
            except StopIteration:
                break
            if trader.stop_event.is_set():
                break
        return results
