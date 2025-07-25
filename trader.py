import threading
import time
from typing import Optional
from simulation import SimulationEnvironment

class Trader:
    """Basic trader that operates on a simulation environment."""

    def __init__(self, stop_event: threading.Event, environment: Optional[SimulationEnvironment] = None):
        self.stop_event = stop_event
        self.env = environment or SimulationEnvironment()

    def run(self):
        """Run until stop_event is set."""
        while not self.stop_event.is_set():
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
