import threading
import time
from typing import Optional, Callable, Any
from simulation import SimulationEnvironment
from market_cache import MarketCache

class Trader:
    """Basic trader that operates on a simulation environment."""

    def __init__(self, stop_event: threading.Event, environment: Optional[SimulationEnvironment] = None,
                 market_fetcher: Optional[Callable[[], Any]] = None):
        self.stop_event = stop_event
        self.env = environment or SimulationEnvironment()
        self.market_cache = MarketCache(market_fetcher or (lambda: []))

    def run(self):
        """Run until stop_event is set."""
        while not self.stop_event.is_set():
            # Refresh market data periodically
            self.market_cache.update_cache()
            try:
                price = self.env.step()
                print(f"Processing price: {price:.2f}")
            except StopIteration:
                print("Simulation finished")
                break
            except Exception as exc:
                print(f"Error: {exc}")
                break
            time.sleep(1)
        print("Trader stopped")
