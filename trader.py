import threading
import time


class Trader:
    """Basic trader that operates on a simulation environment."""


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
